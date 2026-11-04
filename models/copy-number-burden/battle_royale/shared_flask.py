"""Shared-flask competition with carriers and plasmid-free descendants.

Extracted from the notebook's "Shared-flask simulator" cell. Function bodies are unchanged
except that references to declared parameters now go through `config`, so the
notebook's Colab widgets stay authoritative at runtime.
"""
import warnings

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

from . import config
from .analytic import (
    _broadcast_design_parameter,
    _resolve_beta,
    _resolve_loss,
    _validate_loss,
    _validate_pcn,
    pcn_dependent_loss_per_division,
    puc_burden_components,
    puc_growth_factor,
    relative_growth,
)

def simulate_shared_batch(pcns,hours=None,reference_doubling_time_h=None,total_n0=None,carrying_capacity=None,beta=None,loss_per_division=None,plasmid_free_growth_multiplier=None,n_points=500,initial_fractions=None):
    hours=config.SHARED_HOURS if hours is None else hours; reference_doubling_time_h=config.REFERENCE_DOUBLING_TIME_H if reference_doubling_time_h is None else reference_doubling_time_h
    total_n0=config.TOTAL_STARTING_CELLS if total_n0 is None else total_n0; carrying_capacity=config.CARRYING_CAPACITY if carrying_capacity is None else carrying_capacity
    plasmid_free_growth_multiplier=config.PLASMID_FREE_GROWTH_MULTIPLIER if plasmid_free_growth_multiplier is None else plasmid_free_growth_multiplier
    beta=_resolve_beta(beta); loss_per_division=_validate_loss(_resolve_loss(loss_per_division)); pcns=np.asarray(pcns,dtype=float); _validate_pcn(pcns,beta=beta)
    if carrying_capacity<=total_n0: raise ValueError('carrying_capacity must exceed total_n0.')
    if pcns.ndim != 1 or len(pcns)==0 or not np.all(np.isfinite(pcns)): raise ValueError("pcns must be a nonempty finite vector.")
    k=len(pcns); mu0=np.log(2)/reference_doubling_time_h; mu_carrier=mu0*relative_growth(pcns,beta=beta); mu_free=mu0*plasmid_free_growth_multiplier
    loss_hazard_full=np.zeros(k) if loss_per_division==0 else -np.log(1-loss_per_division)*mu_carrier/np.log(2)
    fractions = np.full(k,1/k) if initial_fractions is None else np.asarray(initial_fractions,float)
    if fractions.shape != (k,) or not np.all(np.isfinite(fractions)) or np.any(fractions<=0) or not np.isclose(fractions.sum(),1.0,rtol=0,atol=1e-10):
        raise ValueError('initial_fractions must be finite, positive, match pcns and sum to one.')
    p0=total_n0*fractions; f0=np.zeros(k); y0=np.concatenate([p0,f0])
    def ode(t,y):
        P=y[:k]; F=y[k:]; total=np.sum(P)+np.sum(F); resource=max(0.0,1.0-total/carrying_capacity); transfer=loss_hazard_full*resource*P
        return np.concatenate([mu_carrier*resource*P-transfer,mu_free*resource*F+transfer])
    t_eval=np.linspace(0,hours,n_points); sol=solve_ivp(ode,(0,hours),y0,t_eval=t_eval,rtol=1e-8,atol=1e-10)
    if not sol.success: raise RuntimeError(sol.message)
    if not np.all(np.isfinite(sol.y)): raise RuntimeError('Non-finite values returned by ODE solver.')
    P=sol.y[:k]; F=sol.y[k:]; total_by_design=P+F; total_all=np.sum(total_by_design,axis=0); resource_t=np.clip(1-total_all/carrying_capacity,0,1)
    barcode_signal=P*pcns[:,None]; denom=np.maximum(np.sum(total_by_design,axis=0,keepdims=True),1e-300); carrier_cell_fraction=P/denom; design_cell_fraction=total_by_design/denom
    barcode_fraction=barcode_signal/np.maximum(np.sum(barcode_signal,axis=0,keepdims=True),1e-300)
    gross=np.array([np.trapezoid(mu_carrier[i]*resource_t/np.log(2),sol.t) for i in range(k)]); net=np.log2(np.maximum(P[:,-1],1e-300)/P[:,0])
    return {'time_h':sol.t,'carriers':P,'plasmid_free':F,'design_total':total_by_design,'carrier_cell_fraction':carrier_cell_fraction,'design_cell_fraction':design_cell_fraction,'barcode_fraction':barcode_fraction,'pcns':pcns,'mu_carrier':mu_carrier,'resource':resource_t,'gross_carrier_doublings':gross,'net_carrier_log2_change':net}

def evaluate_focal_metrics(candidate_pcn,pool=None,focal_fraction=None,**kwargs):
    """Evaluate one focal candidate against a declared fixed pool.

    Returns separate biological and measurement-proxy readouts so absolute plasmid
    yield is never silently conflated with within-pool barcode fraction.
    """
    pool=config.REFERENCE_POOL_PCNS if pool is None else np.asarray(pool,float)
    focal_fraction=config.FOCAL_FRACTION if focal_fraction is None else float(focal_fraction)
    if pool.ndim != 1 or len(pool)==0 or not np.all(np.isfinite(pool)):
        raise ValueError('pool must be a nonempty finite vector.')
    if not 0<focal_fraction<1:
        raise ValueError('0 < focal_fraction < 1 required.')
    fractions=np.r_[focal_fraction,np.repeat((1-focal_fraction)/len(pool),len(pool))]
    result=simulate_shared_batch(np.r_[float(candidate_pcn),pool],initial_fractions=fractions,**kwargs)
    carrier=float(result['carriers'][0,-1])
    absolute_plasmids=carrier*float(candidate_pcn)
    barcode_fraction=float(result['barcode_fraction'][0,-1])
    lineage_fraction=float(result['design_cell_fraction'][0,-1])
    total_cells=float(np.sum(result['design_total'][:,-1]))
    k_used=config.CARRYING_CAPACITY if kwargs.get('carrying_capacity',None) is None else float(kwargs['carrying_capacity'])
    return {
        'carrier_cells':carrier,
        'absolute_plasmids':absolute_plasmids,
        'barcode_fraction':barcode_fraction,
        'lineage_fraction':lineage_fraction,
        'total_cells':total_cells,
        'occupancy':total_cells/k_used,
    }

def evaluate_focal(candidate_pcn,pool=None,focal_fraction=None,**kwargs):
    """Backward-compatible two-column view: carrier cells, absolute plasmids."""
    m=evaluate_focal_metrics(candidate_pcn,pool=pool,focal_fraction=focal_fraction,**kwargs)
    return m['carrier_cells'],m['absolute_plasmids']

def focal_grid(candidates,**kwargs):
    return np.array([evaluate_focal(c,**kwargs) for c in candidates])

def focal_metric_grid(candidates,metric='absolute_plasmids',**kwargs):
    allowed={'carrier_cells','absolute_plasmids','barcode_fraction','lineage_fraction'}
    if metric not in allowed: raise ValueError(f'metric must be one of {sorted(allowed)}')
    return np.array([evaluate_focal_metrics(c,**kwargs)[metric] for c in candidates],dtype=float)

def bounded_focal_optimum(metric='absolute_plasmids',lower=10.0,upper=None,**kwargs):
    """Resolution-independent bounded optimum for one declared focal readout."""
    upper=float(config.VALIDATED_PCN_MAX if upper is None else upper); lower=float(lower)
    if not lower<upper: raise ValueError('lower must be < upper.')
    def value(c): return evaluate_focal_metrics(c,**kwargs)[metric]
    opt=minimize_scalar(lambda c:-value(c),bounds=(lower,upper),method='bounded')
    if not opt.success: raise RuntimeError(opt.message)
    options=[lower,float(opt.x),upper]
    best=max(options,key=value)
    return float(best),float(value(best))


# --- pUC-specific fixed-PCN extension -------------------------------------------------
def simulate_puc_fixed_batch(pcns, plasmid_bp=None, cargo_burden_max=None,
                             cargo_half_sat_pcn=None, hours=None,
                             reference_doubling_time_h=None, total_n0=None,
                             carrying_capacity=None, beta=None,
                             loss_per_division=None, loss_reference_pcn=None,
                             loss_pcn_exponent=None, plasmid_free_growth_multiplier=None,
                             n_points=500, initial_fractions=None):
    """Fixed-PCN shared flask with DNA-length and generic cargo burdens separated."""
    hours=config.SHARED_HOURS if hours is None else float(hours)
    reference_doubling_time_h=config.REFERENCE_DOUBLING_TIME_H if reference_doubling_time_h is None else float(reference_doubling_time_h)
    total_n0=config.TOTAL_STARTING_CELLS if total_n0 is None else float(total_n0)
    carrying_capacity=config.CARRYING_CAPACITY if carrying_capacity is None else float(carrying_capacity)
    plasmid_free_growth_multiplier=config.PLASMID_FREE_GROWTH_MULTIPLIER if plasmid_free_growth_multiplier is None else float(plasmid_free_growth_multiplier)
    beta=_resolve_beta(beta)
    base_loss=_validate_loss(_resolve_loss(loss_per_division))
    pcns=np.asarray(pcns,dtype=float)
    _validate_pcn(pcns,beta=beta)
    if pcns.ndim!=1 or len(pcns)==0 or not np.all(np.isfinite(pcns)):
        raise ValueError('pcns must be a nonempty finite vector.')
    if carrying_capacity<=total_n0: raise ValueError('carrying_capacity must exceed total_n0.')
    k=len(pcns)
    bp=_broadcast_design_parameter(config.PUC_DEFAULT_PLASMID_BP if plasmid_bp is None else plasmid_bp,k,'plasmid_bp',positive=True)
    cargo=_broadcast_design_parameter(config.PUC_DEFAULT_CARGO_MAX if cargo_burden_max is None else cargo_burden_max,k,'cargo_burden_max',nonnegative=True)
    if np.any(cargo>=1): raise ValueError('cargo_burden_max must be < 1.')
    fractions=np.full(k,1/k) if initial_fractions is None else np.asarray(initial_fractions,float)
    if fractions.shape!=(k,) or not np.all(np.isfinite(fractions)) or np.any(fractions<=0) or not np.isclose(fractions.sum(),1.0,rtol=0,atol=1e-10):
        raise ValueError('initial_fractions must be finite, positive, match pcns and sum to one.')
    dna_burden,cargo_burden=puc_burden_components(pcns,bp,cargo,cargo_half_sat_pcn,beta)
    growth_factor=puc_growth_factor(pcns,bp,cargo,cargo_half_sat_pcn,beta)
    mu0=np.log(2)/reference_doubling_time_h
    mu_carrier=mu0*growth_factor
    mu_free=mu0*plasmid_free_growth_multiplier
    loss_div=pcn_dependent_loss_per_division(pcns,base_loss,loss_reference_pcn,loss_pcn_exponent)
    loss_hazard=np.where(loss_div>0,-np.log(1-loss_div)*mu_carrier/np.log(2),0.0)
    p0=total_n0*fractions; f0=np.zeros(k); y0=np.concatenate([p0,f0])
    def ode(t,y):
        P=np.maximum(y[:k],0); F=np.maximum(y[k:],0)
        total=np.sum(P)+np.sum(F)
        resource=max(0.0,1.0-total/carrying_capacity)
        transfer=loss_hazard*resource*P
        return np.concatenate([mu_carrier*resource*P-transfer,mu_free*resource*F+transfer])
    sol=solve_ivp(ode,(0,hours),y0,t_eval=np.linspace(0,hours,n_points),rtol=1e-8,atol=1e-10)
    if not sol.success: raise RuntimeError(sol.message)
    if not np.all(np.isfinite(sol.y)): raise RuntimeError('Non-finite values returned by ODE solver.')
    P=np.maximum(sol.y[:k],0); F=np.maximum(sol.y[k:],0); total=P+F
    total_all=np.sum(total,axis=0)
    barcode_signal=P*pcns[:,None]
    return {
        'time_h':sol.t,'pcns':pcns,'plasmid_bp':bp,'cargo_burden_max':cargo,
        'dna_burden':dna_burden,'cargo_burden':cargo_burden,'growth_factor':growth_factor,
        'loss_per_division_effective':loss_div,'carriers':P,'plasmid_free':F,
        'design_total':total,
        'design_cell_fraction':total/np.maximum(total_all[None,:],1e-300),
        'barcode_fraction':barcode_signal/np.maximum(np.sum(barcode_signal,axis=0,keepdims=True),1e-300),
    }

def simulate_puc_focal_fixed(candidate_pcn, candidate_bp=None, candidate_cargo=None,
                             pool_pcns=None, pool_bp=None, pool_cargo=None,
                             focal_fraction=None, **kwargs):
    pool=config.REFERENCE_POOL_PCNS if pool_pcns is None else np.asarray(pool_pcns,float)
    if pool.ndim!=1 or len(pool)<1 or not np.all(np.isfinite(pool)):
        raise ValueError('pool_pcns must be a nonempty finite vector.')
    # Canonical Arena baseline is 19 competitors + 1 focal strain. For explicit
    # pool-size sensitivity, allow other sizes but default to equal inoculation
    # for the actual number of lineages rather than preserving an inconsistent 5%.
    if len(pool)!=config.ARENA_TEAM_COUNT-1:
        warnings.warn(
            f'Pool has {len(pool)} competitors; declared Arena baseline is {config.ARENA_TEAM_COUNT-1}. '
            'Using a synthetic pool-size scenario.',RuntimeWarning,stacklevel=2)
    ff=(1.0/(len(pool)+1)) if focal_fraction is None else float(focal_fraction)
    if not 0<ff<1:
        raise ValueError('0 < focal_fraction < 1 required.')
    pcns=np.r_[float(candidate_pcn),pool]
    bp=np.r_[config.PUC_DEFAULT_PLASMID_BP if candidate_bp is None else float(candidate_bp),
             np.repeat(config.PUC_DEFAULT_PLASMID_BP if pool_bp is None else float(pool_bp),len(pool))]
    cargo=np.r_[config.PUC_DEFAULT_CARGO_MAX if candidate_cargo is None else float(candidate_cargo),
                np.repeat(config.PUC_DEFAULT_CARGO_MAX if pool_cargo is None else float(pool_cargo),len(pool))]
    fractions=np.r_[ff,np.repeat((1-ff)/len(pool),len(pool))]
    return simulate_puc_fixed_batch(pcns,plasmid_bp=bp,cargo_burden_max=cargo,
                                    initial_fractions=fractions,**kwargs)

def evaluate_puc_focal_fixed(candidate_pcn, candidate_bp=None, candidate_cargo=None,
                             metric='absolute_plasmids', **kwargs):
    sim=simulate_puc_focal_fixed(candidate_pcn,candidate_bp=candidate_bp,
                                 candidate_cargo=candidate_cargo,**kwargs)
    carrier=float(sim['carriers'][0,-1]); absolute=carrier*float(candidate_pcn)
    vals={
        'carrier_cells':carrier,
        'absolute_plasmids':absolute,
        'barcode_fraction':float(sim['barcode_fraction'][0,-1]),
        'lineage_fraction':float(sim['design_cell_fraction'][0,-1]),
    }
    if metric not in vals: raise ValueError(f'unknown metric {metric}')
    return vals[metric]

def _max_valid_puc_pcn(plasmid_bp=None,cargo_burden_max=None,cargo_half_sat_pcn=None,beta=None,
                       search_upper=None):
    """Largest PCN inside the positive-growth domain of the first-order pUC law."""
    bp=config.PUC_DEFAULT_PLASMID_BP if plasmid_bp is None else float(plasmid_bp)
    cargo=config.PUC_DEFAULT_CARGO_MAX if cargo_burden_max is None else float(cargo_burden_max)
    half=config.PUC_CARGO_HALF_SAT_PCN if cargo_half_sat_pcn is None else float(cargo_half_sat_pcn)
    beta=float(_resolve_beta(beta))
    upper=float(config.VALIDATED_PCN_MAX if search_upper is None else search_upper)
    def burden(c): return beta*c*(bp/config.PUC19_BP)+cargo*c/(half+c)
    if burden(upper)<1.0:
        return upper
    # monotone burden law: bisection is deterministic and avoids invalid ODE calls
    lo,hi=0.0,upper
    for _ in range(80):
        mid=(lo+hi)/2
        if burden(mid)<1.0: lo=mid
        else: hi=mid
    return np.nextafter(lo,0.0)

def bounded_puc_focal_optimum(candidate_bp=None,candidate_cargo=None,metric='absolute_plasmids',
                              lower=10.0,upper=None,**kwargs):
    requested_upper=float(config.VALIDATED_PCN_MAX if upper is None else upper)
    safe_upper=_max_valid_puc_pcn(
        candidate_bp,candidate_cargo,kwargs.get('cargo_half_sat_pcn',None),kwargs.get('beta',None),
        search_upper=requested_upper)
    lower=float(lower)
    if not lower<safe_upper:
        raise ValueError(f'No positive-growth search interval: lower={lower:g}, valid upper={safe_upper:g}.')
    def value(c): return evaluate_puc_focal_fixed(c,candidate_bp,candidate_cargo,metric=metric,**kwargs)
    opt=minimize_scalar(lambda c:-value(c),bounds=(lower,safe_upper),method='bounded')
    if not opt.success: raise RuntimeError(opt.message)
    options=[lower,float(opt.x),safe_upper]
    best=max(options,key=value)
    return float(best),float(value(best))

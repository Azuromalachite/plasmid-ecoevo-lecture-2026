"""Substrate depletion with growth-state-dependent copy number.

Extracted from the notebook's "Mechanistic substrate + dynamic-PCN simulator" cell. Function bodies are unchanged
except that references to declared parameters now go through `config`, so the
notebook's Colab widgets stay authoritative at runtime.
"""
import warnings

import numpy as np
from scipy.integrate import solve_ivp

from . import config
from .analytic import (
    _broadcast_design_parameter,
    _resolve_beta,
    _resolve_loss,
    _validate_loss,
    _validate_pcn,
    copy_relaxation_rate,
    copy_setpoint,
    monod_activity,
    pcn_dependent_loss_per_division,
    puc_growth_factor,
)

def validate_mechanistic_raw_state(raw_C,raw_S,pcn_cap,tol=1e-6):
    raw_C=np.asarray(raw_C,dtype=float); raw_S=np.asarray(raw_S,dtype=float)
    if not np.all(np.isfinite(raw_C)) or not np.all(np.isfinite(raw_S)): raise RuntimeError('Mechanistic solver produced non-finite states.')
    if np.min(raw_S)<-tol: raise RuntimeError(f'Substrate became materially negative: min={np.min(raw_S):.3e}')
    if np.min(raw_C)<-tol: raise RuntimeError(f'PCN became materially negative: min={np.min(raw_C):.3e}')
    if np.max(raw_C)>pcn_cap+tol: raise RuntimeError(f'PCN exceeded configured cap: max={np.max(raw_C):.3f}')
    return True

def simulate_mechanistic_batch(pcns,hours=None,reference_doubling_time_h=None,total_n0=None,
                               carrying_capacity=None,beta=None,monod_ks=None,copy_replication_ks=None,
                               feedback_gamma=None,copy_relaxation_h=None,max_copy_setpoint_fold=None,
                               pcn_cap=None,loss_per_division=None,loss_reference_pcn=None,
                               loss_pcn_exponent=None,plasmid_free_growth_multiplier=None,
                               plasmid_bp=None,cargo_burden_max=None,cargo_half_sat_pcn=None,
                               initial_fractions=None,n_points=700):
    hours=config.SHARED_HOURS if hours is None else float(hours)
    reference_doubling_time_h=config.REFERENCE_DOUBLING_TIME_H if reference_doubling_time_h is None else float(reference_doubling_time_h)
    total_n0=config.TOTAL_STARTING_CELLS if total_n0 is None else float(total_n0)
    carrying_capacity=config.CARRYING_CAPACITY if carrying_capacity is None else float(carrying_capacity)
    monod_ks=config.MONOD_KS if monod_ks is None else float(monod_ks)
    copy_replication_ks=config.COPY_REPLICATION_KS if copy_replication_ks is None else float(copy_replication_ks)
    feedback_gamma=config.COPY_FEEDBACK_GAMMA if feedback_gamma is None else float(feedback_gamma)
    copy_relaxation_h=config.COPY_RELAXATION_H if copy_relaxation_h is None else float(copy_relaxation_h)
    max_copy_setpoint_fold=config.MAX_COPY_SETPOINT_FOLD if max_copy_setpoint_fold is None else float(max_copy_setpoint_fold)
    pcn_cap=config.DYNAMIC_PCN_CAP if pcn_cap is None else float(pcn_cap)
    plasmid_free_growth_multiplier=config.PLASMID_FREE_GROWTH_MULTIPLIER if plasmid_free_growth_multiplier is None else float(plasmid_free_growth_multiplier)
    beta=_resolve_beta(beta); base_loss=_validate_loss(_resolve_loss(loss_per_division))
    pcns_ref=np.asarray(pcns,dtype=float); _validate_pcn(pcns_ref,beta=beta)
    if pcns_ref.ndim!=1 or len(pcns_ref)==0: raise ValueError('pcns must be a nonempty vector.')
    if np.any(pcns_ref>pcn_cap): raise ValueError('Starting PCN cannot exceed pcn_cap.')
    if monod_ks<=0 or copy_replication_ks<=0: raise ValueError('Monod constants must be > 0.')
    if copy_relaxation_h<=0: raise ValueError('copy_relaxation_h must be > 0.')
    if carrying_capacity<=total_n0: raise ValueError('carrying_capacity must exceed total_n0.')
    k=len(pcns_ref)
    bp=_broadcast_design_parameter(config.PUC_DEFAULT_PLASMID_BP if plasmid_bp is None else plasmid_bp,k,'plasmid_bp',positive=True)
    cargo=_broadcast_design_parameter(config.PUC_DEFAULT_CARGO_MAX if cargo_burden_max is None else cargo_burden_max,k,'cargo_burden_max',nonnegative=True)
    if np.any(cargo>=1): raise ValueError('cargo_burden_max must be < 1.')
    fractions=np.full(k,1/k) if initial_fractions is None else np.asarray(initial_fractions,float)
    if fractions.shape!=(k,) or not np.all(np.isfinite(fractions)) or np.any(fractions<=0) or not np.isclose(fractions.sum(),1.0,rtol=0,atol=1e-10):
        raise ValueError('initial_fractions must be finite, positive, match pcns and sum to one.')

    mu_max=np.log(2)/reference_doubling_time_h
    s0=1.0
    growth_activity0=float(monod_activity(s0,monod_ks))
    mu_env0=mu_max*growth_activity0
    mu_ref=mu_env0*puc_growth_factor(pcns_ref,bp,cargo,cargo_half_sat_pcn,beta)
    p0=total_n0*fractions; f0=np.zeros(k); c0=pcns_ref.copy()
    y0=np.concatenate([p0,f0,c0,[s0]])
    biomass_capacity=carrying_capacity-total_n0

    def ode(t,y):
        P=np.maximum(y[:k],0); F=np.maximum(y[k:2*k],0); C=np.maximum(y[2*k:3*k],1e-9); S=float(y[-1])
        ga=float(monod_activity(S,monod_ks)); ca=float(monod_activity(S,copy_replication_ks)); mu_env=mu_max*ga
        gf=puc_growth_factor(C,bp,cargo,cargo_half_sat_pcn,beta)
        mu_carrier=mu_env*gf
        mu_free=mu_env*plasmid_free_growth_multiplier
        loss_div=pcn_dependent_loss_per_division(C,base_loss,loss_reference_pcn,loss_pcn_exponent)
        transfer=np.zeros(k) if base_loss==0 else (-np.log(1-loss_div))*mu_carrier/np.log(2)*P
        c_ss=copy_setpoint(pcns_ref,mu_carrier,mu_ref,gamma=feedback_gamma,max_fold=max_copy_setpoint_fold,pcn_cap=pcn_cap)
        dC=copy_relaxation_rate(C,c_ss,copy_relaxation_h,ca)
        dP=mu_carrier*P-transfer
        dF=mu_free*F+transfer
        gross=np.sum(mu_carrier*P)+mu_free*np.sum(F)
        dS=-gross/biomass_capacity if S>0 else 0.0
        return np.concatenate([dP,dF,dC,[dS]])

    sol=solve_ivp(ode,(0,hours),y0,t_eval=np.linspace(0,hours,n_points),rtol=1e-7,atol=1e-9)
    if not sol.success: raise RuntimeError(sol.message)
    raw_C=sol.y[2*k:3*k]; raw_S=sol.y[-1]
    validate_mechanistic_raw_state(raw_C,raw_S,pcn_cap)
    P=np.maximum(sol.y[:k],0); F=np.maximum(sol.y[k:2*k],0); C=np.clip(raw_C,0,pcn_cap); S=np.clip(raw_S,0,1)
    ga=monod_activity(S,monod_ks); ca=monod_activity(S,copy_replication_ks); mu_env=mu_max*ga
    mu_carrier=np.array([mu_env*puc_growth_factor(C[j],bp[j],cargo[j],cargo_half_sat_pcn,beta) for j in range(k)])
    barcode_signal=P*C
    barcode_fraction=barcode_signal/np.maximum(np.sum(barcode_signal,axis=0,keepdims=True),1e-300)
    total=P+F
    lineage_fraction=total/np.maximum(np.sum(total,axis=0,keepdims=True),1e-300)
    rel_change=np.max(np.abs(C-pcns_ref[:,None])/pcns_ref[:,None],axis=1)
    return {
        'time_h':sol.t,'pcns_ref':pcns_ref,'plasmid_bp':bp,'cargo_burden_max':cargo,
        'initial_fractions':fractions,'carriers':P,'plasmid_free':F,'pcn':C,
        'substrate':S,'growth_activity':ga,'copy_activity':ca,'mu_env':mu_env,
        'mu_carrier':mu_carrier,'barcode_fraction':barcode_fraction,
        'lineage_fraction':lineage_fraction,'relative_pcn_change':rel_change,
    }

def simulate_mechanistic_focal(candidate_pcn,candidate_bp=None,candidate_cargo=None,
                               pool_pcns=None,pool_bp=None,pool_cargo=None,
                               focal_fraction=None,**kwargs):
    pool=config.REFERENCE_POOL_PCNS if pool_pcns is None else np.asarray(pool_pcns,float)
    ff=config.FOCAL_FRACTION if focal_fraction is None else float(focal_fraction)
    if len(pool)!=config.ARENA_TEAM_COUNT-1:
        raise ValueError(f'Expected {config.ARENA_TEAM_COUNT-1} reference competitors.')
    pcns=np.r_[float(candidate_pcn),pool]
    bp=np.r_[config.PUC_DEFAULT_PLASMID_BP if candidate_bp is None else float(candidate_bp),
             np.repeat(config.PUC_DEFAULT_PLASMID_BP if pool_bp is None else float(pool_bp),len(pool))]
    cargo=np.r_[config.PUC_DEFAULT_CARGO_MAX if candidate_cargo is None else float(candidate_cargo),
                np.repeat(config.PUC_DEFAULT_CARGO_MAX if pool_cargo is None else float(pool_cargo),len(pool))]
    fractions=np.r_[ff,np.repeat((1-ff)/len(pool),len(pool))]
    return simulate_mechanistic_batch(pcns,plasmid_bp=bp,cargo_burden_max=cargo,
                                      initial_fractions=fractions,**kwargs)

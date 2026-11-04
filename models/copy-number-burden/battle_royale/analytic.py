"""The analytic copy-number/burden model.

Extracted from the notebook's "Core model functions" cell without edits to the
bodies, except that bare references to declared parameters now go through
`config`, so the notebook's widgets remain authoritative at runtime.

The inline assertions that followed these definitions stay in the notebook:
they are part of its narrative, and they still run there.
"""
import warnings

import numpy as np

from . import config

def _resolve_beta(beta):
    return config.BETA if beta is None else beta

def _resolve_loss(loss_per_division):
    return config.LOSS_PER_DIVISION if loss_per_division is None else loss_per_division

def _validate_loss(loss_per_division):
    loss=float(loss_per_division)
    if not (0 <= loss < 1): raise ValueError('loss_per_division must be in [0, 1).')
    return loss

def _validate_pcn(pcn,beta=None,validated_max=None):
    beta=_resolve_beta(beta)
    if validated_max is None: validated_max=config.VALIDATED_PCN_MAX
    p=np.asarray(pcn,dtype=float)
    if np.any(p<=0): raise ValueError('PCN must be > 0.')
    zero_growth_pcn=1.0/beta
    if np.any(p>=zero_growth_pcn):
        raise ValueError(f'Linear model predicts zero/negative growth at PCN >= {zero_growth_pcn:.1f}.')
    if np.any(p>validated_max):
        warnings.warn(f'PCN exceeds approximate Rouches library range ({validated_max}).',RuntimeWarning,stacklevel=2)
    return p

def relative_growth(pcn,beta=None):
    beta=_resolve_beta(beta); p=_validate_pcn(pcn,beta=beta); return 1.0-beta*p

def effective_doublings(pcn,g0,beta=None): return np.asarray(g0)*relative_growth(pcn,beta=beta)


def _broadcast_design_parameter(value, k, name, *, positive=False, nonnegative=False):
    arr=np.asarray(value,dtype=float)
    if arr.ndim==0:
        arr=np.repeat(float(arr),k)
    if arr.shape!=(k,) or not np.all(np.isfinite(arr)):
        raise ValueError(f'{name} must be a finite scalar or length-{k} vector.')
    if positive and np.any(arr<=0):
        raise ValueError(f'{name} must be > 0.')
    if nonnegative and np.any(arr<0):
        raise ValueError(f'{name} must be >= 0.')
    return arr

def puc_burden_components(pcn, plasmid_bp=None, cargo_burden_max=None,
                          cargo_half_sat_pcn=None, beta=None):
    """Scenario decomposition for pUC/ColE1-like constructs.

    dna_burden scales the Rouches pUC19 per-copy coefficient by DNA length.
    cargo_burden is a deliberately generic saturating expression penalty.
    The latter is NOT a fitted universal law; it exists to keep expression cost
    separate from DNA-copy cost during sensitivity analysis.
    """
    beta=_resolve_beta(beta)
    p=np.asarray(pcn,dtype=float)
    if np.any(p<=0) or not np.all(np.isfinite(p)):
        raise ValueError('PCN must be finite and > 0.')
    bp=config.PUC_DEFAULT_PLASMID_BP if plasmid_bp is None else np.asarray(plasmid_bp,dtype=float)
    cargo_max=config.PUC_DEFAULT_CARGO_MAX if cargo_burden_max is None else np.asarray(cargo_burden_max,dtype=float)
    half=config.PUC_CARGO_HALF_SAT_PCN if cargo_half_sat_pcn is None else float(cargo_half_sat_pcn)
    if np.any(bp<=0) or np.any(~np.isfinite(bp)): raise ValueError('plasmid_bp must be finite and > 0.')
    if np.any(cargo_max<0) or np.any(cargo_max>=1) or np.any(~np.isfinite(cargo_max)):
        raise ValueError('cargo_burden_max must be finite and in [0,1).')
    if half<=0: raise ValueError('cargo_half_sat_pcn must be > 0.')
    dna=beta*p*(bp/config.PUC19_BP)
    cargo=cargo_max*p/(half+p)
    # The length/cargo extension is first-order and only meaningful while total
    # predicted burden remains below one. Do not silently floor biologically
    # invalid negative-growth states.
    total=np.asarray(dna+cargo,dtype=float)
    if np.any(total>=1.0):
        p_b,bp_b,dna_b,cargo_b,total_b=np.broadcast_arrays(
            np.asarray(p,dtype=float),np.asarray(bp,dtype=float),
            np.asarray(dna,dtype=float),np.asarray(cargo,dtype=float),total)
        flat=int(np.argmax(total_b.ravel()))
        raise ValueError(
            'Burden model predicts zero or negative growth: '
            f'PCN={float(p_b.ravel()[flat]):.1f}, '
            f'plasmid_bp={float(bp_b.ravel()[flat]):.0f}, '
            f'dna={float(dna_b.ravel()[flat]):.3f} + '
            f'cargo={float(cargo_b.ravel()[flat]):.3f} = '
            f'{float(total_b.ravel()[flat]):.3f}. '
            'The linear first-order law does not extend here.')
    return dna,cargo

def puc_growth_factor(pcn, plasmid_bp=None, cargo_burden_max=None,
                      cargo_half_sat_pcn=None, beta=None):
    dna,cargo=puc_burden_components(
        pcn,plasmid_bp=plasmid_bp,cargo_burden_max=cargo_burden_max,
        cargo_half_sat_pcn=cargo_half_sat_pcn,beta=beta)
    growth=1.0-dna-cargo
    if np.any(growth<=0):
        raise RuntimeError('Internal burden validation failure: non-positive growth escaped validation.')
    return np.clip(growth,1e-12,1.0)

def pcn_dependent_loss_per_division(pcn, base_loss=None, reference_pcn=None,
                                    exponent=None, max_loss=0.95):
    """Phenomenological low-PCN loss sensitivity.

    exponent=0 exactly recovers the constant per-division loss model. Positive
    exponents increase loss below the reference PCN and decrease it above the
    reference. This is a scenario mechanism, not a fitted pUC segregation law.
    """
    base=_validate_loss(_resolve_loss(base_loss))
    ref=config.PUC_LOSS_REFERENCE_PCN if reference_pcn is None else float(reference_pcn)
    expn=config.PUC_LOSS_PCN_EXPONENT if exponent is None else float(exponent)
    p=np.asarray(pcn,dtype=float)
    if ref<=0 or expn<0: raise ValueError('reference_pcn > 0 and exponent >= 0 required.')
    if np.any(p<=0): raise ValueError('PCN must be > 0 for PCN-dependent loss.')
    if base==0: return np.zeros_like(p,dtype=float)
    return np.clip(base*np.power(ref/p,expn),0.0,max_loss)

def log2_score(pcn,g0,beta=None,loss_per_division=None,n0=1.0):
    beta=_resolve_beta(beta); loss=_validate_loss(_resolve_loss(loss_per_division))
    p=_validate_pcn(pcn,beta=beta); g=effective_doublings(p,g0,beta=beta)
    return np.log2(n0)+g+np.log2(p)+g*np.log2(1.0-loss)

def score_ratio(pcn_a,pcn_b,g0,beta=None,loss_a=None,loss_b=None):
    beta=_resolve_beta(beta)
    delta=log2_score(pcn_a,g0,beta=beta,loss_per_division=_resolve_loss(loss_a))-log2_score(pcn_b,g0,beta=beta,loss_per_division=_resolve_loss(loss_b))
    return 2.0**delta

def analytic_optimal_pcn(g0,beta=None,loss_per_division=None):
    beta=_resolve_beta(beta); loss=_validate_loss(_resolve_loss(loss_per_division)); g0=np.asarray(g0,dtype=float)
    if np.any(g0<=0): raise ValueError('g0 must be > 0.')
    d=np.log(2.0*(1.0-loss))
    g0, beta = np.broadcast_arrays(g0, np.asarray(beta, dtype=float))
    if np.any(~np.isfinite(beta)) or np.any(beta<=0): raise ValueError('beta must be finite and > 0.')
    if d<=0: return np.full(g0.shape,np.nan,dtype=float)
    return 1.0/(np.asarray(beta)*g0*d)

def monod_activity(substrate,ks):
    if ks<=0: raise ValueError('ks must be > 0.')
    s=np.maximum(np.asarray(substrate,dtype=float),0.0)
    return np.where(s>0,s/(ks+s),0.0)

def copy_setpoint(base_pcn,mu,mu_ref,gamma=None,max_fold=None,pcn_cap=None):
    if gamma is None: gamma=config.COPY_FEEDBACK_GAMMA
    if max_fold is None: max_fold=config.MAX_COPY_SETPOINT_FOLD
    if pcn_cap is None: pcn_cap=config.DYNAMIC_PCN_CAP
    if gamma<0: raise ValueError('gamma must be >= 0.')
    if max_fold<1: raise ValueError('max_fold must be >= 1.')
    base=np.asarray(base_pcn,dtype=float); mu=np.asarray(mu,dtype=float); mu_ref=np.asarray(mu_ref,dtype=float)
    ratio=mu_ref/np.maximum(mu,np.finfo(float).tiny)
    fold=np.minimum(np.power(ratio,gamma),max_fold)
    return np.clip(base*fold,0.0,pcn_cap)

def copy_relaxation_rate(current_pcn,setpoint_pcn,tau_h,activity):
    if tau_h<=0: raise ValueError('tau_h must be > 0.')
    return (np.asarray(setpoint_pcn)-np.asarray(current_pcn))/tau_h*activity

def copy_relaxation_step(current_pcn,setpoint_pcn,dt_h,tau_h,activity):
    if tau_h<=0 or dt_h<0: raise ValueError('tau_h > 0 and dt_h >= 0 required.')
    frac=1.0-np.exp(-np.asarray(activity)*dt_h/tau_h)
    return np.asarray(current_pcn)+frac*(np.asarray(setpoint_pcn)-np.asarray(current_pcn))

def expect_raises(fn,exc_type=Exception):
    try: fn()
    except exc_type: return True
    return False

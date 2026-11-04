"""Particle simulation of cell-to-cell copy-number heterogeneity.

Extracted from the notebook's "Single-cell PCN particle simulation" cell. Function bodies are unchanged
except that references to declared parameters now go through `config`, so the
notebook's Colab widgets stay authoritative at runtime.
"""
import warnings

import numpy as np
import pandas as pd

from . import config
from .analytic import (
    _resolve_beta,
    copy_relaxation_step,
    copy_setpoint,
    monod_activity,
)

def _lognormal_integer_sample(mean,cv,n,rng):
    if mean<=0: return np.zeros(n,dtype=int)
    if cv<0: raise ValueError('CV must be >= 0.')
    if cv==0: return np.repeat(int(round(mean)),n)
    sigma2=np.log(1+cv**2); sigma=np.sqrt(sigma2); mu=np.log(mean)-0.5*sigma2
    return np.maximum(np.rint(rng.lognormal(mu,sigma,n)).astype(int),0)

def simulate_single_cell_pcn(mean_pcn=None,n_cells=None,initial_cv=None,control_noise=None,dt_h=None,seed=None,beta=None,feedback_gamma=None,copy_relaxation_h=None,max_copy_setpoint_fold=None,pcn_cap=None,substrate_time=None,substrate_values=None):
    mean_pcn=config.SINGLE_CELL_MEAN_PCN if mean_pcn is None else mean_pcn; n_cells=config.SINGLE_CELL_N if n_cells is None else n_cells; initial_cv=config.SINGLE_CELL_INITIAL_CV if initial_cv is None else initial_cv; control_noise=config.SINGLE_CELL_CONTROL_NOISE if control_noise is None else control_noise
    dt_h=config.SINGLE_CELL_DT_H if dt_h is None else dt_h; seed=config.SINGLE_CELL_SEED if seed is None else seed; beta=_resolve_beta(beta); feedback_gamma=config.COPY_FEEDBACK_GAMMA if feedback_gamma is None else feedback_gamma; copy_relaxation_h=config.COPY_RELAXATION_H if copy_relaxation_h is None else copy_relaxation_h; max_copy_setpoint_fold=config.MAX_COPY_SETPOINT_FOLD if max_copy_setpoint_fold is None else max_copy_setpoint_fold; pcn_cap=config.DYNAMIC_PCN_CAP if pcn_cap is None else pcn_cap
    rng=np.random.default_rng(seed)
    if substrate_time is None or substrate_values is None:
        substrate_time=np.linspace(0,config.SHARED_HOURS,500); substrate_values=np.exp(-substrate_time/max(config.SHARED_HOURS/3,1e-9))
    substrate_time=np.asarray(substrate_time,float); substrate_values=np.asarray(substrate_values,float); t_grid=np.arange(substrate_time.min(),substrate_time.max()+0.5*dt_h,dt_h)
    base_C=_lognormal_integer_sample(mean_pcn,initial_cv,n_cells,rng); C=base_C.copy(); initial_C=C.copy(); mu_max=np.log(2)/config.REFERENCE_DOUBLING_TIME_H; s0=float(np.interp(t_grid[0],substrate_time,substrate_values)); mu_env0=mu_max*float(monod_activity(s0,config.MONOD_KS)); mu_ref_base=mu_env0*np.clip(1-beta*base_C,1e-12,1.0); records=[]
    for step,t in enumerate(t_grid):
        S=float(np.clip(np.interp(t,substrate_time,substrate_values),0,1)); ga=float(monod_activity(S,config.MONOD_KS)); ca=float(monod_activity(S,config.COPY_REPLICATION_KS)); mu_env=mu_max*ga; mu=mu_env*np.clip(1-beta*C,0,1)
        records.append({'time_h':t,'mean':float(np.mean(C)),'median':float(np.median(C)),'q10':float(np.quantile(C,0.10)),'q90':float(np.quantile(C,0.90)),'cv':float(np.std(C)/max(np.mean(C),1e-12)),'zero_fraction':float(np.mean(C==0)),'mean_growth_h':float(np.mean(mu))})
        if step==len(t_grid)-1: break
        C_ss=copy_setpoint(base_C,mu,mu_ref_base,gamma=feedback_gamma,max_fold=max_copy_setpoint_fold,pcn_cap=pcn_cap); C_ss[C==0]=0; C_cont=copy_relaxation_step(C,C_ss,dt_h,copy_relaxation_h,ca)
        sigma=control_noise*np.sqrt(dt_h)
        if sigma>0: C_cont*=np.exp(rng.normal(-0.5*sigma**2,sigma,size=len(C_cont)))
        C_cont=np.clip(C_cont,0,pcn_cap); p_div=1-np.exp(-np.maximum(mu,0)*dt_h); did=rng.random(len(C))<p_div; non=np.where(~did)[0]; div=np.where(did)[0]
        outC=[]; outB=[]; outM=[]
        if len(non): outC.append(np.rint(C_cont[non]).astype(int)); outB.append(base_C[non]); outM.append(mu_ref_base[non])
        if len(div):
            total=rng.poisson(np.maximum(2*C_cont[div],0)); d1=rng.binomial(total,0.5); d2=total-d1; outC.extend([d1,d2]); outB.extend([base_C[div],base_C[div]]); outM.extend([mu_ref_base[div],mu_ref_base[div]])
        C_pool=np.concatenate(outC).astype(int); B_pool=np.concatenate(outB).astype(int); M_pool=np.concatenate(outM).astype(float); B_pool[C_pool==0]=0; M_pool[C_pool==0]=0
        if len(C_pool)>n_cells:
            keep=rng.choice(len(C_pool),size=n_cells,replace=False); C=C_pool[keep]; base_C=B_pool[keep]; mu_ref_base=M_pool[keep]
        else: C=C_pool; base_C=B_pool; mu_ref_base=M_pool
        C=np.clip(C,0,pcn_cap).astype(int)
    return {'summary':pd.DataFrame(records),'initial_pcn':initial_C,'final_pcn':C.copy(),'final_base_pcn':base_C.copy(),'time_h':t_grid}

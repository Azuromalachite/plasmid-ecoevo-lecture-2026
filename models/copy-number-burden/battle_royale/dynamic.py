"""Copy-up over time: PCN is ramped rather than granted.

Extracted from the notebook's "Dynamic copy-up simulation" cell. Function bodies are unchanged
except that references to declared parameters now go through `config`, so the
notebook's Colab widgets stay authoritative at runtime.
"""
import warnings

import numpy as np

from . import config
from .analytic import (
    _resolve_loss,
    _validate_loss,
    _validate_pcn,
    log2_score,
    relative_growth,
)

def dynamic_copy_profile(
    g_axis,
    g0,
    c_early,
    c_target,
    switch_fraction,
    amp_rate_log2_per_ref_doubling=config.AMP_RATE_LOG2_PER_REF_DOUBLING,
):
    if not (0 <= switch_fraction <= 1):
        raise ValueError("switch_fraction must be in [0, 1].")
    if amp_rate_log2_per_ref_doubling < 0:
        raise ValueError("Amplification rate must be >= 0.")

    _validate_pcn([c_early, c_target])
    g_switch = switch_fraction * g0
    after = np.maximum(g_axis - g_switch, 0.0)

    c = c_early * 2.0 ** (amp_rate_log2_per_ref_doubling * after)
    c = np.minimum(c, c_target)
    c[g_axis <= g_switch] = c_early
    return c

def dynamic_log2_score(
    c_early,
    c_target,
    g0,
    switch_fraction,
    beta=config.BETA,
    loss_per_division=None,
    amp_rate_log2_per_ref_doubling=config.AMP_RATE_LOG2_PER_REF_DOUBLING,
    n_steps=4001,
):
    loss_per_division = _validate_loss(_resolve_loss(loss_per_division))
    g_axis = np.linspace(0, g0, n_steps)
    c_profile = dynamic_copy_profile(
        g_axis,
        g0,
        c_early,
        c_target,
        switch_fraction,
        amp_rate_log2_per_ref_doubling,
    )

    # Integrate actual host doublings across reference-growth opportunity.
    r_profile = relative_growth(c_profile, beta=beta)
    host_doublings = np.trapezoid(r_profile, g_axis)

    # Per-division plasmid loss compounds over completed carrier doublings.
    log2_retention = host_doublings * np.log2(1.0 - loss_per_division)

    c_end = c_profile[-1]
    score = host_doublings + np.log2(c_end) + log2_retention

    return {
        "log2_score": score,
        "host_doublings": host_doublings,
        "endpoint_pcn": c_end,
        "g_axis": g_axis,
        "pcn_profile": c_profile,
    }

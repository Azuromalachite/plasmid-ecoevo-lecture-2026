"""Every declared parameter of the Battle Royale model, in one place.

Extracted verbatim from the notebook's Configuration cell. Values here are the
defaults; at runtime the notebook overwrites the ten `# @param` ones with
whatever its Colab form widgets hold, because a widget needs its literal to
live in the notebook. So: edit here to change the default, edit the notebook to
change a run.

Nothing in this module is fitted except BETA, which comes from Rouches et al.
Everything else is declared, and the comments say which is which.
"""
import warnings

import numpy as np

if not hasattr(np, "trapezoid"):
    raise RuntimeError(
        f"Battle Royale needs NumPy >= 2.0 for np.trapezoid; found "
        f"{np.__version__}. Try: pip install -U 'numpy>=2.0'")

# -----------------------------
# LITERATURE-ANCHORED PARAMETERS
# -----------------------------
# Rouches et al. Fig. 4E fit: a = 0.065% ± 0.006% per plasmid copy.
# Decimal form:
BETA = 0.00065
BETA_SD_PUBLISHED = 0.00006

# Approximate range directly explored by the ColE1 library.
VALIDATED_PCN_MAX = 800

# -----------------------------
# DEFAULT SCENARIO PARAMETERS
# -----------------------------
REFERENCE_G0 = 10.0
LOW_PCN = 80
HIGH_PCN = 500

# Probability that a carrier lineage loses the plasmid per completed carrier doubling.
# Set to 0 for the baseline copy-number-only analysis.
LOSS_PER_DIVISION = 0.0
LOSS_SWEEP = "0.0,0.001,0.01"

# -----------------------------
# ADVANCED / FIXED DEFAULTS
# Edit these directly only when a specific sensitivity analysis needs them.
# -----------------------------
# DYNAMIC COPY-UP PARAMETERS
DYNAMIC_C_EARLY = 80
DYNAMIC_C_TARGET = 500

# log2(copy-number increase) attainable per one unit of reference growth opportunity.
# 1.0 means 80 -> 160 -> 320 -> 640 over ~3 reference-doubling units after activation.
AMP_RATE_LOG2_PER_REF_DOUBLING = 1.0

# SHARED-FLASK PARAMETERS
SHARED_HOURS = 12.0  # illustrative; official duration not specified
ARENA_TEAM_COUNT = 20
EQUAL_START_FRACTION = 1.0 / ARENA_TEAM_COUNT
REFERENCE_POOL_PCNS = np.repeat(100.0, ARENA_TEAM_COUNT - 1)
REFERENCE_POOL_LABEL = "Synthetic pUC/ColE1 reference pool: 19 competitors, each PCN 100"
FOCAL_FRACTION = EQUAL_START_FRACTION
FOCAL_FRACTION_LABEL = "focal fraction 1/20 = 0.05 (illustrative equal-cell inoculum)"
COMPARISON_ANCHOR_PCN = 100.0
REFERENCE_DOUBLING_TIME_H = 0.5
TOTAL_STARTING_CELLS = 1e6
CARRYING_CAPACITY = 1e9
MATCHED_G0 = np.log2(CARRYING_CAPACITY / TOTAL_STARTING_CELLS)
PLASMID_FREE_GROWTH_MULTIPLIER = 1.0

# pUC/ColE1-specific extension.
# Rouches' fitted per-copy burden used a 2,686-bp pUC19 reference. Length scaling
# below is therefore a sensitivity mechanism, not a re-fitted universal law.
PUC19_BP = 2686.0
PUC_DEFAULT_PLASMID_BP = PUC19_BP
PUC_CARGO_HALF_SAT_PCN = 100.0
PUC_DEFAULT_CARGO_MAX = 0.0  # fractional growth penalty approached at very high PCN
PUC_LOSS_REFERENCE_PCN = 100.0
PUC_LOSS_PCN_EXPONENT = 0.0  # 0 = constant loss; >0 makes low-PCN loss higher

# A fully synthetic 20-member engineered-pUC continuum used only for sensitivity.
SYNTHETIC_20_PCN = np.geomspace(20.0, VALIDATED_PCN_MAX, ARENA_TEAM_COUNT)

# MECHANISTIC RESOURCE + PCN FEEDBACK MODEL
# Comma-separated starting PCNs for the mechanistic shared-flask scenario.
MECHANISTIC_PCN_LIST = "50,100,200,500"

# Monod half-saturation constant for the NORMALIZED substrate S in [0,1].
# This is a scenario parameter, not a fitted LB constant.
MONOD_KS = 0.05

# Strength of positive growth-rate -> copy-number feedback.
# Default is deliberately conservative because no universal BL21/pUC fit exists.
# C_ss ~ C_ref * (mu_ref / mu)^gamma.
# Literature supports growth-rate dependence, but this gamma is phenomenological.
COPY_FEEDBACK_GAMMA = 0.25

# Relaxation timescale for copy number to approach its current set point.
COPY_RELAXATION_H = 1.0

# Explicit biological/sensitivity bound on growth-state-mediated copy-up.
MAX_COPY_SETPOINT_FOLD = 2.0

# DNA replication may remain possible at lower substrate than bulk population growth.
# Phenomenological rather than a fitted LB constant.
COPY_REPLICATION_KS = 0.005

# Maximum absolute PCN allowed in the feedback model.
DYNAMIC_PCN_CAP = 800

# SINGLE-CELL HETEROGENEITY MODEL
SINGLE_CELL_MEAN_PCN = 100
SINGLE_CELL_N = 10000

# Initial coefficient of variation of PCN.
# Illustrative: Jahn et al. motivates heterogeneity but does not define a universal CV.
SINGLE_CELL_INITIAL_CV = 0.30

# Multiplicative stochasticity in copy-number regulation per sqrt(hour).
SINGLE_CELL_CONTROL_NOISE = 0.15

SINGLE_CELL_DT_H = 0.10
SINGLE_CELL_SEED = 42

# EDITORIAL COMMUNICATION STYLE

def parse_pcn_list(value):
    """Parse a comma-separated PCN string into a float array."""
    items = [v.strip() for v in str(value).split(",") if v.strip()]
    if not items:
        raise ValueError("empty PCN list")
    return np.asarray([float(v) for v in items], dtype=float)


def parse_float_list(value):
    """Parse a comma-separated float string into a float array."""
    items = [v.strip() for v in str(value).split(",") if v.strip()]
    if not items:
        raise ValueError("empty float list")
    return np.asarray([float(v) for v in items], dtype=float)


MECHANISTIC_PCNS = parse_pcn_list(MECHANISTIC_PCN_LIST)
LOSS_SWEEP_VALUES = parse_float_list(LOSS_SWEEP)

#: Every uppercase name above, for the notebook to pull into its namespace.
NAMES = sorted(k for k, v in list(globals().items())
               if k.isupper() and not k.startswith("_"))

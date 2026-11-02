#!/usr/bin/env python3
"""Validate the plasmid invasion threshold against cases derived from it.

Claim under test: `claim.model.plasmid_invasion_threshold` in
`evidence/claims.yml`. In a resource-explicit, well-mixed continuous culture
with mass-action transfer and per-unit-time segregational loss, a rare
plasmid-bearing class increases when

    gamma * n_star  >  c * psi  +  tau

where n_star is the plasmid-free density at the plasmid-free equilibrium and
psi there equals the dilution rate D.

WHY THIS SCRIPT EXISTS (OF-1). The previous verification drew parameter sets
independently, discarded the ones that happened to land within 5% of the
threshold, and reported that the sign of the invasion expression predicted the
outcome in 59 of 59 of the rest. Parameters drawn that way land far from the
boundary almost surely, so the test could hardly have failed: it reported a
pass count for a question it never asked. `legacy_sampling_survey()` below
measures exactly how far away those cases sat, in the test's own terms.

What replaces it: cases are *constructed* at controlled signed distances from
the boundary. Everything except the transfer rate is fixed, the critical
transfer rate is solved for, and gamma is set to gamma_crit * (1 + eps) for a
ladder of signed eps. The predicted invasion eigenvalue is then exactly

    lambda_pred = eps * (c * D + tau)

so eps is a dimensionless, signed distance from the threshold with a known
consequence. The full nonlinear system is integrated and the realised
exponential rate of the plasmid-bearing class is measured and compared.

WHAT IS REPORTED. Not a pass count. The **sensitivity domain**: the range of
eps over which the prediction is recovered, and the two edges that bound it.
The lower edge is physical rather than numerical -- the eigenvalue describes
the limit of a vanishing plasmid-bearing class, so a finite inoculum P0
perturbs the resident state by order P0/n_star and the test cannot resolve a
distance from the boundary smaller than roughly that. The sweep therefore runs
over P0/n_star as well as eps, and the lower edge moves with it, which is the
evidence that it is the perturbation and not the integrator.

Integration is done with ln P as the state variable. P spans many orders of
magnitude and stays positive by construction; in linear P a solver's absolute
tolerance would set a floor far above the effects being measured.

Dependencies: NumPy, SciPy and SymPy. SymPy is required, not optional: a
symbolic check that silently skips itself when an import fails is a check that
reports clean on a domain it never entered.

Usage (from the repository root):
    uv run --no-project --with numpy --with scipy --with sympy \
        python models/invasion-threshold/check_invasion_threshold.py

Exit status is 1 if any part disagrees with the claim as stated.
"""

import sys

try:
    import numpy as np
    from scipy.integrate import solve_ivp
    import sympy as sp
except ImportError as exc:  # noqa: BLE001 - we want the name in the message
    sys.exit(f"needs numpy, scipy and sympy ({exc}). See the usage line above.")


# ---------------------------------------------------------------------------
# The model
# ---------------------------------------------------------------------------
# R  resource, ug/mL                N  plasmid-free cells, cells/mL
# P  plasmid-bearing cells, cells/mL
#
#   R' = D (R0 - R) - (1/Y) [ psi(R) N + (1-c) psi(R) P ]
#   N' = psi(R) N - D N - gamma N P + tau P
#   P' = (1-c) psi(R) P - D P + gamma N P - tau P
#
# with Monod growth psi(R) = psi_max R / (K + R). Transconjugants are assumed
# to transfer like donors and to carry the same cost, which is what lets the
# plasmid-bearing class be one variable.

PARAMS = dict(
    psi_max=0.7,   # 1/h
    K=0.25,        # ug/mL
    R0=100.0,      # ug/mL
    D=0.2,         # 1/h
    Y=5.0e6,       # cells per ug of resource
    c=0.05,        # fractional growth cost of carriage
    tau=1.0e-4,    # 1/h, segregational loss per unit time
)


def psi(R, p):
    return p["psi_max"] * R / (p["K"] + R)


def plasmid_free_equilibrium(p):
    """(R*, n*) where psi(R*) = D. Raises if the chemostat does not support it."""
    if p["D"] >= p["psi_max"]:
        raise ValueError("washout: D must be below psi_max")
    r_star = p["K"] * p["D"] / (p["psi_max"] - p["D"])
    if r_star >= p["R0"]:
        raise ValueError("washout: R0 must exceed R*")
    n_star = p["Y"] * (p["R0"] - r_star)
    return r_star, n_star


def gamma_critical(p):
    """The transfer rate at which the invasion eigenvalue is exactly zero."""
    _, n_star = plasmid_free_equilibrium(p)
    return (p["c"] * p["D"] + p["tau"]) / n_star


def predicted_eigenvalue(gamma, p):
    _, n_star = plasmid_free_equilibrium(p)
    return gamma * n_star - p["c"] * p["D"] - p["tau"]


def rhs_logP(t, y, gamma, p):
    """Right-hand side in (R, N, L) with L = ln P. Exact, not an approximation."""
    R, N, L = y
    P = np.exp(L)
    growth = psi(R, p)
    dR = p["D"] * (p["R0"] - R) - (growth * N + (1 - p["c"]) * growth * P) / p["Y"]
    dN = growth * N - p["D"] * N - gamma * N * P + p["tau"] * P
    dL = (1 - p["c"]) * growth - p["D"] + gamma * N - p["tau"]
    return [dR, dN, dL]


# ---------------------------------------------------------------------------
# 1. Symbolic: the eigenvalue is exact, not an approximation
# ---------------------------------------------------------------------------

def symbolic_check():
    """Derive the invasion eigenvalue rather than assert it.

    Two things are checked, and the second is the one that matters: the
    plasmid row of the Jacobian at the plasmid-free equilibrium has zeros off
    the diagonal, so the eigenvalue governing a rare plasmid-bearing class is
    that diagonal entry exactly -- no quasi-steady-state argument is involved.
    """
    R, N, P = sp.symbols("R N P", positive=True)
    psi_max, K, R0, D, Y, c, tau, g = sp.symbols(
        "psi_max K R0 D Y c tau gamma", positive=True)

    growth = psi_max * R / (K + R)
    dR = D * (R0 - R) - (growth * N + (1 - c) * growth * P) / Y
    dN = growth * N - D * N - g * N * P + tau * P
    dP = (1 - c) * growth * P - D * P + g * N * P - tau * P

    problems = []

    # (a) Conjugation and segregation move cells between classes and must
    #     cancel in the total-cell balance.
    cell_balance = sp.simplify(sp.expand(dN + dP))
    conj_seg_residual = sp.simplify(
        cell_balance - sp.simplify(growth * N + (1 - c) * growth * P - D * (N + P)))
    if conj_seg_residual != 0:
        problems.append(f"cell balance does not cancel transfer/segregation: "
                        f"residual {conj_seg_residual}")

    # (b) The plasmid-free equilibrium, and the Jacobian's plasmid row there.
    r_star = sp.solve(sp.Eq(growth, D), R)[0]
    n_star = Y * (R0 - r_star)
    at_pfe = {R: r_star, N: n_star, P: 0}

    off_diagonal = [sp.simplify(sp.diff(dP, v).subs(at_pfe)) for v in (R, N)]
    if any(entry != 0 for entry in off_diagonal):
        problems.append(f"plasmid row of the Jacobian is not upper triangular "
                        f"at the plasmid-free equilibrium: {off_diagonal}")

    eigenvalue = sp.simplify(sp.diff(dP, P).subs(at_pfe))
    claimed = sp.simplify(g * n_star - c * D - tau)
    if sp.simplify(eigenvalue - claimed) != 0:
        problems.append(f"eigenvalue {eigenvalue} != claimed {claimed}")

    print("1. Symbolic derivation")
    print(f"   R*            = {sp.simplify(r_star)}")
    print(f"   n*            = {sp.simplify(n_star)}")
    print(f"   Jacobian row  = [dP/dR, dP/dN] = {off_diagonal} at P = 0")
    print(f"   eigenvalue    = {sp.simplify(eigenvalue)}")
    print(f"   cell balance  : conjugation and segregation cancel exactly "
          f"(residual {conj_seg_residual})")
    print(f"   -> {'OK' if not problems else 'PROBLEM'}")
    return problems


# ---------------------------------------------------------------------------
# 2. Cases constructed at controlled distances from the boundary
# ---------------------------------------------------------------------------

def measure_rate(eps, p0_rel, p, t_end=400.0, fit_from=0.5):
    """Integrate and measure the realised exponential rate of ln P.

    Returns (lambda_pred, lambda_obs). The rate is taken over the second half
    of the window, after any transient in R and N and while the plasmid-bearing
    class is still a small perturbation.
    """
    r_star, n_star = plasmid_free_equilibrium(p)
    gamma = gamma_critical(p) * (1.0 + eps)
    lam_pred = predicted_eigenvalue(gamma, p)

    y0 = [r_star, n_star, np.log(p0_rel * n_star)]
    t_eval = np.linspace(0.0, t_end, 4001)
    sol = solve_ivp(rhs_logP, (0.0, t_end), y0, args=(gamma, p),
                    method="LSODA", rtol=1e-12, atol=1e-14, t_eval=t_eval)
    if not sol.success:
        raise RuntimeError(f"integration failed at eps={eps:g}: {sol.message}")

    mask = sol.t >= fit_from * t_end
    t, L = sol.t[mask], sol.y[2][mask]
    lam_obs = np.polyfit(t, L, 1)[0]
    return lam_pred, lam_obs


def boundary_ladder(p, p0_rel_values=(1e-4, 1e-6, 1e-8, 1e-10, 1e-12),
                    exponents=tuple(range(0, -16, -1))):
    """Sign agreement and rate error as a function of distance and inoculum."""
    print("\n2. Cases constructed at a known distance from the boundary")
    print("   eps = (gamma - gamma_crit)/gamma_crit, so lambda_pred = eps*(cD + tau)")
    print("   lower edge = smallest |eps| whose sign is still recovered\n")
    print(f"   {'P0/n*':>8} | {'smallest |eps| with':>19} | "
          f"{'rate error at':>14} | {'rate error at':>14}")
    print(f"   {'':>8} | {'correct sign':>19} | {'|eps| = 1e-2':>14} | "
          f"{'|eps| = 1':>14}")
    print("   " + "-" * 64)

    problems = []
    edges = {}
    for p0_rel in p0_rel_values:
        smallest_ok = None
        rate_err = {}
        for e in exponents:
            for sign in (+1.0, -1.0):
                eps = sign * 10.0 ** e
                lam_pred, lam_obs = measure_rate(eps, p0_rel, p)
                if np.sign(lam_obs) == np.sign(lam_pred):
                    smallest_ok = 10.0 ** e
                else:
                    # Once the sign is lost it stays lost as |eps| shrinks.
                    break
                if e in (-2, 0) and sign > 0:
                    rate_err[e] = abs(lam_obs - lam_pred) / abs(lam_pred)
            else:
                continue
            break
        edges[p0_rel] = smallest_ok
        print(f"   {p0_rel:8.0e} | {smallest_ok:19.0e} | "
              f"{rate_err.get(-2, float('nan')):14.2e} | "
              f"{rate_err.get(0, float('nan')):14.2e}")

    # The lower edge must track the perturbation size, not sit at a fixed
    # floor. A fixed floor would mean the integrator, not the physics, is the
    # limit -- and would make the domain an artefact of solver settings.
    resolved = [v for v in edges.values() if v is not None]
    if len(set(resolved)) == 1:
        problems.append("the lower edge does not move with the inoculum size; "
                        "the limit is the solver, not the linearisation")
    for p0_rel, edge in edges.items():
        if edge is not None and edge > 1e3 * p0_rel and edge > 1e-6:
            problems.append(f"at P0/n* = {p0_rel:g} the sign is only recovered "
                            f"for |eps| >= {edge:g}, far above the perturbation")

    # If the finest edge sits at the bottom of the ladder, the ladder is the
    # limit and the number below it is unmeasured. Reporting it as the system's
    # resolution would be reporting an instrument's floor as a result, which is
    # the class of defect this script exists to remove.
    floor = 10.0 ** min(exponents)
    bottomed_out = [k for k, v in edges.items() if v is not None and v <= floor]
    if bottomed_out:
        problems.append(
            f"the ladder bottoms out at |eps| = {floor:g} for P0/n* in "
            f"{[f'{k:g}' for k in bottomed_out]}; extend `exponents` before "
            f"quoting a resolution there")
    return problems, edges


def rate_agreement(p, p0_rel=1e-10):
    """Where the predicted rate, not just its sign, is recovered."""
    print("\n3. Upper edge: where the linear rate stops describing the system")
    print(f"   {'eps':>10} | {'lambda_pred (1/h)':>18} | "
          f"{'lambda_obs (1/h)':>18} | {'rel. error':>10}")
    print("   " + "-" * 66)
    worst_within_domain = 0.0
    problems = []
    for eps in (1e-6, 1e-4, 1e-2, 0.1, 1.0, 10.0, 100.0):
        lam_pred, lam_obs = measure_rate(eps, p0_rel, p)
        err = abs(lam_obs - lam_pred) / abs(lam_pred)
        print(f"   {eps:10.0e} | {lam_pred:18.6e} | {lam_obs:18.6e} | {err:10.2e}")
        if eps <= 1.0:
            worst_within_domain = max(worst_within_domain, err)
    if worst_within_domain > 1e-3:
        problems.append(f"rate error reaches {worst_within_domain:.2e} inside "
                        f"|eps| <= 1, where the linearisation is claimed to hold")
    print(f"\n   worst relative rate error for |eps| <= 1: "
          f"{worst_within_domain:.2e}")
    return problems, worst_within_domain


# ---------------------------------------------------------------------------
# 3. What the superseded test was actually measuring
# ---------------------------------------------------------------------------

def legacy_sampling_survey(p, n=2000, seed=20261102):
    """Reconstruct the independent-sampling design and report its eps.

    This does not re-run the old verdict; it measures the design. Each sample
    draws gamma log-uniformly over the range a plasmid study would consider,
    then reports |eps| -- how far the drawn case sits from the threshold the
    test claimed to be probing.
    """
    rng = np.random.default_rng(seed)
    g_crit = gamma_critical(p)
    gammas = 10.0 ** rng.uniform(-14.0, -9.0, size=n)
    eps = gammas / g_crit - 1.0
    abs_eps = np.abs(eps)

    within_5pct = np.mean(abs_eps <= 0.05)
    quantiles = np.quantile(abs_eps, [0.05, 0.5, 0.95])

    print("\n4. The design this replaces, measured in its own terms")
    print(f"   {n} transfer rates drawn log-uniformly over 1e-14 to 1e-9 mL/cell/h")
    print(f"   critical transfer rate here: {g_crit:.3e} mL/cell/h")
    print(f"   |eps| quantiles (5/50/95%): "
          f"{quantiles[0]:.3g}, {quantiles[1]:.3g}, {quantiles[2]:.3g}")
    print(f"   fraction landing inside the 5% band the old test discarded: "
          f"{within_5pct:.3%}")
    print(f"   fraction at |eps| > 10 (two or more orders from the boundary): "
          f"{np.mean(abs_eps > 10):.1%}")
    print("   -> a pass count over cases drawn this way reports almost nothing "
          "about\n      the boundary, which is what the expression is a claim "
          "about.")
    return quantiles, within_5pct


def main():
    p = dict(PARAMS)
    r_star, n_star = plasmid_free_equilibrium(p)
    print("Invasion threshold: gamma * n_star > c * psi + tau")
    print(f"Parameters: " + ", ".join(f"{k}={v:g}" for k, v in p.items()))
    print(f"R* = {r_star:.4g} ug/mL, n* = {n_star:.4g} cells/mL, "
          f"gamma_crit = {gamma_critical(p):.4g} mL/cell/h\n")

    problems = []
    problems += symbolic_check()
    ladder_problems, edges = boundary_ladder(p)
    problems += ladder_problems
    rate_problems, worst_err = rate_agreement(p)
    problems += rate_problems
    legacy_sampling_survey(p)

    finest = min(v for v in edges.values() if v is not None)
    print("\n5. Sensitivity domain")
    print(f"   sign of the expression recovered down to |eps| = {finest:.0e} "
          f"at the smallest inoculum tested")
    print(f"   predicted rate recovered to better than {worst_err:.0e} "
          f"relative for |eps| <= 1")
    print("   lower edge set by the finite inoculum, not the solver: it moves "
          "with P0/n*")
    print("   outside |eps| <= 1 the linearisation is not claimed to apply and "
          "the rate departs")

    if problems:
        print("\nPROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("\nno problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())

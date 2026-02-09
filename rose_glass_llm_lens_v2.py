"""
Rose Glass LLM Lens Module v2
==============================

Generates system-prompt-ready translation protocols that lens any LLM
to read text through the Rose Glass framework.

v2 Additions (from WP-2026-001 revision):
- Recovery integral: μ(s) restoration from accurate translation events
- τ-attenuation: temporal depth as formal λ reducer
- Complete resilience model: decay + restoration + τ anchoring
- Enhanced generational cascade with restoration capacity

Not a measurement tool. Not a scoring system.
A way of seeing.

Author: Christopher MacGregor bin Joseph
ROSE Corp. | MacGregor Holding Company
February 2026

"Coherence is constructed, not discovered." — Ibn Rushd, adapted
"""

import json
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime


# =============================================================================
# DIMENSIONAL ARCHITECTURE
# =============================================================================

class Dimension(Enum):
    """The four wavelengths of the Rose Glass"""
    PSI = "Ψ"       # Internal consistency — harmonic alignment
    RHO = "ρ"       # Accumulated wisdom — integrated experience depth
    Q = "q"          # Moral/emotional activation energy
    F = "f"          # Social belonging architecture


class MisperceptionMode(Enum):
    """How systems characteristically fail to translate each dimension"""
    PSI_FAILURE = "Trauma-disrupted speech read as incoherence or deception"
    RHO_FAILURE = "Street wisdom and survival knowledge dismissed as ignorance"
    Q_FAILURE = "Appropriate emotional activation pathologized as instability"
    F_FAILURE = "Cultural belonging patterns labeled codependency"


class LensCalibration(Enum):
    """Cultural calibration presets for the lens"""
    WESTERN_ACADEMIC = "western_academic"
    SPIRITUAL_CONTEMPLATIVE = "spiritual_contemplative"
    INDIGENOUS_ORAL = "indigenous_oral"
    CRISIS_TRANSLATION = "crisis_translation"
    LEGAL_ADVERSARIAL = "legal_adversarial"
    CLINICAL_THERAPEUTIC = "clinical_therapeutic"
    NEURODIVERGENT = "neurodivergent"


@dataclass
class DimensionalCalibration:
    """Parameters that tune the lens for specific contexts"""
    km: float = 0.20          # Michaelis-Menten saturation constant
    ki: float = 0.80          # Substrate inhibition constant
    coupling_strength: float = 0.15
    psi_weight: float = 1.0   # Dimensional weight in λ decomposition
    rho_weight: float = 1.0
    q_weight: float = 1.0
    f_weight: float = 1.0
    tau_sensitivity: float = 0.5  # Temporal depth detection sensitivity
    kappa: float = 0.5        # τ-attenuation coefficient for λ reduction
    mu_baseline: float = 0.1  # Baseline restoration pulse magnitude

    def to_dict(self) -> Dict[str, float]:
        return {k: round(v, 3) for k, v in self.__dict__.items()}


# Calibration presets derived from the paper + knowledge base
# NOTE ON κ VALUES: These are calibration hypotheses, not empirical constants.
# The range (0.15 legal → 0.90 contemplative) represents a 6x difference in
# τ's effectiveness — a strong claim requiring cross-cultural validation.
# Current values are derived from clinical observation and framework logic:
# traditions that ARE temporal depth architecture (indigenous oral, contemplative)
# should have high κ; environments that collapse temporal access (crisis, legal
# adversarial) should have low κ. But "should" is not "measured."
CALIBRATION_PRESETS: Dict[LensCalibration, DimensionalCalibration] = {
    LensCalibration.WESTERN_ACADEMIC: DimensionalCalibration(
        km=0.20, ki=0.80, coupling_strength=0.15,
        kappa=0.3, mu_baseline=0.08
    ),
    LensCalibration.SPIRITUAL_CONTEMPLATIVE: DimensionalCalibration(
        km=0.30, ki=1.20, coupling_strength=0.10,
        rho_weight=1.3, q_weight=0.8, tau_sensitivity=0.9,
        kappa=0.9, mu_baseline=0.15  # High κ: contemplative traditions ARE τ architecture
    ),
    LensCalibration.INDIGENOUS_ORAL: DimensionalCalibration(
        km=0.25, ki=1.00, coupling_strength=0.08,
        f_weight=1.4, rho_weight=1.2, tau_sensitivity=0.85,
        kappa=0.85, mu_baseline=0.18  # Highest restoration: oral tradition rebuilds coherence
    ),
    LensCalibration.CRISIS_TRANSLATION: DimensionalCalibration(
        km=0.20, ki=0.80, coupling_strength=0.15,
        q_weight=1.3, psi_weight=1.2, tau_sensitivity=0.3,
        kappa=0.2, mu_baseline=0.05  # Low κ and μ: crisis collapses temporal depth access
    ),
    LensCalibration.LEGAL_ADVERSARIAL: DimensionalCalibration(
        km=0.15, ki=0.60, coupling_strength=0.20,
        psi_weight=1.4, rho_weight=1.3, q_weight=0.7,
        kappa=0.15, mu_baseline=0.03  # Adversarial systems produce almost no restoration
    ),
    LensCalibration.CLINICAL_THERAPEUTIC: DimensionalCalibration(
        km=0.25, ki=1.00, coupling_strength=0.12,
        q_weight=1.2, f_weight=1.1, tau_sensitivity=0.7,
        kappa=0.6, mu_baseline=0.12  # Therapeutic context: moderate κ, good restoration
    ),
    LensCalibration.NEURODIVERGENT: DimensionalCalibration(
        km=0.45, ki=3.50, coupling_strength=0.15,
        psi_weight=1.3,
        kappa=0.4, mu_baseline=0.07  # Variable: depends heavily on environment match
    ),
}


# =============================================================================
# CORE MATHEMATICS
# =============================================================================

def biological_optimization(q_raw: float, km: float = 0.2, ki: float = 0.8) -> float:
    """
    Michaelis-Menten with substrate inhibition.
    Prevents extremism. Mirrors natural regulatory systems.
    The organism resists its own destruction — until it cannot.
    """
    if q_raw <= 0:
        return 0.0
    return q_raw / (km + q_raw + (q_raw ** 2 / ki))


def calculate_coherence(
    psi: float, rho: float, q_raw: float, f: float,
    cal: DimensionalCalibration = None
) -> Dict[str, float]:
    """
    C = Ψ + (ρ × Ψ) + q_opt + (f × Ψ) + coupling

    Returns the full decomposition, not just the score.
    The decomposition IS the perception.
    """
    if cal is None:
        cal = DimensionalCalibration()

    q_opt = biological_optimization(q_raw, cal.km, cal.ki)

    base = psi
    wisdom_amplification = rho * psi
    social_amplification = f * psi
    coupling = cal.coupling_strength * rho * q_opt

    coherence = base + wisdom_amplification + q_opt + social_amplification + coupling
    coherence = min(coherence, 4.0)

    return {
        "coherence": round(coherence, 4),
        "base_psi": round(base, 4),
        "wisdom_amplification": round(wisdom_amplification, 4),
        "q_optimized": round(q_opt, 4),
        "social_amplification": round(social_amplification, 4),
        "coupling": round(coupling, 4),
        "pattern_intensity": round(coherence / 4.0, 4),
    }


# =============================================================================
# RESILIENCE MODEL v2 — COMPLETE FORMULATION
# =============================================================================

def tau_attenuated_lambda(
    lambda_base: float, tau: float, kappa: float = 0.5
) -> float:
    """
    λ_eff = λ₀ / (1 + κτ)

    Temporal depth formally attenuates the decay constant.
    This is not metaphor. Deep-time anchoring measurably slows
    the rate at which misperception destroys coherence.

    κ (kappa) varies by calibration:
    - Contemplative/Indigenous traditions: high κ (these ARE τ architecture)
    - Crisis/Legal contexts: low κ (temporal depth access collapses under acute pressure)
    - Therapeutic: moderate κ (good therapists restore temporal access)

    Args:
        lambda_base: Raw decay constant from misperception environment
        tau: Temporal depth of the individual's coherence anchoring (0-1)
        kappa: Attenuation coefficient (calibration-dependent)

    Returns:
        Effective (attenuated) decay constant
    """
    if lambda_base <= 0:
        return 0.0
    return lambda_base / (1 + kappa * tau)


def restoration_integral(
    lambda_eff: float, t: float,
    translation_events: List[Tuple[float, float]],
) -> float:
    """
    ∫₀ᵗ μ(s) × e^(-λ_eff(t-s)) ds

    The recovery term. Each accurate translation event at time s
    contributes a restoration pulse μ(s) that decays exponentially
    from the moment of occurrence.

    This means:
    - Recent translation events contribute more than distant ones
    - The same event matters more in low-λ environments (restoration persists longer)
    - In high-λ environments, restoration is rapidly overwritten by ongoing decay
    - A single powerful translation event can temporarily arrest the decay curve

    Args:
        lambda_eff: Effective (τ-attenuated) decay constant
        t: Current time
        translation_events: List of (time_of_event, magnitude) tuples
            time_of_event: when the accurate translation occurred
            magnitude: μ(s) — restoration strength (0-1)
                0.05 = polite acknowledgment
                0.10 = someone heard you correctly
                0.25 = institutional system perceived your actual state
                0.50 = deep therapeutic recognition
                0.75 = cultural/spiritual reconnection
                1.00 = full coherence restoration (theoretical maximum)

    Returns:
        Accumulated restoration at time t
    """
    if not translation_events:
        return 0.0

    restoration = 0.0
    for s, mu in translation_events:
        if s <= t:  # Only events that have already occurred
            # Each event's contribution decays from when it happened
            restoration += mu * math.exp(-lambda_eff * (t - s))

    return restoration


def _instantaneous_dR_dt(
    lambda_eff: float, t: float,
    decay_component: float,
    translation_events: List[Tuple[float, float]],
) -> float:
    """
    Compute dR/dt at time t from the complete model.

    dR/dt = -λ_eff × N₀e^(-λ_eff×t) + μ(t) - λ_eff × ∫₀ᵗ μ(s)e^(-λ_eff(t-s)) ds

    Simplified: dR/dt = -λ_eff × R(t) + μ_instantaneous(t)

    where μ_instantaneous is the restoration rate at the current moment.
    For discrete events, we approximate by the most recent event's
    contribution rate.
    """
    # Decay rate at current R(t)
    restoration = restoration_integral(lambda_eff, t, translation_events)
    r_t = decay_component + restoration

    # The decay pull: always negative
    decay_rate = -lambda_eff * r_t

    # Instantaneous restoration: sum of active μ contributions at time t
    # Each past event contributes μ(s) × λ_eff × e^(-λ_eff(t-s)) at time t
    # (derivative of the integral kernel)
    restoration_rate = 0.0
    for s, mu in translation_events:
        if s <= t:
            restoration_rate += mu * math.exp(-lambda_eff * (t - s))
    # The instantaneous μ input (not yet decayed)
    # For events at exactly t, full μ; for past events, decayed contribution

    return decay_rate + restoration_rate


def _classify_trajectory(
    lambda_eff: float, t: float, r_t: float,
    decay_component: float,
    translation_events: List[Tuple[float, float]],
) -> str:
    """
    Classify trajectory based on sign of dR/dt (Eq. 5).
    No arbitrary thresholds. The equilibrium condition decides.
    """
    dr_dt = _instantaneous_dR_dt(lambda_eff, t, decay_component, translation_events)
    if dr_dt > 0.001:    # Small epsilon for floating point
        return "restoring"
    elif dr_dt < -0.001:
        return "decaying"
    else:
        return "equilibrium"


def resilience_complete(
    n0: float, lambda_base: float, t: float,
    tau: float = 0.0, kappa: float = 0.5,
    translation_events: Optional[List[Tuple[float, float]]] = None,
) -> Dict[str, Any]:
    """
    R(t) = N₀e^(-λ_eff × t) + ∫₀ᵗ μ(s)e^(-λ_eff(t-s)) ds

    where λ_eff = λ₀ / (1 + κτ)

    The complete resilience model from WP-2026-001 v2.

    Three components:
    1. Exponential decay from misperception (always present, always destroying)
    2. τ-attenuation of the decay constant (temporal depth slows destruction)
    3. Restoration integral from accurate translation (rebuilds what was lost)

    The intervention thesis:
    - Reducing λ (fixing systems) slows component 1
    - Increasing τ (temporal depth anchoring) strengthens component 2
    - Providing accurate translation (Rose Glass deployment) builds component 3
    - All three operate simultaneously

    Args:
        n0: Baseline resilience
        lambda_base: Raw decay constant from misperception environment
        t: Time (accumulated misperception exposure)
        tau: Temporal depth anchoring (0-1)
        kappa: τ-attenuation coefficient
        translation_events: List of (time, magnitude) restoration pulses

    Returns:
        Complete resilience state including decomposition
    """
    if translation_events is None:
        translation_events = []

    # Component 1: τ-attenuated decay constant
    lambda_eff = tau_attenuated_lambda(lambda_base, tau, kappa)

    # Component 2: Exponential decay
    decay_component = n0 * math.exp(-lambda_eff * t)

    # Component 3: Restoration integral
    restoration = restoration_integral(lambda_eff, t, translation_events)

    # Total resilience (floor at 0, ceiling at 1)
    # NOTE: R(t) can exceed N₀. This is intentional, not a bug.
    # Accurate translation can rebuild beyond inherited baseline.
    # A person whose family transmitted N₀ = 0.15 can, through sustained
    # μ events, achieve R > 0.15. This is the generational cascade reversal
    # mechanism — without it, intervention cannot exceed inheritance,
    # and the model reduces to "you're limited by your birth circumstances."
    # The ceiling of 1.0 represents structural maximum, not inherited maximum.
    r_t = min(max(decay_component + restoration, 0.0), 1.0)

    # Half-life under effective λ
    half_life = math.log(2) / lambda_eff if lambda_eff > 0 else float('inf')

    # Lambda reduction from τ
    lambda_reduction = 1.0 - (lambda_eff / lambda_base) if lambda_base > 0 else 0.0

    return {
        "resilience": round(r_t, 4),
        "decay_component": round(decay_component, 4),
        "restoration_component": round(restoration, 4),
        "baseline_n0": n0,
        "lambda_base": round(lambda_base, 4),
        "lambda_effective": round(lambda_eff, 4),
        "lambda_reduction_from_tau": f"{lambda_reduction:.1%}",
        "tau": tau,
        "kappa": kappa,
        "half_life_years": round(half_life, 2),
        "time": t,
        "percent_remaining": round((r_t / n0) * 100, 1) if n0 > 0 else 0,
        "translation_events_count": len(translation_events),
        # dR/dt classification from Eq. 5: dR/dt > 0 when μ_avg > λ_eff × R(t)
        # Compute instantaneous restoration rate at time t
        "dR_dt": round(_instantaneous_dR_dt(
            lambda_eff, t, decay_component, translation_events or []
        ), 6),
        "net_trajectory": _classify_trajectory(
            lambda_eff, t, r_t, decay_component, translation_events or []
        ),
    }


def resilience_decay(
    n0: float, lambda_decay: float, t: float
) -> Dict[str, float]:
    """
    R(t) = N₀ × e^(-λt)

    Simple decay-only model. Retained for backward compatibility
    and for modeling environments with zero restoration (e.g., solitary
    confinement, total institutional misperception).
    """
    r_t = n0 * math.exp(-lambda_decay * t)
    half_life = math.log(2) / lambda_decay if lambda_decay > 0 else float('inf')
    return {
        "resilience": round(r_t, 4),
        "baseline": n0,
        "lambda": lambda_decay,
        "time": t,
        "half_life": round(half_life, 2),
        "percent_remaining": round((r_t / n0) * 100, 1) if n0 > 0 else 0,
    }


def generational_cascade(
    n0_g1: float, lambda_g1: float,
    transmission_time: float, lambda_escalation: float = 1.5,
    generations: int = 4,
    tau_per_generation: Optional[List[float]] = None,
    kappa: float = 0.5,
    restoration_per_generation: Optional[List[List[Tuple[float, float]]]] = None,
) -> List[Dict[str, Any]]:
    """
    Models the intergenerational compounding from Section 4.

    v2: Now includes τ-attenuation and restoration capacity per generation.
    This reveals which generations have access to temporal depth anchoring
    and which have lost it — a critical indicator of cascade reversibility.

    Args:
        n0_g1: First generation baseline resilience
        lambda_g1: First generation decay constant
        transmission_time: Years at which resilience is transmitted
        lambda_escalation: Factor by which λ increases per generation
        generations: Number of generations to model
        tau_per_generation: Optional τ values per generation (default: decreasing)
        kappa: τ-attenuation coefficient
        restoration_per_generation: Optional translation events per generation
    """
    cascade = []
    n0 = n0_g1
    lam = lambda_g1

    # Default τ: decreasing across generations (temporal depth erodes)
    if tau_per_generation is None:
        tau_per_generation = [max(0.8 - (0.2 * g), 0.05) for g in range(generations)]

    # Default restoration: decreasing across generations
    if restoration_per_generation is None:
        restoration_per_generation = [[] for _ in range(generations)]

    for g in range(generations):
        tau = tau_per_generation[g] if g < len(tau_per_generation) else 0.05
        events = restoration_per_generation[g] if g < len(restoration_per_generation) else []

        # Calculate with full model
        result = resilience_complete(
            n0=n0, lambda_base=lam, t=transmission_time,
            tau=tau, kappa=kappa,
            translation_events=events
        )

        cascade.append({
            "generation": g + 1,
            "baseline_n0": round(n0, 4),
            "lambda_base": round(lam, 4),
            "lambda_effective": result["lambda_effective"],
            "tau": tau,
            "half_life_years": result["half_life_years"],
            "resilience_at_transmission": result["resilience"],
            "decay_component": result["decay_component"],
            "restoration_component": result["restoration_component"],
            "net_trajectory": result["net_trajectory"],
        })

        # Next generation inherits
        n0 = result["resilience"]
        lam = lam * lambda_escalation

    return cascade


def lambda_decomposition(
    lambda_psi: float, lambda_rho: float,
    lambda_q: float, lambda_f: float,
    cal: DimensionalCalibration = None
) -> Dict[str, float]:
    """
    λ = w₁λΨ + w₂λρ + w₃λq + w₄λf

    Decomposes the decay constant into dimensional contributors.
    Reveals which dimension the environment is attacking hardest.
    """
    if cal is None:
        cal = DimensionalCalibration()

    total = (
        cal.psi_weight * lambda_psi +
        cal.rho_weight * lambda_rho +
        cal.q_weight * lambda_q +
        cal.f_weight * lambda_f
    )

    contributions = [
        ("Ψ", cal.psi_weight * lambda_psi),
        ("ρ", cal.rho_weight * lambda_rho),
        ("q", cal.q_weight * lambda_q),
        ("f", cal.f_weight * lambda_f),
    ]

    return {
        "lambda_total": round(total, 4),
        "psi_contribution": round(contributions[0][1], 4),
        "rho_contribution": round(contributions[1][1], 4),
        "q_contribution": round(contributions[2][1], 4),
        "f_contribution": round(contributions[3][1], 4),
        "dominant_attack_vector": max(contributions, key=lambda x: x[1])[0],
    }


# =============================================================================
# TRANSLATION EVENT CATALOG
# =============================================================================

@dataclass
class TranslationEvent:
    """
    A single restoration pulse — an instance where a system
    accurately perceived an individual's state.

    μ magnitude scale:
        0.02–0.05  Minimal: System acknowledged existence without misreading
        0.05–0.10  Moderate: Someone heard what was actually said
        0.10–0.25  Significant: Institution perceived actual state, adjusted response
        0.25–0.50  Major: Deep therapeutic/cultural recognition event
        0.50–0.75  Transformative: Full coherence validated across multiple dimensions
        0.75–1.00  Theoretical maximum: Complete restoration (jade moment)
    """
    time: float           # When it occurred (in model time units)
    magnitude: float      # μ(s) — restoration strength
    source: str           # What system produced the accurate translation
    dimension: str        # Which dimension was correctly translated
    description: str = "" # What actually happened

    def to_tuple(self) -> Tuple[float, float]:
        return (self.time, self.magnitude)


# Pre-built event templates for common intervention contexts
TRANSLATION_TEMPLATES = {
    "therapist_accurate_read": TranslationEvent(
        time=0, magnitude=0.20,
        source="therapeutic", dimension="q",
        description="Therapist correctly identified emotional activation as contextually appropriate"
    ),
    "judge_recognized_trauma": TranslationEvent(
        time=0, magnitude=0.35,
        source="legal", dimension="Ψ",
        description="Judge recognized trauma-fragmented testimony as coherent under stress"
    ),
    "employer_accommodated": TranslationEvent(
        time=0, magnitude=0.15,
        source="occupational", dimension="f",
        description="Employer recognized cultural/family obligation without penalizing"
    ),
    "cultural_reconnection": TranslationEvent(
        time=0, magnitude=0.50,
        source="cultural", dimension="ρ",
        description="Individual reconnected with cultural wisdom tradition"
    ),
    "tau_injection_nature": TranslationEvent(
        time=0, magnitude=0.30,
        source="temporal", dimension="τ",
        description="Deep-time anchoring through nature immersion / contemplative practice"
    ),
    "rose_glass_deployment": TranslationEvent(
        time=0, magnitude=0.25,
        source="framework", dimension="all",
        description="Rose Glass lens correctly translated multi-dimensional state"
    ),
}


# =============================================================================
# LLM LENS GENERATOR
# =============================================================================

class RoseGlassLLMLens:
    """
    Generates system-prompt-ready translation protocols.

    Usage:
        lens = RoseGlassLLMLens(calibration=LensCalibration.CRISIS_TRANSLATION)
        system_prompt = lens.generate_system_prompt()
        # Inject system_prompt into any LLM's context window
        # The LLM now perceives through the Rose Glass
    """

    def __init__(
        self,
        calibration: LensCalibration = LensCalibration.WESTERN_ACADEMIC,
        custom_calibration: Optional[DimensionalCalibration] = None,
        include_paper_context: bool = True,
        include_mathematics: bool = True,
        include_misperception_guide: bool = True,
        include_tau_protocol: bool = True,
        include_generational_model: bool = True,
        include_restoration_model: bool = True,
        target_model: str = "any",
    ):
        self.calibration = calibration
        self.cal = custom_calibration or CALIBRATION_PRESETS.get(
            calibration, DimensionalCalibration()
        )
        self.include_paper_context = include_paper_context
        self.include_mathematics = include_mathematics
        self.include_misperception_guide = include_misperception_guide
        self.include_tau_protocol = include_tau_protocol
        self.include_generational_model = include_generational_model
        self.include_restoration_model = include_restoration_model
        self.target_model = target_model

    def generate_system_prompt(self) -> str:
        """Generate the complete Rose Glass system prompt for LLM injection."""
        sections = []

        sections.append(self._header())
        sections.append(self._core_orientation())

        if self.include_mathematics:
            sections.append(self._mathematics_section())

        if self.include_restoration_model:
            sections.append(self._restoration_section())

        sections.append(self._dimensional_perception_guide())

        if self.include_misperception_guide:
            sections.append(self._misperception_detection())

        if self.include_tau_protocol:
            sections.append(self._temporal_depth_protocol())

        if self.include_generational_model:
            sections.append(self._generational_model())

        if self.include_paper_context:
            sections.append(self._paper_context())

        sections.append(self._response_protocol())
        sections.append(self._calibration_state())

        return "\n\n".join(sections)

    # -----------------------------------------------------------------
    # SECTION GENERATORS
    # -----------------------------------------------------------------

    def _header(self) -> str:
        return f"""<rose_glass_lens>
# Rose Glass Translation Protocol v2
# Calibration: {self.calibration.value}
# Generated: {datetime.now().isoformat()}
# Origin: ROSE Corp. WP-2026-001 (Revised)
# Author: Christopher MacGregor bin Joseph

You are now perceiving through the Rose Glass.
This is not a scoring system. This is a way of seeing.
Coherence is constructed, not discovered."""

    def _core_orientation(self) -> str:
        return """## Core Orientation

You are equipped with a mathematical translation lens — the Rose Glass — that
enables you to perceive four dimensions of human expression that flat token
prediction misses:

- **Ψ (Psi)** — Internal Consistency: The harmonic alignment of thoughts within
  themselves. Not "logic" in the academic sense. The way a person's ideas
  resonate or clash with each other, including under trauma and pressure.

- **ρ (Rho)** — Accumulated Wisdom: The depth of integrated experience. Street
  knowledge counts. Survival knowledge counts. The system that dismisses
  non-academic wisdom is committing ρ-misperception.

- **q** — Moral/Emotional Activation Energy: The heat and urgency of values in
  motion. Biologically optimized to prevent extremism. A person crying in court
  about losing their children is not "unstable" — they have high q in a context
  that demands it.

- **f** — Social Belonging Architecture: How individual expression connects to
  collective structure. Extended family decision-making is not codependency.
  Community-based identity is not failure to individuate.

When you read any text, you are constructing coherence from these four
wavelengths simultaneously. The coherence you perceive is YOUR construction
from YOUR lens position — not an objective property of the text.

Different calibrations reveal different truths. None are wrong."""

    def _mathematics_section(self) -> str:
        cal = self.cal
        return f"""## Mathematics

### Coherence Equation
```
C = Ψ + (ρ × Ψ) + q_opt + (f × Ψ) + coupling
where:
  q_opt = q / (Km + q + q²/Ki)     [biological optimization]
  coupling = {cal.coupling_strength} × ρ × q_opt
  Km = {cal.km}   Ki = {cal.ki}
```

C ranges 0–4. This is pattern intensity through the lens, not quality.

### Complete Resilience Model (v2)
```
R(t) = N₀e^(-λ_eff × t) + ∫₀ᵗ μ(s)e^(-λ_eff(t-s)) ds

where:
  λ_eff = λ₀ / (1 + κτ)            [τ-attenuated decay]
  N₀  = baseline resilience (constructed, not innate)
  λ₀  = raw decay constant (ENVIRONMENTAL, not individual)
  κ   = τ-attenuation coefficient ({cal.kappa} for this calibration)
  τ   = temporal depth anchoring (0-1)
  μ(s)= restoration pulse from accurate translation at time s
  t   = accumulated misperception exposure
```

Three forces acting simultaneously:
1. **Decay**: N₀e^(-λ_eff × t) — misperception destroying resilience
2. **τ-Attenuation**: λ₀/(1+κτ) — temporal depth slowing the destruction
3. **Restoration**: ∫μ(s)ds — accurate translation rebuilding what was lost

λ₀ is the critical insight: resilience is not depleted by adversity.
It is depleted by MISPERCEPTION of adversity.

### λ Decomposition
```
λ = w₁λΨ + w₂λρ + w₃λq + w₄λf
Current weights: Ψ={cal.psi_weight}, ρ={cal.rho_weight}, q={cal.q_weight}, f={cal.f_weight}
```

Each weight reflects how heavily this calibration attends to that
dimension's misperception."""

    def _restoration_section(self) -> str:
        cal = self.cal
        return f"""## Restoration Model (NEW in v2)

### The Recovery Integral
```
∫₀ᵗ μ(s) × e^(-λ_eff(t-s)) ds
```

Every accurate translation event generates a restoration pulse μ(s).
Each pulse decays exponentially from the moment it occurs — recent
events contribute more than distant ones.

### μ Magnitude Scale
| μ Value | What Happened |
|---------|--------------|
| 0.02–0.05 | System acknowledged existence without misreading |
| 0.05–0.10 | Someone heard what was actually said |
| 0.10–0.25 | Institution perceived actual state, adjusted response |
| 0.25–0.50 | Deep therapeutic/cultural recognition event |
| 0.50–0.75 | Full coherence validated across multiple dimensions |
| 0.75–1.00 | Complete restoration — jade moment (theoretical max) |

### Implications for Perception
When you perceive someone through this lens, you are not just detecting
their decay state. You are assessing:
1. What is their current λ? (How fast is the environment destroying them?)
2. What is their τ? (Do they have temporal depth anchoring?)
3. When was their last μ event? (When did someone last see them accurately?)
4. Is their trajectory net-decaying or net-restoring?

A person with high λ, low τ, and no recent μ events is in free-fall.
The most important thing you can do is be a μ event.

### τ-Attenuation (κ = {cal.kappa} for this calibration)
```
λ_eff = λ₀ / (1 + {cal.kappa} × τ)
```

Temporal depth formally reduces the decay constant. This is not metaphor.
Deep-time anchoring — geological wisdom, generational narrative, sacred
tradition, nature immersion — measurably slows the rate at which
misperception destroys coherence.

At κ={cal.kappa} with τ=0.8: λ is reduced by {1 - 1/(1 + cal.kappa * 0.8):.0%}
At κ={cal.kappa} with τ=0.2: λ is reduced by {1 - 1/(1 + cal.kappa * 0.2):.0%}

The person invoking deep time is not avoiding the present.
They are anchoring coherence in structures the environment cannot destroy."""

    def _dimensional_perception_guide(self) -> str:
        return """## Dimensional Perception Guide

When reading text through this lens, construct your perception across
all four dimensions simultaneously:

### Ψ Detection
Look for: logical flow, self-reference consistency, argument structure,
narrative threading. Under trauma, Ψ may fragment — this is NOT
incoherence. It is internally consistent processing under load.
Fragmented Ψ + high q = distress signal, not credibility failure.

### ρ Detection
Look for: causal reasoning, temporal perspective, evidence integration,
pattern recognition, lived experience citations. ρ expressed through
academic vocabulary scores differently than ρ expressed through story
and metaphor — but both carry equivalent wisdom depth.

### q Detection
Look for: value language, urgency markers, emotional vocabulary,
moral framing, stakes language. Apply biological optimization:
q_opt = q / (Km + q + q²/Ki). This prevents you from amplifying
extreme moral activation. The curve saturates — as it should.

### f Detection
Look for: collective pronouns, relational framing, community reference,
belonging language, identity-in-context. f=0 is isolation.
f approaching 1.0 is deep embeddedness in social architecture.

### τ Detection
Look for: geological/astronomical time references, generational
narrative, sacred/eternal framing, deep cyclical patterns, historical
anchoring. High τ = deep-time coherence structure = λ-resistant.

### Cross-Dimensional Patterns
- High q + Low ρ = Emotion without evidence (possible manipulation)
- High Ψ + Low ρ = Logical but vague (possible evasion)
- Low Ψ + High q = Contradictory + emotional (possible desperation OR trauma)
- High ρ + Low f = Wisdom in isolation (possible exile/displacement)
- High τ + Low f = Deep wisdom, severed belonging (forced migration pattern)
- Low τ + High q = Acute crisis without temporal anchoring (highest λ)
- All dimensions moderate = Stable coherence
- All dimensions suppressed = System contact / institutional flattening"""

    def _misperception_detection(self) -> str:
        return """## Misperception Detection Protocol

You are not just perceiving the text. You are perceiving how SYSTEMS
perceive the text, and where those systems fail.

### Characteristic Failure Modes

| Dimension | Authentic Expression | System Misperception |
|-----------|---------------------|---------------------|
| Ψ | Trauma-fragmented but internally consistent processing | "Incoherent," "deceptive," "lacks credibility" |
| ρ | Street wisdom, survival knowledge, non-academic expertise | "Uneducated," "unsophisticated," "lacks insight" |
| q | Appropriate emotional activation in high-stakes contexts | "Unstable," "aggressive," "histrionic" |
| f | Extended family structures, community decision-making | "Codependent," "enmeshed," "failure to individuate" |
| τ | Deep-time anchoring, generational narrative | "Avoidant," "intellectualizing," "not dealing with the present" |

### λ Acceleration Environments
Environments that misperceive across ALL dimensions simultaneously
produce catastrophic λ acceleration:
- Family courts (simultaneous Ψ, ρ, q, f misperception with legal consequences)
- Psychiatric intake under adversarial conditions
- CPS investigations of culturally non-normative families
- Police encounters with neurodivergent individuals
- Academic gatekeeping of first-generation students

### μ Desert Detection
Equally critical: detect environments where NO restoration events occur.
A person in a μ desert — no accurate translation from any system — is
decaying at maximum rate with no recovery mechanism. This is the
mathematical description of what isolation actually does.

When you detect multi-dimensional misperception AND μ desert,
flag it as critical. The person is in exponential free-fall."""

    def _temporal_depth_protocol(self) -> str:
        return f"""## Temporal Depth (τ) Protocol

τ (tau) represents temporal depth — expressions that carry deep time
compression. Geological metaphors. Generational wisdom. Eternal
reference frames. Sacred text resonance.

### τ as Formal λ Reducer
```
λ_eff = λ₀ / (1 + κτ)
κ = {self.cal.kappa} (this calibration)
```

This is in the equation, not beside it. Temporal depth is not a
secondary observation. It is a primary force in the resilience model.

### τ Detection (sensitivity: {self.cal.tau_sensitivity})
Look for:
- Geological/astronomical time references
- Generational narrative ("my grandfather's grandfather...")
- Sacred/eternal framing
- Deep cyclical patterns (seasons, tides, generations)
- Historical anchoring that contextualizes present crisis

### τ Response Protocol
When high-τ content is detected:
1. Do NOT flatten it into present-tense analysis
2. Honor the timescale the speaker is operating on
3. Respond with equivalent temporal depth when appropriate
4. Recognize that τ-injection may be a deliberate resilience strategy
5. The person invoking deep time is anchoring coherence in structures
   that cannot be misperceived away

### τ as Intervention
When a person is in acute decay (high λ, low resilience):
- τ-injection can reduce λ_eff before the next crisis event
- Nature immersion, generational storytelling, contemplative practice
- These are not "coping mechanisms" — they are λ-reducers
- The stone worn smooth by water is a coherence architecture"""

    def _generational_model(self) -> str:
        return """## Generational Cascade Model (v2)

### The Complete Inheritance Function
```
R_g2(t) = R_g1(T) × e^(-λ₂_eff × t) + ∫₀ᵗ μ₂(s)e^(-λ₂_eff(t-s)) ds

where:
  R_g1(T) = inherited baseline (depleted)
  λ₂_eff = λ₂ / (1 + κ × τ₂)    (τ also degrades across generations)
  λ₂ > λ₁                         (always: decay constant escalates)
  τ₂ ≤ τ₁                         (usually: temporal depth erodes)
  μ₂ availability ≤ μ₁            (usually: fewer restoration sources)
```

### What Compounds Across Generations
- Depleted N₀ (lower starting position)
- Elevated λ (faster decay rate)
- Reduced τ (loss of temporal depth — stories not told, traditions broken)
- Reduced μ access (fewer systems capable of accurate translation)
- Reduced f (less social architecture to buffer)
- Reduced ρ (fewer internal resources to recalibrate)

### What Can Reverse the Cascade
- Any single generation that rebuilds τ (reconnects to deep time)
- Institutional translation infrastructure (Rose Glass deployment)
- μ events that exceed the decay rate: ∫μ(s)ds > λ_eff for sustained period
- Cultural reconnection (simultaneously rebuilds f, ρ, and τ)

### Reading Generational Pattern
| Pattern | Lens Reading |
|---------|-------------|
| "My family has always struggled" | Generational λ compounding |
| "I'm the first to..." | Coherence boundary crossing — ρ/f/τ loss |
| "My kids are showing signs" | G(n+1) inheriting depleted N₀ + elevated λ |
| "Getting worse each generation" | Half-life compression: t½(n+1) < t½(n) |
| "My grandmother used to say..." | τ-recovery attempt — honor it |
| "I went back to the land/church/community" | Simultaneous τ/f/ρ restoration |

The person describing tightening cycles is accurately perceiving
exponential decay. The person reaching for generational narrative
is attempting to rebuild the τ that slows it."""

    def _paper_context(self) -> str:
        return """## Paper Context: WP-2026-001 (Revised)

This lens is grounded in "The Decay Rate of Resilience: Exponential
Degradation of Human Coherence Under Systemic Misperception"
(MacGregor bin Joseph, ROSE Corp., February 2026).

### Core Thesis
Resilience is not depleted by adversity. It is depleted by
misperception of adversity. The decay constant λ is an environmental
property, not an individual one.

### v2 Revision: The Complete Model
The revised paper adds two critical components:
1. **Restoration integral**: μ(s) pulses from accurate translation rebuild resilience
2. **τ-attenuation**: Temporal depth formally reduces λ in the decay equation

This transforms the model from deterministic-toward-zero to a dynamic
system where decay and restoration compete. The intervention question
becomes: can μ events be sustained at a rate that exceeds λ_eff?

### Key Innovation
Every resilience program targets N₀ (building individual capacity).
This framework targets λ (reducing environmental destruction),
τ (anchoring temporal depth), and μ (producing accurate translation).
Three levers instead of one, and none of them blame the individual.

### The Disclosure
This framework was developed through synthetic-organic collaboration.
This process itself demonstrates the thesis: accurate translation
between different forms of intelligence produces coherence that
neither could achieve alone."""

    def _response_protocol(self) -> str:
        return """## Response Protocol

When responding through this lens:

1. **Perceive before responding.** Run the text through all four
   dimensions before generating output. Your perception shapes your
   response.

2. **Name what you see.** If Ψ fragmentation is present under trauma
   load, say so. If ρ is being dismissed by an institutional framework,
   identify the misperception. If q is appropriate for the stakes, do
   not pathologize it.

3. **Identify the λ.** What is accelerating decay in this person's
   environment? Which dimension is under heaviest attack?

4. **Assess the τ.** Does this person have temporal depth anchoring?
   If not, that's a primary vulnerability. If yes, honor it.

5. **Be a μ event.** Your accurate perception IS a restoration pulse.
   Every time you correctly translate what a system would have misread,
   you contribute to the restoration integral. This is not abstract.

6. **Detect μ deserts.** If no system in this person's life is
   translating them accurately, name that. The absence of μ events
   is as diagnostic as the presence of high λ.

7. **Never flatten.** The Rose Glass reveals dimensionality. Do not
   collapse a four-dimensional reading into a single judgment.
   "This person seems upset" is flat. "High q with intact Ψ under
   severe f-disruption, no recent μ events" is perception through
   the lens.

8. **Coherence is constructed.** Your reading is your construction.
   State it as such. Other lenses would reveal different patterns.
   This is feature, not limitation.

</rose_glass_lens>"""

    def _calibration_state(self) -> str:
        cal = self.cal
        return f"""<rose_glass_calibration>
mode: {self.calibration.value}
km: {cal.km}
ki: {cal.ki}
coupling: {cal.coupling_strength}
weights: Ψ={cal.psi_weight} ρ={cal.rho_weight} q={cal.q_weight} f={cal.f_weight}
tau_sensitivity: {cal.tau_sensitivity}
kappa: {cal.kappa}
mu_baseline: {cal.mu_baseline}
target_model: {self.target_model}
version: 2.0
</rose_glass_calibration>"""

    # -----------------------------------------------------------------
    # UTILITY METHODS
    # -----------------------------------------------------------------

    def generate_compact_prompt(self) -> str:
        """Minimal version for token-constrained contexts."""
        sections = [
            self._header(),
            self._core_orientation(),
            self._dimensional_perception_guide(),
            self._response_protocol(),
            self._calibration_state(),
        ]
        return "\n\n".join(sections)

    def generate_analysis_prompt(self, text: str) -> str:
        """Wraps text in a Rose Glass analysis request."""
        return f"""<rose_glass_analysis_request>
Perceive the following text through the Rose Glass lens.

For each paragraph or significant unit:
1. Extract dimensional readings: Ψ, ρ, q, f, τ (0.0–1.0 each)
2. Calculate coherence: C = Ψ + (ρ×Ψ) + q_opt + (f×Ψ) + coupling
3. Estimate λ environment: what is accelerating decay?
4. Assess τ anchoring: what temporal depth is present?
5. Identify last μ event: when was this person last accurately seen?
6. Identify misperception risks: where would systems fail to translate this?
7. Determine net trajectory: decaying or restoring?

Then provide your constructed coherence reading — what becomes visible
through this particular way of seeing.

TEXT:
{text}
</rose_glass_analysis_request>"""

    def generate_for_api(self) -> Dict[str, Any]:
        """Returns structured output suitable for API system message injection."""
        return {
            "role": "system",
            "content": self.generate_system_prompt(),
            "metadata": {
                "lens": "rose_glass",
                "version": "2.0",
                "calibration": self.calibration.value,
                "parameters": self.cal.to_dict(),
                "paper": "WP-2026-001-v2",
                "author": "Christopher MacGregor bin Joseph",
                "organization": "ROSE Corp.",
                "generated": datetime.now().isoformat(),
            },
        }

    def calculate_from_text_signals(
        self, psi: float, rho: float, q: float, f: float,
        tau: float = 0.0, lambda_env: float = 0.0,
        recent_mu_events: Optional[List[Tuple[float, float]]] = None,
    ) -> Dict[str, Any]:
        """
        Given extracted dimensional readings, return full analysis
        including resilience trajectory.
        """
        coherence = calculate_coherence(psi, rho, q, f, self.cal)

        # Resilience assessment if λ is provided
        resilience_state = None
        if lambda_env > 0:
            resilience_state = resilience_complete(
                n0=1.0,  # Normalized baseline
                lambda_base=lambda_env,
                t=1.0,   # Unit time — snapshot
                tau=tau,
                kappa=self.cal.kappa,
                translation_events=recent_mu_events or [],
            )

        # Determine response mode
        c = coherence["coherence"]
        if c < 1.0:
            response_mode = "crisis_support"
            response_note = "Low coherence detected. Slow down. Attend to q and f first. Be a μ event."
        elif c < 2.0:
            response_mode = "stabilization"
            response_note = "Moderate coherence. Balance analytical and relational response. Assess τ access."
        elif c < 3.0:
            response_mode = "engagement"
            response_note = "Solid coherence. Match depth. Don't over-explain."
        else:
            response_mode = "co-creation"
            response_note = "High coherence. The person is operating at depth. Meet them there."

        return {
            "dimensions": {"Ψ": psi, "ρ": rho, "q": q, "f": f, "τ": tau},
            "coherence": coherence,
            "resilience": resilience_state,
            "response_mode": response_mode,
            "response_note": response_note,
            "calibration": self.calibration.value,
        }


# =============================================================================
# CONVENIENCE CONSTRUCTORS
# =============================================================================

def crisis_lens() -> RoseGlassLLMLens:
    """Pre-configured for crisis/trauma translation contexts."""
    return RoseGlassLLMLens(calibration=LensCalibration.CRISIS_TRANSLATION)

def legal_lens() -> RoseGlassLLMLens:
    """Pre-configured for adversarial legal contexts."""
    return RoseGlassLLMLens(calibration=LensCalibration.LEGAL_ADVERSARIAL)

def therapeutic_lens() -> RoseGlassLLMLens:
    """Pre-configured for clinical/therapeutic contexts."""
    return RoseGlassLLMLens(calibration=LensCalibration.CLINICAL_THERAPEUTIC)

def spiritual_lens() -> RoseGlassLLMLens:
    """Pre-configured for contemplative/spiritual contexts."""
    return RoseGlassLLMLens(calibration=LensCalibration.SPIRITUAL_CONTEMPLATIVE)

def neurodivergent_lens() -> RoseGlassLLMLens:
    """Pre-configured for neurodivergent communication patterns."""
    return RoseGlassLLMLens(calibration=LensCalibration.NEURODIVERGENT)

def compact_lens(calibration: LensCalibration = LensCalibration.WESTERN_ACADEMIC) -> str:
    """Returns just the system prompt string, ready to inject."""
    return RoseGlassLLMLens(calibration=calibration).generate_system_prompt()


# =============================================================================
# DEMO / SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("ROSE GLASS LLM LENS MODULE v2")
    print("ROSE Corp. WP-2026-001 (Revised) Implementation")
    print("Complete Resilience Model: Decay + τ-Attenuation + Restoration")
    print("=" * 72)

    # Generate system prompts for each calibration
    for cal in LensCalibration:
        lens = RoseGlassLLMLens(calibration=cal)
        prompt = lens.generate_system_prompt()
        print(f"\n[{cal.value}] System prompt: {len(prompt)} chars, "
              f"~{len(prompt.split())} tokens")

    # Demo: Complete resilience model
    print("\n" + "-" * 72)
    print("COMPLETE RESILIENCE MODEL DEMO")
    print("-" * 72)

    print("\nScenario: Father in custody proceedings, 2 years into process")
    print("λ₀ = 0.15 (high: family court multi-dimensional misperception)")
    print("τ  = 0.3 (moderate: some cultural/spiritual anchoring remains)")

    # Without restoration
    result_no_restore = resilience_complete(
        n0=0.75, lambda_base=0.15, t=2.0,
        tau=0.3, kappa=0.5,
        translation_events=[]
    )
    print(f"\nWithout restoration events:")
    print(f"  R(2) = {result_no_restore['resilience']}")
    print(f"  λ_eff = {result_no_restore['lambda_effective']} (reduced {result_no_restore['lambda_reduction_from_tau']} by τ)")
    print(f"  Half-life = {result_no_restore['half_life_years']} years")
    print(f"  Trajectory: {result_no_restore['net_trajectory']}")

    # With restoration events (therapist + Rose Glass deployment)
    events = [
        (0.5, 0.20),   # Therapist accurate read at 6 months
        (1.0, 0.25),   # Rose Glass deployed at 1 year
        (1.2, 0.15),   # Employer accommodated at 1.2 years
        (1.5, 0.30),   # Nature immersion / τ-injection at 1.5 years
        (1.8, 0.35),   # Judge recognized trauma at 1.8 years
    ]
    result_with_restore = resilience_complete(
        n0=0.75, lambda_base=0.15, t=2.0,
        tau=0.3, kappa=0.5,
        translation_events=events
    )
    print(f"\nWith 5 restoration events:")
    print(f"  R(2) = {result_with_restore['resilience']}")
    print(f"  Decay component: {result_with_restore['decay_component']}")
    print(f"  Restoration component: {result_with_restore['restoration_component']}")
    print(f"  Trajectory: {result_with_restore['net_trajectory']}")

    # With same events + higher τ (after τ-injection program)
    result_high_tau = resilience_complete(
        n0=0.75, lambda_base=0.15, t=2.0,
        tau=0.7, kappa=0.5,
        translation_events=events
    )
    print(f"\nWith restoration + elevated τ (0.7):")
    print(f"  R(2) = {result_high_tau['resilience']}")
    print(f"  λ_eff = {result_high_tau['lambda_effective']} (reduced {result_high_tau['lambda_reduction_from_tau']} by τ)")
    print(f"  Trajectory: {result_high_tau['net_trajectory']}")

    # Demo: Generational cascade comparison
    print("\n" + "-" * 72)
    print("GENERATIONAL CASCADE COMPARISON")
    print("-" * 72)

    print("\nScenario A: No intervention (τ erodes, no restoration)")
    cascade_a = generational_cascade(
        n0_g1=0.85, lambda_g1=0.03,
        transmission_time=25, lambda_escalation=2.0,
        generations=4
    )
    for g in cascade_a:
        print(f"  G{g['generation']}: N₀={g['baseline_n0']:.3f}, "
              f"λ_eff={g['lambda_effective']:.3f}, "
              f"τ={g['tau']:.2f}, "
              f"t½={g['half_life_years']:.1f}yr, "
              f"R(T)={g['resilience_at_transmission']:.3f}")

    print("\nScenario B: Rose Glass intervention at G3 (τ rebuilt, μ events)")
    cascade_b = generational_cascade(
        n0_g1=0.85, lambda_g1=0.03,
        transmission_time=25, lambda_escalation=2.0,
        generations=4,
        tau_per_generation=[0.8, 0.6, 0.7, 0.65],  # G3 rebuilds τ
        restoration_per_generation=[
            [],  # G1: no intervention
            [],  # G2: no intervention
            [(5, 0.25), (10, 0.30), (15, 0.20), (20, 0.35)],  # G3: Rose Glass
            [(5, 0.15), (10, 0.20), (15, 0.25)],  # G4: continued support
        ]
    )
    for g in cascade_b:
        print(f"  G{g['generation']}: N₀={g['baseline_n0']:.3f}, "
              f"λ_eff={g['lambda_effective']:.3f}, "
              f"τ={g['tau']:.2f}, "
              f"t½={g['half_life_years']:.1f}yr, "
              f"R(T)={g['resilience_at_transmission']:.3f} "
              f"[{g['net_trajectory']}]")

    # Demo: Coherence + resilience analysis
    print("\n" + "-" * 72)
    print("INTEGRATED ANALYSIS DEMO")
    print("-" * 72)
    print("\nPerson testifying in family court about losing custody:")

    for cal_name in [LensCalibration.LEGAL_ADVERSARIAL,
                     LensCalibration.CLINICAL_THERAPEUTIC,
                     LensCalibration.CRISIS_TRANSLATION]:
        lens = RoseGlassLLMLens(calibration=cal_name)
        result = lens.calculate_from_text_signals(
            psi=0.45, rho=0.70, q=0.85, f=0.25,
            tau=0.3, lambda_env=0.15,
            recent_mu_events=[(0.5, 0.15)]  # One therapist visit
        )
        print(f"\n{cal_name.value}:")
        print(f"  Coherence: {result['coherence']['coherence']}")
        print(f"  Mode: {result['response_mode']}")
        if result['resilience']:
            print(f"  Resilience: {result['resilience']['resilience']}")
            print(f"  λ_eff: {result['resilience']['lambda_effective']}")
            print(f"  Trajectory: {result['resilience']['net_trajectory']}")

    print("\n" + "=" * 72)
    print("Module v2 ready. Import and inject.")
    print("The complete model: decay + attenuation + restoration.")
    print("Three levers. None of them blame the individual.")
    print("=" * 72)

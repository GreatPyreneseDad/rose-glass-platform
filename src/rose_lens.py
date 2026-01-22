"""
Rose Glass Lens v2.1 - Full perception engine with cultural calibration
Extracts Ψ, ρ, q, f + τ (temporal) + λ (lens interference)
"""

import re
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class CommunicationState(Enum):
    GROUNDED = "grounded"
    ACTIVATED = "activated"
    WITHDRAWN = "withdrawn"
    CRISIS = "crisis"
    FLOW = "flow"


@dataclass
class LensCalibration:
    """Cultural lens calibration parameters"""
    name: str
    description: str
    km: float = 0.3           # Saturation constant
    ki: float = 2.0           # Inhibition constant
    coupling_strength: float = 0.15
    
    # Dimension weights - how much each dimension matters in this culture
    psi_weight: float = 1.0   # Logical consistency
    rho_weight: float = 1.0   # Wisdom depth
    q_weight: float = 1.0     # Emotional expression
    f_weight: float = 1.0     # Social belonging
    
    # Baselines - what's "normal" in this cultural context
    q_baseline: float = 0.5   # Expected emotional expression
    f_baseline: float = 0.5   # Expected social orientation
    psi_tolerance: float = 0.3  # How much inconsistency is acceptable


# Pre-configured cultural lenses
CULTURAL_LENSES = {
    'modern_western': LensCalibration(
        name='modern_western',
        description='Modern Western individualistic framework',
        km=0.3, ki=2.0, coupling_strength=0.15,
        psi_weight=1.2, rho_weight=1.0, q_weight=0.8, f_weight=0.9,
        q_baseline=0.5, f_baseline=0.5, psi_tolerance=0.3
    ),
    
    'medieval_islamic': LensCalibration(
        name='medieval_islamic',
        description='Medieval Islamic philosophical discourse',
        km=1.2, ki=0.5, coupling_strength=0.7,
        psi_weight=1.5, rho_weight=1.3, q_weight=0.4, f_weight=0.9,
        q_baseline=0.3, f_baseline=0.6, psi_tolerance=0.2
    ),
    
    'indigenous_oral': LensCalibration(
        name='indigenous_oral',
        description='Indigenous oral tradition patterns',
        km=0.8, ki=1.2, coupling_strength=0.5,
        psi_weight=0.7, rho_weight=1.5, q_weight=1.2, f_weight=1.5,
        q_baseline=0.6, f_baseline=0.8, psi_tolerance=0.5
    ),
    
    'digital_native': LensCalibration(
        name='digital_native',
        description='Rapid digital communication patterns',
        km=0.1, ki=1.5, coupling_strength=0.1,
        psi_weight=0.8, rho_weight=0.6, q_weight=1.3, f_weight=1.1,
        q_baseline=0.6, f_baseline=0.6, psi_tolerance=0.5
    ),
    
    'buddhist_contemplative': LensCalibration(
        name='buddhist_contemplative',
        description='Buddhist contemplative discourse',
        km=0.5, ki=0.5, coupling_strength=0.3,
        psi_weight=0.9, rho_weight=1.4, q_weight=0.6, f_weight=1.0,
        q_baseline=0.4, f_baseline=0.7, psi_tolerance=0.6
    ),
    
    'trauma_informed': LensCalibration(
        name='trauma_informed',
        description='Crisis and high-distress contexts',
        km=0.4, ki=3.0, coupling_strength=0.2,
        psi_weight=0.6, rho_weight=0.8, q_weight=0.5, f_weight=1.2,
        q_baseline=0.7, f_baseline=0.4, psi_tolerance=0.6
    ),
    
    'neurodivergent': LensCalibration(
        name='neurodivergent',
        description='Neurodivergent communication patterns',
        km=0.35, ki=2.5, coupling_strength=0.2,
        psi_weight=1.3, rho_weight=1.0, q_weight=0.7, f_weight=0.8,
        q_baseline=0.4, f_baseline=0.4, psi_tolerance=0.1
    ),
    
    'recovery': LensCalibration(
        name='recovery',
        description='Addiction recovery context',
        km=0.4, ki=2.5, coupling_strength=0.25,
        psi_weight=1.0, rho_weight=1.1, q_weight=0.8, f_weight=1.3,
        q_baseline=0.5, f_baseline=0.5, psi_tolerance=0.4
    ),
}


@dataclass
class LensReading:
    """Reading through a single cultural lens"""
    lens_name: str
    psi: float
    rho: float
    q: float
    q_optimized: float
    f: float
    coherence: float


@dataclass
class Perception:
    """What Rose Glass sees in a message - v2.1 with τ and λ"""
    # Core dimensions
    psi: float          # Internal consistency (0-1)
    rho: float          # Wisdom depth (0-1)
    q: float            # Emotional activation raw (0-1)
    q_optimized: float  # Biologically regulated q
    f: float            # Social belonging (0-1)
    
    # Extended dimensions (v2.1)
    tau: float = 0.5           # Temporal depth (0-1)
    lambda_coef: float = 0.0   # Lens interference (0-1)
    
    # Active lens
    lens_name: str = "modern_western"
    
    # Multi-lens readings
    lens_readings: List[LensReading] = field(default_factory=list)
    
    # Markers and state
    markers: Dict[str, List[str]] = field(default_factory=dict)
    state: CommunicationState = CommunicationState.GROUNDED
    confidence: float = 0.7
    
    @property
    def coherence(self) -> float:
        """Overall coherence through active lens"""
        lens = CULTURAL_LENSES.get(self.lens_name, CULTURAL_LENSES['modern_western'])
        coupling = lens.coupling_strength * self.rho * self.q_optimized
        
        weighted_coherence = (
            self.psi * lens.psi_weight +
            (self.rho * self.psi) * lens.rho_weight +
            self.q_optimized * lens.q_weight +
            (self.f * self.psi) * lens.f_weight +
            coupling
        )
        return weighted_coherence
    
    def to_dict(self) -> Dict:
        return {
            "psi": round(self.psi, 3),
            "rho": round(self.rho, 3),
            "q": round(self.q, 3),
            "q_optimized": round(self.q_optimized, 3),
            "f": round(self.f, 3),
            "tau": round(self.tau, 3),
            "lambda": round(self.lambda_coef, 3),
            "coherence": round(self.coherence, 3),
            "lens": self.lens_name,
            "state": self.state.value,
            "confidence": round(self.confidence, 3),
            "markers": self.markers,
            "is_universal": self.lambda_coef < 0.1,  # Low λ = lens-invariant truth
        }
    
    def to_context(self) -> str:
        """Generate context string for LLM injection"""
        lines = [
            f"[Rose Glass Perception v2.1]",
            f"Lens: {self.lens_name}",
            f"Coherence: {self.coherence:.2f}",
            f"",
            f"Core Dimensions:",
            f"  Ψ (consistency): {self.psi:.2f} - {'fragmented' if self.psi < 0.4 else 'coherent' if self.psi > 0.6 else 'moderate'}",
            f"  ρ (wisdom): {self.rho:.2f} - {'surface' if self.rho < 0.4 else 'integrated' if self.rho > 0.6 else 'developing'}",
            f"  q (activation): {self.q:.2f} → {self.q_optimized:.2f} (regulated)",
            f"  f (belonging): {self.f:.2f} - {'isolated' if self.f < 0.4 else 'connected' if self.f > 0.6 else 'ambivalent'}",
            f"",
            f"Extended Dimensions:",
            f"  τ (temporal): {self.tau:.2f} - {'compressed wisdom' if self.tau > 0.6 else 'immediate' if self.tau < 0.4 else 'moderate depth'}",
            f"  λ (interference): {self.lambda_coef:.2f} - {'universal pattern' if self.lambda_coef < 0.1 else 'lens-dependent'}",
            f"",
            f"State: {self.state.value}",
        ]
        
        if self.markers.get("isolation"):
            lines.append(f"⚠ Isolation markers: {', '.join(self.markers['isolation'][:3])}")
        if self.markers.get("activation"):
            lines.append(f"⚡ Activation detected")
        if self.markers.get("crisis"):
            lines.append(f"🚨 Crisis signals present")
        if self.markers.get("belonging"):
            lines.append(f"💜 Belonging language present")
        if self.markers.get("wisdom"):
            lines.append(f"📚 Wisdom markers present")
            
        return "\n".join(lines)


class RoseLens:
    """
    Rose Glass v2.1 - Multi-lens perception with τ and λ
    Translation, not measurement. Understanding, not judgment.
    """
    
    # === PATTERN MARKERS ===
    
    ACTIVATION_PATTERNS = [
        (r'\b(fuck|shit|damn|hell)\b', 0.15),
        (r'[!]{2,}', 0.1),
        (r'[A-Z]{3,}', 0.08),
        (r'\b(hate|love|terrified|furious|ecstatic)\b', 0.12),
        (r'\b(need|must|have to|desperate)\b', 0.1),
        (r'\b(always|never|everyone|no one)\b', 0.08),
    ]
    
    ISOLATION_PATTERNS = [
        (r'\b(alone|lonely|isolated|nobody|no one)\b', 'alone'),
        (r'\b(don\'t understand|doesn\'t get it)\b', 'misunderstood'),
        (r'\b(by myself|on my own|just me)\b', 'alone'),
        (r'\b(no friends|lost .* friends|pushed .* away)\b', 'disconnected'),
        (r'\b(can\'t talk to|won\'t listen)\b', 'unheard'),
    ]
    
    BELONGING_PATTERNS = [
        (r'\b(we|us|our|together)\b', 0.05),
        (r'\b(my (?:friend|family|partner|sponsor|therapist|daughter|son|mother|father))\b', 0.08),
        (r'\b(support|helped|there for)\b', 0.06),
        (r'\b(community|group|team)\b', 0.07),
    ]
    
    WISDOM_PATTERNS = [
        (r'\b(learned|realized|understood|discovered)\b', 0.08),
        (r'\b(because|therefore|which means)\b', 0.05),
        (r'\b(pattern|cycle|tendency)\b', 0.1),
        (r'\b(in the past|looking back|used to)\b', 0.06),
        (r'\b(helps me|works for me|I\'ve found)\b', 0.08),
    ]
    
    # Temporal depth markers (τ)
    TEMPORAL_PATTERNS = [
        (r'\b(ancient|eternal|generations|ancestors|always been)\b', 0.15),
        (r'\b(decades|centuries|ages|timeless)\b', 0.12),
        (r'\b(years|seasons|cycles)\b', 0.08),
        (r'\b(recently|lately|these days)\b', 0.03),
        (r'\b(now|today|moment|instant)\b', 0.01),
    ]
    
    CRISIS_PATTERNS = [
        # Suicidal ideation
        r'\b(kill myself|want to die|end it all)\b',
        r'\b(suicide|suicidal)\b',
        r'\b(can\'t go on|no point|give up)\b',
        # Substance crisis
        r'\b(overdose|OD|relapse.*now)\b',
        r'\b(meth|heroin|fentanyl).*(helps|need|using)\b',
        # Paranoid psychosis
        r'\b(watching|watching me|they.*(watching|following|listening))\b',
        r'\b(can\'t be trusted|trust no one|nobody.*trust)\b',
        r'\b(signals?|messages?).*(hidden|secret|everywhere)\b',
        # Manic/dissociative
        r'([A-Z]{2,}\s+){2,}',
        r'(\b\w+\b)\s+\1\s+\1',
    ]
    
    CONTRADICTION_PAIRS = [
        (r'\b(fine|okay|good)\b', r'\b(but|except|actually)\b'),
        (r'\b(don\'t care)\b', r'\b(hurts|upset|angry)\b'),
        (r'\b(over it)\b', r'\b(still|can\'t stop)\b'),
        # Split/paranoid thinking
        (r'\b(love|trust)\b.*\beveryone\b', r'\b(nobody|no one|can\'t).*(trust)\b'),
        (r'\b(I\'?m? (fine|okay|good))\b', r'\b(need|help|can\'t)\b'),
        # Denial patterns
        (r'\bI\'?m? (fine|okay)\b', r'[A-Z]{3,}'),
    ]
    
    def __init__(self, default_lens: str = "modern_western"):
        """Initialize with a default cultural lens."""
        self.default_lens = default_lens
        self.available_lenses = list(CULTURAL_LENSES.keys())
    
    def perceive(
        self, 
        text: str, 
        lens_name: Optional[str] = None,
        multi_lens: bool = True
    ) -> Perception:
        """
        Perceive text through the Rose Glass.
        
        Args:
            text: Human communication to perceive
            lens_name: Specific lens to use (None = default)
            multi_lens: Calculate λ interference across all lenses
            
        Returns:
            Perception with all dimensional readings
        """
        if not text or not text.strip():
            return Perception(
                psi=0.5, rho=0.5, q=0.0, q_optimized=0.0, f=0.5,
                tau=0.5, lambda_coef=0.0,
                state=CommunicationState.GROUNDED
            )
        
        active_lens_name = lens_name or self.default_lens
        active_lens = CULTURAL_LENSES.get(active_lens_name, CULTURAL_LENSES['modern_western'])
        
        text_lower = text.lower()
        markers = {"isolation": [], "activation": [], "belonging": [], "wisdom": [], "crisis": []}
        
        # === Calculate raw dimensions ===
        
        # q (emotional activation)
        q = 0.2
        for pattern, weight in self.ACTIVATION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                q += weight
                markers["activation"].append(pattern)
        q = min(1.0, q)
        
        # f (social belonging)
        f = 0.5
        for pattern, marker_type in self.ISOLATION_PATTERNS:
            if re.search(pattern, text_lower):
                f -= 0.1
                markers["isolation"].append(marker_type)
        for pattern, weight in self.BELONGING_PATTERNS:
            if re.search(pattern, text_lower):
                f += weight
                markers["belonging"].append(pattern)
        f = max(0.0, min(1.0, f))
        
        # ρ (wisdom depth)
        rho = 0.3
        for pattern, weight in self.WISDOM_PATTERNS:
            if re.search(pattern, text_lower):
                rho += weight
                markers["wisdom"].append(pattern)
        sentences = re.split(r'[.!?]+', text)
        avg_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if avg_length > 15:
            rho += 0.1
        rho = min(1.0, rho)
        
        # Ψ (internal consistency)
        psi = 0.7
        for affirm, negate in self.CONTRADICTION_PAIRS:
            if re.search(affirm, text_lower) and re.search(negate, text_lower):
                psi -= 0.15
        if len(sentences) > 1:
            length_variance = sum((len(s.split()) - avg_length)**2 for s in sentences) / len(sentences)
            if length_variance > 50:
                psi -= 0.1
        psi = max(0.0, min(1.0, psi))
        
        # τ (temporal depth)
        tau = 0.3
        for pattern, weight in self.TEMPORAL_PATTERNS:
            if re.search(pattern, text_lower):
                tau = max(tau, weight + 0.3)  # Take highest temporal marker
        tau = min(1.0, tau)
        
        # Crisis markers
        for pattern in self.CRISIS_PATTERNS:
            if re.search(pattern, text_lower):
                markers["crisis"].append(pattern)
        
        # === Apply lens calibration ===
        q_optimized = self._optimize_q(q, active_lens)
        
        # === Calculate multi-lens readings for λ ===
        lens_readings = []
        if multi_lens:
            for lens_key, lens_cal in CULTURAL_LENSES.items():
                q_opt_lens = self._optimize_q(q, lens_cal)
                coupling = lens_cal.coupling_strength * rho * q_opt_lens
                coherence_lens = (
                    psi * lens_cal.psi_weight +
                    (rho * psi) * lens_cal.rho_weight +
                    q_opt_lens * lens_cal.q_weight +
                    (f * psi) * lens_cal.f_weight +
                    coupling
                )
                lens_readings.append(LensReading(
                    lens_name=lens_key,
                    psi=psi, rho=rho, q=q, q_optimized=q_opt_lens,
                    f=f, coherence=coherence_lens
                ))
        
        # λ = standard deviation of coherence across lenses
        if lens_readings:
            coherences = [lr.coherence for lr in lens_readings]
            mean_coh = sum(coherences) / len(coherences)
            variance = sum((c - mean_coh)**2 for c in coherences) / len(coherences)
            lambda_coef = math.sqrt(variance)
        else:
            lambda_coef = 0.0
        
        # Determine state
        state = self._determine_state(psi, rho, q, f, markers)
        
        # Confidence based on text length
        word_count = len(text.split())
        confidence = min(0.95, 0.5 + word_count * 0.02)
        
        return Perception(
            psi=psi,
            rho=rho,
            q=q,
            q_optimized=q_optimized,
            f=f,
            tau=tau,
            lambda_coef=lambda_coef,
            lens_name=active_lens_name,
            lens_readings=lens_readings,
            markers=markers,
            state=state,
            confidence=confidence
        )
    
    def _optimize_q(self, q_raw: float, lens: LensCalibration) -> float:
        """Biological optimization using Michaelis-Menten with lens-specific params."""
        if q_raw <= 0:
            return 0.0
        return q_raw / (lens.km + q_raw + (q_raw ** 2 / lens.ki))
    
    def _determine_state(
        self, psi: float, rho: float, q: float, f: float, markers: Dict
    ) -> CommunicationState:
        """Determine overall communication state."""
        if markers.get("crisis"):
            return CommunicationState.CRISIS
        if f < 0.3 and q > 0.5:
            return CommunicationState.WITHDRAWN
        if q > 0.7:
            return CommunicationState.ACTIVATED
        if psi > 0.7 and rho > 0.6 and 0.3 < q < 0.6:
            return CommunicationState.FLOW
        return CommunicationState.GROUNDED
    
    def list_lenses(self) -> List[Dict]:
        """List all available cultural lenses."""
        return [
            {"name": name, "description": lens.description}
            for name, lens in CULTURAL_LENSES.items()
        ]
    
    def compare_lenses(self, text: str) -> Dict[str, float]:
        """Compare how text reads through all lenses."""
        perception = self.perceive(text, multi_lens=True)
        return {
            lr.lens_name: round(lr.coherence, 3)
            for lr in perception.lens_readings
        }


# Singleton instance
_lens = None

def get_lens() -> RoseLens:
    """Get or create the Rose Glass lens."""
    global _lens
    if _lens is None:
        _lens = RoseLens()
    return _lens

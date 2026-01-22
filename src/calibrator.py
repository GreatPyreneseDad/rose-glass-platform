"""
Rose Glass Calibrator - Adapts responses to user state
The outbound side of the lens
"""

from dataclasses import dataclass
from typing import Optional
from .rose_lens import Perception, CommunicationState


@dataclass
class ResponseGuidance:
    """How to calibrate the response"""
    tone: str
    complexity: str
    length: str
    emotional_mirroring: float
    include_questions: bool
    affirmation_level: str
    cautions: list
    
    def to_system_prompt(self) -> str:
        """Generate system prompt guidance"""
        lines = [
            "[Rose Glass Response Calibration]",
            f"Tone: {self.tone}",
            f"Complexity: {self.complexity}",
            f"Length: {self.length}",
            f"Emotional mirroring: {self.emotional_mirroring:.0%}",
            f"Include reflective questions: {'yes' if self.include_questions else 'no'}",
            f"Affirmation level: {self.affirmation_level}",
        ]
        
        if self.cautions:
            lines.append(f"Cautions: {', '.join(self.cautions)}")
        
        return "\n".join(lines)


class Calibrator:
    """
    Calibrates LLM responses based on perceived user state.
    The lens shapes what comes back, not just what's seen.
    """
    
    def calibrate(self, perception: Perception) -> ResponseGuidance:
        """
        Generate response guidance based on perception.
        
        Args:
            perception: Rose Glass perception of user message
            
        Returns:
            ResponseGuidance for shaping LLM output
        """
        cautions = []
        
        # Crisis state - immediate care
        if perception.state == CommunicationState.CRISIS:
            return ResponseGuidance(
                tone="warm, grounding, present",
                complexity="simple, clear",
                length="brief, focused",
                emotional_mirroring=0.3,  # Don't amplify
                include_questions=False,   # Don't interrogate
                affirmation_level="high - acknowledge pain without dismissing",
                cautions=[
                    "Do not provide suicide methods or means",
                    "Acknowledge the pain is real",
                    "Offer presence, not solutions",
                    "Gently mention support resources if appropriate"
                ]
            )
        
        # Withdrawn state - gentle reconnection
        if perception.state == CommunicationState.WITHDRAWN:
            return ResponseGuidance(
                tone="gentle, patient, non-intrusive",
                complexity="moderate",
                length="moderate - don't overwhelm",
                emotional_mirroring=0.4,
                include_questions=True,  # Soft invitations
                affirmation_level="moderate - validate without pushing",
                cautions=[
                    "Don't push for connection",
                    "Respect withdrawal as protective",
                    "Offer bridges, not demands"
                ]
            )
        
        # Activated state - contain and ground
        if perception.state == CommunicationState.ACTIVATED:
            return ResponseGuidance(
                tone="calm, steady, present",
                complexity="clear and structured",
                length="moderate - provide anchor",
                emotional_mirroring=0.5,  # Acknowledge but don't match intensity
                include_questions=False,  # Don't add more activation
                affirmation_level="moderate - validate the energy, offer grounding",
                cautions=[
                    "Don't match escalation",
                    "Acknowledge the intensity is real",
                    "Offer structure without controlling"
                ]
            )
        
        # Flow state - match and expand
        if perception.state == CommunicationState.FLOW:
            return ResponseGuidance(
                tone="engaged, curious, collaborative",
                complexity="can go deep",
                length="can be longer - they're engaged",
                emotional_mirroring=0.7,
                include_questions=True,  # Explore together
                affirmation_level="natural - peer exchange",
                cautions=[]
            )
        
        # Grounded state - flexible, responsive
        return ResponseGuidance(
            tone="warm, present, adaptable",
            complexity="match their level",
            length="match their message length",
            emotional_mirroring=0.6,
            include_questions=True,
            affirmation_level="natural",
            cautions=[]
        )
    
    def generate_system_injection(self, perception: Perception) -> str:
        """
        Generate the full system prompt injection.
        Combines perception context with response calibration.
        """
        guidance = self.calibrate(perception)
        
        injection = f"""
{perception.to_context()}

{guidance.to_system_prompt()}

IMPORTANT INSTRUCTIONS:
- Use this perception to INFORM your response style, tone, and approach
- Do NOT output any "Rose Glass" analysis or perception data in your response
- Do NOT mention coherence scores, dimensions, or states to the user
- Do NOT role-play as a perception system
- Simply respond naturally as a helpful assistant, letting the calibration shape HOW you respond
- The user should not see any of this metadata - just your calibrated response
"""
        return injection.strip()


# Singleton
_calibrator = None

def get_calibrator() -> Calibrator:
    """Get or create the calibrator."""
    global _calibrator
    if _calibrator is None:
        _calibrator = Calibrator()
    return _calibrator

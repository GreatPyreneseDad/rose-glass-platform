#!/usr/bin/env python3
"""
Quick test of Rose Glass perception
Run: python test_lens.py
"""

import sys
sys.path.insert(0, '.')

from src.rose_lens import get_lens
from src.calibrator import get_calibrator

def test_perception():
    lens = get_lens()
    calibrator = get_calibrator()
    
    test_cases = [
        "I'm fine. Everything is under control.",
        "Nobody understands what I'm going through. I'm completely alone.",
        "FUCK THIS!!! I can't take it anymore!!!",
        "I've been thinking about what happened, and I realize I was wrong.",
        "My sponsor and I talked yesterday. We're going to a meeting together.",
        "I don't know if I can keep going. What's the point anymore?",
    ]
    
    print("🌹 Rose Glass Perception Test")
    print("=" * 60)
    
    for text in test_cases:
        print(f"\n📝 \"{text[:50]}{'...' if len(text) > 50 else ''}\"")
        print("-" * 40)
        
        perception = lens.perceive(text)
        guidance = calibrator.calibrate(perception)
        
        print(f"   Ψ (consistency): {perception.psi:.2f}")
        print(f"   ρ (wisdom):      {perception.rho:.2f}")
        print(f"   q (activation):  {perception.q:.2f} → {perception.q_optimized:.2f}")
        print(f"   f (belonging):   {perception.f:.2f}")
        print(f"   Coherence:       {perception.coherence:.2f}")
        print(f"   State:           {perception.state.value}")
        print(f"   → Tone:          {guidance.tone}")
        
        if perception.markers.get("isolation"):
            print(f"   ⚠️  Isolation:    {perception.markers['isolation']}")
        if perception.markers.get("crisis"):
            print(f"   🚨 CRISIS DETECTED")
    
    print("\n" + "=" * 60)
    print("✅ Rose Glass is perceiving.\n")

if __name__ == "__main__":
    test_perception()

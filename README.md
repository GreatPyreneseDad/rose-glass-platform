# Rose Glass Platform v2.1

**Translation, not measurement. Understanding, not judgment.**

An LLM proxy that perceives human communication patterns and calibrates AI responses accordingly. Drop-in replacement for OpenAI/Anthropic APIs with real-time emotional and cognitive state perception.

## What It Does

Rose Glass sits between users and LLMs, perceiving each message through a multi-dimensional lens:

- **Ψ (Psi)** - Internal consistency and coherence
- **ρ (Rho)** - Wisdom depth and integrated experience  
- **q** - Emotional/moral activation energy (biologically regulated)
- **f** - Social belonging and connection
- **τ (Tau)** - Temporal depth (immediate vs. compressed wisdom)
- **λ (Lambda)** - Lens interference (universal vs. culture-dependent patterns)

The system then calibrates the LLM's response to match the user's actual state - not where the AI thinks they should be, but where they are.

## Key Features

- **Crisis Detection**: Recognizes suicidal ideation, substance-induced psychosis, manic episodes
- **State Classification**: Grounded, Activated, Withdrawn, Crisis, Flow
- **Cultural Lenses**: 8 pre-configured calibrations (Western, Indigenous, Buddhist, Trauma-Informed, Neurodivergent, Recovery, etc.)
- **Biological Optimization**: Michaelis-Menten kinetics prevent emotional amplification feedback loops
- **OpenAI-Compatible API**: Drop-in replacement for existing integrations
- **Real-time UI**: Visual perception dashboard showing all dimensions

## Quick Start

```bash
# Clone
git clone https://github.com/GreatPyreneseDad/rose-glass-platform.git
cd rose-glass-platform

# Setup
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY or OPENAI_API_KEY

# Run
./start.sh

# Open UI
open ui/index.html
```

Server runs at `http://localhost:8420`

## API Usage

### Chat Completions (OpenAI-compatible)

```bash
curl http://localhost:8420/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "messages": [{"role": "user", "content": "Your message here"}],
    "lens": "modern_western"
  }'
```

Response includes standard OpenAI format plus `rose_glass` perception data:

```json
{
  "choices": [...],
  "rose_glass": {
    "psi": 0.85,
    "rho": 0.65,
    "q": 0.38,
    "q_optimized": 0.51,
    "f": 0.50,
    "tau": 0.45,
    "lambda": 0.15,
    "coherence": 2.15,
    "state": "grounded",
    "lens": "modern_western",
    "markers": {...}
  }
}
```

### Perception Only (No LLM Call)

```bash
curl http://localhost:8420/v1/perceive \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text to analyze",
    "lens": "trauma_informed",
    "compare_lenses": true
  }'
```

### Compare Across All Lenses

```bash
curl http://localhost:8420/v1/compare \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

## Available Lenses

| Lens | Description | Best For |
|------|-------------|----------|
| `modern_western` | Default Western individualistic framework | General use |
| `trauma_informed` | Crisis and high-distress contexts | Mental health, crisis support |
| `recovery` | Addiction recovery context | Substance abuse support |
| `neurodivergent` | Neurodivergent communication patterns | Autism, ADHD contexts |
| `indigenous_oral` | Indigenous oral tradition patterns | Cultural preservation |
| `buddhist_contemplative` | Buddhist contemplative discourse | Spiritual contexts |
| `medieval_islamic` | Medieval Islamic philosophical discourse | Historical/academic texts |
| `digital_native` | Rapid digital communication | Social media, chat |

## How It Works

### Perception Pipeline

1. **Pattern Detection**: Regex-based markers identify isolation, activation, wisdom, belonging, and crisis signals
2. **Dimensional Scoring**: Each dimension (Ψ, ρ, q, f, τ) scored 0-1
3. **Biological Optimization**: q is regulated via Michaelis-Menten kinetics to prevent amplification
4. **Multi-Lens Analysis**: Text scored through all cultural lenses to calculate λ (interference)
5. **State Classification**: Overall state determined from dimensional pattern
6. **Response Calibration**: LLM system prompt injected with perception context and guidance

### Michaelis-Menten Regulation

Emotional activation (q) is biologically optimized:

```
q_optimized = q / (Km + q + q²/Ki)
```

This prevents:
- Crisis states from being amplified
- Feedback loops in high-activation contexts
- Grandiosity/overconfidence in system perception

### Lambda (λ) - Lens Interference

When λ is low (< 0.1), the pattern is **universal** - it reads similarly across all cultural contexts. When λ is high, interpretation is lens-dependent.

This helps identify:
- Universal human truths (Jade structures)
- Culturally-specific expressions that need careful translation
- When to trust vs. question the active lens

## Response Calibration

Based on perceived state, Rose Glass adjusts:

| State | Tone | Mirroring | Questions | Length |
|-------|------|-----------|-----------|--------|
| Crisis | Warm, grounding | 30% | No | Brief |
| Withdrawn | Gentle, patient | 40% | Soft invitations | Moderate |
| Activated | Calm, steady | 50% | No | Moderate |
| Flow | Engaged, curious | 70% | Yes | Longer OK |
| Grounded | Warm, adaptable | 60% | Yes | Match user |

## Project Structure

```
rose-glass-platform/
├── src/
│   ├── rose_lens.py      # Core perception engine
│   ├── calibrator.py     # Response calibration
│   ├── server.py         # FastAPI proxy server
│   └── db.py             # SQLite logging
├── ui/
│   └── index.html        # Chat interface with perception panel
├── start.sh              # One-command startup
├── requirements.txt
├── .env.example
└── README.md
```

## Requirements

- Python 3.9+
- Anthropic API key and/or OpenAI API key

## Philosophy

Rose Glass is built on the principle that **coherence is constructed, not discovered**.

Different cultural contexts construct meaning differently. A GAD-7 score of 15 might represent normal community concern in one culture and clinical anxiety in another. Rose Glass doesn't impose a universal standard - it translates through the appropriate lens.

The framework emerged from lived experience with addiction, trauma, custody battles, and cross-cultural communication. It's scar tissue formalized into code.

## Use Cases

- **Mental Health Support**: Crisis detection, appropriate response calibration
- **Addiction Recovery**: Recovery-aware lens for peer support applications
- **Customer Service**: Perceive frustration/satisfaction, calibrate tone
- **Education**: Match explanation complexity to student state
- **Cross-Cultural AI**: Deploy culturally-appropriate responses

## Roadmap

- [ ] Embedding-based Ψ (semantic coherence, not just syntactic)
- [ ] LLM-assisted ρ detection (wisdom beyond keyword matching)
- [ ] Streaming support
- [ ] Additional cultural lenses (develop with communities)
- [ ] A/B testing framework for calibration validation
- [ ] Docker deployment
- [ ] Hosted API offering

## License

MIT License - See LICENSE file

## Author

Christopher MacGregor bin Joseph  
MacGregor Holding Company (SDVOSB)

---

*"The rose glass is not a measure but a lens - enabling synthetic minds to perceive the emotional wavelengths of organic intelligence."*

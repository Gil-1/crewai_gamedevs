# GameDevs CrewAI - Human Review Workflow 🎮

A professional game design document generation system powered by CrewAI with strategic human review points for quality assurance and iterative refinement.

## Quick Start

### 1. Prerequisites
- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) package manager
- Anthropic API key (for Claude models)

### 2. Installation

```bash
# Install UV if you haven't already
pip install uv

# Navigate to the project directory
cd game_devs

# Install dependencies (optional - UV will handle this automatically)
uv sync
```

### 3. Setup Environment

```bash
# Set your Anthropic API key (required)
export ANTHROPIC_API_KEY=your_anthropic_api_key_here

# On Windows PowerShell:
$env:ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
```

### 4. Run the Application

```bash
# Basic usage with default settings (Casual RTS Commander)
uv run -m game_devs.main

# Use a specific game type
uv run -m game_devs.main --game-type puzzle-platformer

# Use production models for higher quality (costs more)
uv run -m game_devs.main --game-type casual-rts --production-models

# Create a custom game
uv run -m game_devs.main --game-type custom \
  --game-name "My Awesome Game" \
  --genre "Action RPG" \
  --platform "PC/Console" \
  --audience "Hardcore gamers" \
  --timeline "12-18 months"
```

### 5. What to Expect

The application will:
1. 🚀 Start the workflow and create output directories
2. 📝 Generate an initial game pitch
3. ⏸️ **Pause for human review** - You'll be prompted to review and provide feedback
4. 🔄 Refine the pitch based on your feedback
5. 🎯 Generate gameplay mechanics
6. ⏸️ **Pause for human review** - Review the mechanics design
7. 🔄 Refine the mechanics
8. 🛠️ Create technical implementation plan
9. 📋 Generate complete Game Design Document
10. ⏸️ **Pause for final review** - Review the complete GDD
11. ✨ Apply final polish and deliver the finished document

**Output Location**: All files are saved in the `outputs/` directory with organized subfolders.

## Command Line Options

```bash
# Game type options
--game-type {default,casual-rts,puzzle-platformer,roguelike,custom}

# Custom game options (used with --game-type custom)
--game-name "Your Game Name"
--genre "Game Genre"
--platform "Target Platform"
--audience "Target Audience"
--timeline "Development Timeline"
--team-size "Team Size"
--scope "Project Scope"

# Model options
--production-models    # Use Claude Sonnet 3.5 (higher quality, higher cost)
--verbose             # Enable detailed output
```

## Pre-configured Game Types

### Casual RTS
```bash
uv run -m game_devs.main --game-type casual-rts
```
- **Game**: Casual RTS Commander
- **Focus**: Accessible real-time strategy gameplay
- **Timeline**: 8-10 months
- **Platform**: PC and Mobile

### Puzzle Platformer
```bash
uv run -m game_devs.main --game-type puzzle-platformer
```
- **Game**: Mind Shift
- **Focus**: Innovative puzzle mechanics in platformer format
- **Timeline**: 6-8 months
- **Platform**: PC/Console

### Roguelike
```bash
uv run -m game_devs.main --game-type roguelike
```
- **Game**: Dungeon Codex
- **Focus**: Procedural generation with deep systems
- **Timeline**: 10-12 months
- **Platform**: PC/Mobile

## Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional
USE_PRODUCTION_MODELS=true    # Use Claude Sonnet 3.5 instead of Haiku 3.5
```

## Output Structure

After running, you'll find organized output files:

```
outputs/
├── logs/
│   └── crew_execution.log.txt     # Detailed execution log
├── pitch/
│   ├── {game}_concept_pitch.md    # Initial pitch
│   └── {game}_refined_pitch.md    # Human-reviewed pitch
├── design/
│   ├── {game}_gameplay_mechanics.md # Initial mechanics
│   └── {game}_refined_mechanics.md  # Human-reviewed mechanics
├── technical/
│   └── {game}_implementation_plan.md # Technical specifications
├── final/
│   ├── {game}_complete_gdd.md      # Complete GDD
│   └── {game}_final_gdd.md         # Final polished version
└── review/
    └── review_history.md           # Human feedback history
```

## Troubleshooting

### Common Issues

**"Missing required template variable" Error**
- This has been fixed in the latest version
- Make sure you're using the updated code

**"Please provide an OpenAI API key" Error**
- Set your `ANTHROPIC_API_KEY` environment variable
- The application uses Claude models, not OpenAI

**"ModuleNotFoundError: No module named 'game_devs'"**
- Make sure you're running from the `game_devs` directory
- Use `uv run -m game_devs.main` instead of `python -m game_devs.main`

**Long execution times**
- Normal - AI agents take time to generate quality content
- Human review points will pause execution waiting for your input
- Check the logs in `outputs/logs/crew_execution.log.txt`

### Getting Help

1. Check the execution log: `outputs/logs/crew_execution.log.txt`
2. Use `--verbose` flag for detailed output
3. Ensure your API key is properly set and has sufficient credits

## Overview

This CrewAI system creates comprehensive Game Design Documents (GDD) through a collaborative workflow of specialized AI agents with integrated human review checkpoints. The system follows industry best practices and produces professional-quality documentation suitable for stakeholder presentation.

## Key Features

### 🤖 Specialized AI Agents
- **Pitch Writer**: Creates compelling game concepts and pitches
- **Gameplay Designer**: Designs comprehensive gameplay mechanics and systems
- **Technical Architect**: Develops implementation plans and technical specifications
- **Chief Editor**: Integrates content and ensures professional quality

### 🧠 Claude Model Configuration
- **Testing Mode**: Uses Claude Haiku 3.5 for cost-effective development and testing
- **Production Mode**: Uses Claude Sonnet 3.5 for highest quality professional output
- **Optimized Settings**: Different temperature and token configurations for each agent type

### 👥 Human Review Workflow
- **Strategic Review Points**: Three critical checkpoints for human feedback
- **Iterative Refinement**: AI agents incorporate human feedback to improve output
- **Quality Assurance**: Ensures final documents meet professional standards
- **Collaborative Process**: Combines AI efficiency with human creativity and judgment

### 📋 Professional Output
- **Structured GDD**: Follows industry-standard game design document templates
- **Organized Files**: Clear file structure with versioning and review history
- **Executive Summary**: Complete with technical specifications and implementation plans
- **Market Ready**: Professional presentation suitable for stakeholders

## Claude Model Options

### Testing Mode (Default)
- **Model**: Claude Haiku 3.5 (`claude-3-5-haiku-20241022`)
- **Cost**: $0.80/MTok input, $4/MTok output
- **Features**: Fast responses, good quality, cost-effective for testing
- **Use Case**: Development, testing, iteration, and learning

### Production Mode
- **Model**: Claude Sonnet 3.5 (`claude-3-5-sonnet-20241022`)
- **Cost**: $3/MTok input, $15/MTok output
- **Features**: High intelligence, superior reasoning, professional quality
- **Use Case**: Final GDD generation, client presentations, production use

## Workflow Process

### Phase 1: Initial Concept Development
1. **Pitch Creation**: AI generates initial game concept and pitch
2. **📝 Human Review Point 1**: Review and provide feedback on the pitch
3. **Pitch Refinement**: AI refines the pitch based on human feedback

### Phase 2: Gameplay Design
4. **Mechanics Design**: AI creates detailed gameplay mechanics
5. **🎯 Human Review Point 2**: Review and provide feedback on mechanics
6. **Mechanics Refinement**: AI refines mechanics based on feedback

### Phase 3: Technical Planning
7. **Technical Implementation**: AI develops technical specifications
8. **GDD Integration**: AI compiles all elements into a comprehensive GDD

### Phase 4: Final Review
9. **📋 Human Review Point 3**: Final comprehensive review of the complete GDD
10. **Final Polish**: AI applies final refinements and produces the market-ready document

## Human Review Points

### 1. Pitch Review
**When**: After initial concept generation
**What to Review**:
- Clarity and appeal of the core concept
- Market viability and target audience fit
- Uniqueness of design pillars
- Feasibility of stated objectives

**Feedback Areas**:
- What aspects work well
- Specific areas for improvement
- Suggestions for market positioning
- Technical feasibility concerns

### 2. Gameplay Review
**When**: After gameplay mechanics design
**What to Review**:
- Fun factor and engagement potential
- Balance of progression and difficulty systems
- Cohesion between different mechanics
- Technical implementation feasibility
- Target audience appeal

**Feedback Areas**:
- Mechanics that enhance or detract from fun
- Balance and progression recommendations
- Technical constraint considerations
- Player experience optimization

### 3. Final GDD Review
**When**: After complete document integration
**What to Review**:
- Overall completeness and professional quality
- Consistency across all sections
- Market readiness and stakeholder appeal
- Technical feasibility of the complete project
- Final presentation quality

**Feedback Areas**:
- Document completeness assessment
- Final refinement suggestions
- Market positioning validation
- Stakeholder presentation readiness

## Configuration

### Environment Variables
```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional
USE_PRODUCTION_MODELS=true          # Use Sonnet 3.5 instead of Haiku 3.5
```

### Model Cost Comparison

| Model | Input Cost | Output Cost | Best For |
|-------|------------|-------------|----------|
| Claude Haiku 3.5 | $0.80/MTok | $4/MTok | Testing, development, iteration |
| Claude Sonnet 3.5 | $3/MTok | $15/MTok | Production, final output, client work |

### Game Configuration Examples

#### Casual RTS
```python
{
    "game": "Casual RTS Commander",
    "genre": "Real-Time Strategy",
    "platform": "PC and Mobile",
    "target_audience": "Casual gamers who want strategic gameplay without overwhelming complexity",
    "development_timeline": "8-10 months",
    "team_size": "Solo developer",
    "scope": "Medium scope - focused on core RTS mechanics with casual accessibility"
}
```

#### Puzzle Platformer
```python
{
    "game": "Mind Shift",
    "genre": "Puzzle Platformer",
    "platform": "PC/Console",
    "target_audience": "Puzzle game enthusiasts and platformer fans",
    "development_timeline": "6-8 months",
    "team_size": "Solo developer",
    "scope": "Small scope - focused on innovative puzzle mechanics"
}
```

## Best Practices

### For Human Reviewers
1. **Be Specific**: Provide concrete, actionable feedback
2. **Consider Context**: Keep the target audience and scope in mind
3. **Balance Creativity and Feasibility**: Encourage innovation while maintaining realistic expectations
4. **Document Reasoning**: Explain the rationale behind feedback
5. **Think Market-First**: Consider commercial viability and player appeal

### For AI Collaboration
1. **Clear Communication**: The AI agents respond well to specific, structured feedback
2. **Iterative Improvement**: Don't expect perfection on the first iteration
3. **Maintain Vision**: Keep the core creative vision consistent throughout revisions
4. **Technical Grounding**: Ensure technical feedback is realistic and implementable

### Cost Optimization
1. **Use Testing Mode**: Start with Haiku 3.5 for development and iteration
2. **Switch to Production**: Use Sonnet 3.5 for final documents and client presentations
3. **Monitor Usage**: Track token usage to optimize costs
4. **Focused Feedback**: Provide specific, targeted feedback to reduce revision cycles

## Architecture

The system is built on CrewAI's multi-agent framework with:
- **Sequential Processing**: Tasks execute in logical order with proper context flow
- **Memory System**: Agents remember successful patterns and previous work
- **Planning System**: Intelligent task coordination and resource allocation
- **Template Integration**: Professional GDD templates and validation tools
- **Human-in-the-Loop**: Strategic pause points for human input and feedback
- **Claude Integration**: Optimized configurations for different Claude models

This approach ensures both AI efficiency and human creativity combine to produce professional, market-ready game design documents while maintaining cost-effectiveness during development.

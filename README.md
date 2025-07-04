# CrewGameDevs

## Project Overview
CrewGameDevs is an AI-powered multi-agent system built with [CrewAI](https://crewai.com) to accelerate rapid game prototyping and idea testing. The project simulates a collaborative team of three core roles—Game Director, Game Designer, and Game Developer—each represented as an autonomous agent. Their collective goal is to quickly develop and iterate on game prototypes, making it easy to explore and validate new game concepts.

## Goals
- Rapidly generate and iterate on game prototype ideas
- Simulate real-world game development team collaboration
- Modular, extensible agent/task design for easy customization

## Technical Tools
- CrewAI 0.140.0 (multi-agent orchestration)
- Python 3.10–3.13
- (Optional) Unreal Engine C++ for downstream prototyping

## Agents
- **Game Director**: Oversees and guides the creative vision, execution, and overall direction of the game prototype. Ensures a coherent and engaging experience by aligning gameplay, narrative, art, and production values.
- **Game Designer**: Designs and prototypes core gameplay mechanics, rules, and systems. Focuses on creating compelling, enjoyable, and innovative player experiences.
- **Game Developer**: Implements and optimizes the technical foundation of the prototype, turning design concepts into functional, playable experiences.

## Tasks
- **game_director_task**: Defines the creative vision, core concept, and high-level direction for the prototype. Sets objectives and constraints for the team.
- **game_designer_task**: Designs the core gameplay mechanics, rules, and systems based on the vision. Outlines the gameplay loop and key features.
- **game_developer_task**: Creates a technical plan, outlining architecture, tools, and technologies. Provides a step-by-step plan for rapid prototyping and testing.

## Project Structure
- `src/game_devs/config/agents.yaml` — Agent definitions and roles
- `src/game_devs/config/tasks.yaml` — Task definitions and agent assignments
- `src/game_devs/crew.py` — Crew, agent, and task orchestration logic
- `src/game_devs/main.py` — Entrypoint for running, training, and testing the crew

## Installation
1. **Install Python 3.10–3.13**
2. **Install [uv](https://docs.astral.sh/uv/):**
   ```bash
   pip install uv
   ```
3. **Install dependencies:**
   ```bash
   crewai install
   ```
4. **Set up environment variables:**
   - Add your LLM provider API key (e.g., `OPENAI_API_KEY`) to a `.env` file in the project root.

## Usage
Run the crew from the project root:
```bash
crewai run
```

### Customizing Inputs
Edit `src/game_devs/main.py` to change the game prototype name:
```python
inputs = {
    'game': 'Rapid Prototype Platformer'
}
```

### Training, Testing, and Replay
- **Train:**
  ```bash
  crewai train <n_iterations> <output_file>
  ```
- **Test:**
  ```bash
  crewai test <n_iterations> <eval_llm>
  ```
- **Replay:**
  ```bash
  crewai replay <task_id>
  ```

## Extending the Project
- Add new agents or tasks by editing the YAML config files
- Integrate tools or knowledge sources in `crew.py`
- Use the modular structure to adapt to other creative or technical workflows

## References & Support
- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)

---
Empower your game development process with AI-driven collaboration and rapid prototyping!

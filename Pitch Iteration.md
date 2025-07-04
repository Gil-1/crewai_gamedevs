# Multiple pitches feature to be validated by human

Insert a “**Round-0 : Pitch Ideation & Selection**” stage in front of the rest of the pipeline.
Below is a practical way to do it with minimal changes to your existing CrewAI project.

## 1 . New (or repurposed) **Pitch-Ideation Agent**

| Agent | Role | Key prompt additions |
| --- | --- | --- |
| Pitch Ideator : (you can rename or reuse the current game_director) | Generate N distinct two-sentence pitches + hooks that all fit your constraints (casual RTS, solo dev 6-12 mo, PC). | “Produce 5 different, clearly numbered pitches. Each must fit the casual-RTS scope and have a unique hook. Keep each pitch ≤ 2 sentences, followed by a one-sentence ‘why it’s fun.’” |

Tip: ``keep allow_delegation: false`` for this agent so it simply brainstorms without asking others yet.

## 2 . Pitch-Review Task (Human-in-the-loop or AI scoring)

### Option A – Manual pick (simplest)

```yaml
Copier
Modifier
pitch_review_task:
  agent: pitch_ideator          # or a dedicated 'reviewer' agent
  description: |
    Present the numbered list of pitches to the human developer.
    Ask them to type the number of the pitch they want to pursue.
  expected_output: "Selected pitch number"
  human_input: true             # pauses run for your choice
```

You run ``crew.kickoff()`` → CLI pauses, you type “3” → execution resumes with that input stored as ``{selected_pitch}`` for downstream tasks.

## 3 . Pass the chosen pitch to the rest of the pipeline

Every downstream task (Gameplay Loop, Integration, Technical Plan) already receives context from previous tasks.
Add the chosen pitch to their context or expose it via an input variable:

```python
inputs = {"chosen_pitch": result_of_review_task }
GameDevs().crew().kickoff(inputs=inputs)
```

or inside YAML:

```yaml
core_gameplay_task:
  context: ["pitch_review_task"]     # the task that holds the chosen pitch
```

## 4 . Parallelising the idea phase (speed)

If you want multiple ideators working in parallel (to avoid a single model’s “mode”), set:

```python
Crew(
  agents=[pitch_ideator1, pitch_ideator2, …],
  tasks=[pitch_task1, pitch_task2, …],
  process=Process.concurrent   # only for the ideation sub-crew
)
```

Then feed all generated lists into the review task.

## 5 . Template changes at a glance

```yaml
# agents.yaml
pitch_ideator:
  role: "Pitch Ideator"
  goal: "Generate multiple compelling pitches for a casual RTS prototype."
  backstory: "A creative director known for razor-sharp elevator pitches."
  allow_delegation: false

# tasks.yaml
pitch_ideation_task:
  agent: pitch_ideator
  description: "Brainstorm 5 distinct two-sentence pitches..."
  expected_output: |
    ### Pitches
    1. ...
    2. ...
    ...
  output_file: "0_pitches.md"

pitch_review_task:
  agent: pitch_ideator   # or 'pitch_reviewer'
  context: [pitch_ideation_task]
  # either human_input: true  OR auto-evaluation prompt
```

Downstream tasks simply add ``context: [pitch_review_task]`` so they only see the chosen pitch.

## 6 . Why this works

- Keeps the heavy design work focused. You only invest Game-play + Tech effort after you or an evaluator pick the winning idea.
- Single run, two phases. CrewAI pauses for your choice, resumes to finish the GDD—still a “one-shot” document from the user’s perspective.
- Re-run friendly. Want new ideas? Just rerun the ideation stage; everything else stays intact.
- Scales later. The same pattern lets you add “art-style explorations” or “monetisation variants” as separate pitch batches before drilling down.

## Next Steps

1. Add the ideation and review tasks to your YAML.
2. Mark the review task with ``human_input: true`` (or create an evaluator agent).
3. Update downstream tasks to read ``{selected_pitch}`` from the review output.

That’s it—your crew will now **offer multiple pitched** concepts first, let you choose, and then flesh out only the winner into a full GDD ready for prototyping.

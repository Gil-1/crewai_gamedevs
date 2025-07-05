from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import LLM
from typing import List
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class GameDevs():
    """GameDevs crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def pitch_writer(self) -> Agent:
        # Configure LLM with Claude - Pitch Writer focuses on concept clarity
        claude_llm = LLM(
            model="claude-3-5-haiku-latest",
            temperature=0.8,
            max_tokens=4000,
            top_p=0.9
        )

        return Agent(
            config=self.agents_config['pitch_writer'], # type: ignore[index]
            llm=claude_llm,
            verbose=True,
            allow_delegation=False,  # Specialist focuses on pitch expertise
            memory=True  # Remember successful pitch patterns
        )

    @agent
    def gameplay_designer(self) -> Agent:
        # Configure LLM with Claude - Gameplay Designer focuses on mechanics
        claude_llm = LLM(
            model="claude-3-5-haiku-latest",
            temperature=0.7,
            max_tokens=4000,
            top_p=0.85
        )

        return Agent(
            config=self.agents_config['gameplay_designer'], # type: ignore[index]
            llm=claude_llm,
            verbose=True,
            allow_delegation=False,  # Specialist focuses on gameplay expertise
            memory=True  # Remember successful gameplay patterns
        )

    @agent
    def technical_architect(self) -> Agent:
        # Configure LLM with Claude - Technical Architect focuses on implementation
        claude_llm = LLM(
            model="claude-3-5-haiku-latest",
            temperature=0.3,
            max_tokens=4000,
            top_p=0.9
        )

        return Agent(
            config=self.agents_config['technical_architect'], # type: ignore[index]
            llm=claude_llm,
            verbose=True,
            allow_delegation=False,  # Specialist focuses on technical expertise
            memory=True  # Remember successful architectural patterns
        )

    @agent
    def chief_editor(self) -> Agent:
        # Configure LLM with Claude - Chief Editor focuses on integration and polish
        claude_llm = LLM(
            model="claude-3-5-haiku-latest",
            temperature=0.5,
            max_tokens=4000,
            top_p=0.8
        )

        return Agent(
            config=self.agents_config['chief_editor'], # type: ignore[index]
            llm=claude_llm,
            verbose=True,
            allow_delegation=True,  # Editor can coordinate with other agents for clarification
            memory=True  # Remember successful integration patterns
        )

    @task
    def pitch_concept_task(self) -> Task:
        return Task(
            config=self.tasks_config['pitch_concept_task'], # type: ignore[index]
        )

    @task
    def gameplay_mechanics_task(self) -> Task:
        return Task(
            config=self.tasks_config['gameplay_mechanics_task'], # type: ignore[index]
        )

    @task
    def gdd_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['gdd_integration_task'], # type: ignore[index]
        )

    @task
    def technical_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_implementation_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GameDevs crew"""
        return Crew(
            agents=self.agents, # All agents in the specialized workflow
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # Sequential for proper context flow
            verbose=True
            # Delegation enabled for chief_editor to coordinate when needed
        )

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
    def game_director(self) -> Agent:
        # Configure LLM with Ollama - Director coordinates team
        ollama_llm = LLM(
            model="claude-3-5-haiku-latest",
            #model="ollama/llama3.1:latest",
            #base_url=os.getenv("API_BASE", "http://localhost:11434"),
            temperature=0.8,
            max_tokens=4000,  # Increased to 32K for comprehensive outputs
            top_p=0.9
        )

        return Agent(
            config=self.agents_config['game_director'], # type: ignore[index]
            llm=ollama_llm,
            verbose=True,
            allow_delegation=True,  # ✅ Keep - Director coordinates team
            memory=True  # ✅ Add - Learn from past collaborations
        )

    @agent
    def game_designer(self) -> Agent:
        # Configure LLM with Ollama - Designer focuses on expertise
        ollama_llm = LLM(
            model="claude-3-5-haiku-latest",
            #model="ollama/llama3.1:latest",
            #base_url=os.getenv("API_BASE", "http://localhost:11434"),
            temperature=0.7,
            max_tokens=4000,  # Increased to 32K for comprehensive outputs
            top_p=0.85
        )

        return Agent(
            config=self.agents_config['game_designer'], # type: ignore[index]
            llm=ollama_llm,
            verbose=True,
            allow_delegation=False,  # ✅ Change - Specialist focuses on expertise
            memory=True  # ✅ Add - Remember design patterns
        )

    @agent
    def game_developer(self) -> Agent:
        # Configure LLM with Ollama - Developer focuses on expertise
        ollama_llm = LLM(
            model="claude-3-5-haiku-latest",
            #model="ollama/llama3.1:latest",
            #base_url=os.getenv("API_BASE", "http://localhost:11434"),
            temperature=0.3,
            max_tokens=4000,  # Increased to 32K for comprehensive outputs
            top_p=0.9
        )

        return Agent(
            config=self.agents_config['game_developer'], # type: ignore[index]
            llm=ollama_llm,
            verbose=True,
            allow_delegation=False,  # ✅ Change - Specialist focuses on expertise
            memory=True  # ✅ Add - Remember implementation patterns
        )

    @task
    def game_director_task(self) -> Task:
        return Task(
            config=self.tasks_config['game_director_task'], # type: ignore[index]
        )

    @task
    def game_designer_task(self) -> Task:
        return Task(
            config=self.tasks_config['game_designer_task'], # type: ignore[index]
        )

    @task
    def game_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config['game_developer_task'], # type: ignore[index]
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
            agents=self.agents, # All agents back in the list
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # Back to sequential - more efficient
            verbose=True
            # Keep delegation enabled in agents for flexibility
        )

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from typing import List
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
        return Agent(
            config=self.agents_config['game_director'], # type: ignore[index]
            verbose=True
        )

    @agent
    def game_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['game_designer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def game_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['game_developer'], # type: ignore[index]
            verbose=True
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

    @crew
    def crew(self) -> Crew:
        """Creates the GameDevs crew"""
        # Create knowledge source from GDD Guide
        gdd_knowledge_source = TextFileKnowledgeSource(
            file_paths=["GDD_GUIDE.md"]  # Relative path from knowledge directory
        )

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[gdd_knowledge_source], # Add knowledge sources here
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

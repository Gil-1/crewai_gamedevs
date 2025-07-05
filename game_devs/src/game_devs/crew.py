from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import LLM
from typing import List
import os

# Import template tools for knowledge base integration
from game_devs.tools.template_tools import (
    GDDTemplateReaderTool,
    DesignGuideSearchTool,
    KnowledgeDirectoryTool,
    TemplateValidationTool
)

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

    # Template tools integration for professional GDD generation
    # https://docs.crewai.com/concepts/agents#agent-tools

    def __init__(self):
        super().__init__()
        # Initialize template tools for knowledge base access
        self.design_guide_search = DesignGuideSearchTool()
        self.template_reader = GDDTemplateReaderTool()
        self.knowledge_explorer = KnowledgeDirectoryTool()
        self.template_validator = TemplateValidationTool()

        # Ensure output directories exist
        self._ensure_output_directories()

    def _ensure_output_directories(self):
        """Ensure all output directories exist for organized file structure."""
        output_dirs = [
            "out/concept",
            "out/design",
            "out/gdd",
            "out/technical",
            "out/review"
        ]

        for directory in output_dirs:
            os.makedirs(directory, exist_ok=True)

    # Claude LLM configurations optimized for different agent types
    # Using Haiku 3.5 as default for cost-effective testing
    @property
    def pitch_llm(self):
        """Creative pitch writing - higher temperature for creativity"""
        return LLM(
            model="claude-3-5-haiku-20241022",  # Haiku 3.5: Fast and cost-effective
            temperature=0.8,
            max_tokens=4000
        )

    @property
    def design_llm(self):
        """Gameplay design - balanced creativity and structure"""
        return LLM(
            model="claude-3-5-haiku-20241022",  # Haiku 3.5: Fast and cost-effective
            temperature=0.7,
            max_tokens=6000
        )

    @property
    def technical_llm(self):
        """Technical implementation - lower temperature for precision"""
        return LLM(
            model="claude-3-5-haiku-20241022",  # Haiku 3.5: Fast and cost-effective
            temperature=0.3,
            max_tokens=6000
        )

    @property
    def editorial_llm(self):
        """Editorial and integration - balanced approach"""
        return LLM(
            model="claude-3-5-haiku-20241022",  # Haiku 3.5: Fast and cost-effective
            temperature=0.5,
            max_tokens=8000
        )

    # Production-ready LLM configurations using higher-tier models
    @property
    def production_pitch_llm(self):
        """Production pitch writing with Sonnet 3.5 for better quality"""
        return LLM(
            model="claude-3-5-sonnet-20241022",  # Sonnet 3.5: High intelligence
            temperature=0.8,
            max_tokens=4000
        )

    @property
    def production_design_llm(self):
        """Production gameplay design with Sonnet 3.5"""
        return LLM(
            model="claude-3-5-sonnet-20241022",  # Sonnet 3.5: High intelligence
            temperature=0.7,
            max_tokens=6000
        )

    @property
    def production_technical_llm(self):
        """Production technical implementation with Sonnet 3.5"""
        return LLM(
            model="claude-3-5-sonnet-20241022",  # Sonnet 3.5: High intelligence
            temperature=0.3,
            max_tokens=6000
        )

    @property
    def production_editorial_llm(self):
        """Production editorial with Sonnet 3.5"""
        return LLM(
            model="claude-3-5-sonnet-20241022",  # Sonnet 3.5: High intelligence
            temperature=0.5,
            max_tokens=8000
        )

    def get_model_config(self, use_production_models=False):
        """Get model configuration based on environment"""
        if use_production_models:
            return {
                'pitch': self.production_pitch_llm,
                'design': self.production_design_llm,
                'technical': self.production_technical_llm,
                'editorial': self.production_editorial_llm
            }
        else:
            return {
                'pitch': self.pitch_llm,
                'design': self.design_llm,
                'technical': self.technical_llm,
                'editorial': self.editorial_llm
            }

    @agent
    def pitch_writer(self) -> Agent:
        # Use environment variable to determine if production models should be used
        use_production = os.getenv('USE_PRODUCTION_MODELS', 'false').lower() == 'true'
        models = self.get_model_config(use_production)

        return Agent(
            config=self.agents_config['pitch_writer'],
            verbose=True,
            llm=models['pitch'],
            allow_delegation=True,
            tools=[self.template_reader, self.design_guide_search, self.knowledge_explorer]
        )

    @agent
    def gameplay_designer(self) -> Agent:
        use_production = os.getenv('USE_PRODUCTION_MODELS', 'false').lower() == 'true'
        models = self.get_model_config(use_production)

        return Agent(
            config=self.agents_config['gameplay_designer'],
            verbose=True,
            llm=models['design'],
            allow_delegation=True,
            tools=[self.template_reader, self.design_guide_search, self.knowledge_explorer]
        )

    @agent
    def technical_architect(self) -> Agent:
        use_production = os.getenv('USE_PRODUCTION_MODELS', 'false').lower() == 'true'
        models = self.get_model_config(use_production)

        return Agent(
            config=self.agents_config['technical_architect'],
            verbose=True,
            llm=models['technical'],
            allow_delegation=True,
            tools=[self.design_guide_search, self.knowledge_explorer]
        )

    @agent
    def chief_editor(self) -> Agent:
        use_production = os.getenv('USE_PRODUCTION_MODELS', 'false').lower() == 'true'
        models = self.get_model_config(use_production)

        return Agent(
            config=self.agents_config['chief_editor'],
            verbose=True,
            llm=models['editorial'],
            allow_delegation=True,
            tools=[self.template_reader, self.design_guide_search, self.knowledge_explorer, self.template_validator]
        )

    @task
    def pitch_concept_task(self) -> Task:
        return Task(
            config=self.tasks_config['pitch_concept_task'],
            agent=self.pitch_writer()
        )

    @task
    def pitch_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['pitch_review_task'],
            agent=self.chief_editor()
        )

    @task
    def pitch_refinement_task(self) -> Task:
        return Task(
            config=self.tasks_config['pitch_refinement_task'],
            agent=self.pitch_writer()
        )

    @task
    def gameplay_mechanics_task(self) -> Task:
        return Task(
            config=self.tasks_config['gameplay_mechanics_task'],
            agent=self.gameplay_designer()
        )

    @task
    def gameplay_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['gameplay_review_task'],
            agent=self.chief_editor()
        )

    @task
    def gameplay_refinement_task(self) -> Task:
        return Task(
            config=self.tasks_config['gameplay_refinement_task'],
            agent=self.gameplay_designer()
        )

    @task
    def technical_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_implementation_task'],
            agent=self.technical_architect()
        )

    @task
    def gdd_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['gdd_integration_task'],
            agent=self.chief_editor()
        )

    @task
    def final_gdd_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_gdd_review_task'],
            agent=self.chief_editor()
        )

    @task
    def final_polish_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_polish_task'],
            agent=self.chief_editor()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GameDevs crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,  # Disable memory to avoid OpenAI dependency
            planning=False,  # Disable planning to avoid OpenAI dependency
            # Removed OpenAI embedder - CrewAI will work without embeddings
            # or you can configure a local embedding model if needed
            output_log_file="outputs/logs/crew_execution.log"
        )

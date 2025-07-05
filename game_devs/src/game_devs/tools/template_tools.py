"""
Template Integration Tools for CrewAI Game Development Crew

This module provides tools for agents to access the GDD template and design guide
to ensure professional, consistent document generation following best practices.
"""

from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import os


class GDDTemplateReaderInput(BaseModel):
    """Input schema for GDD Template Reader Tool."""
    section: Optional[str] = Field(None, description="Specific template section to retrieve (optional)")


class GDDTemplateReaderTool(BaseTool):
    name: str = "GDD Template Reader"
    description: str = (
        "Reads the Game Design Document template to understand required sections and formatting. "
        "Use this to ensure your output follows the professional GDD template structure. "
        "Can retrieve the full template or specific sections."
    )
    args_schema: Type[BaseModel] = GDDTemplateReaderInput

    def _run(self, section: Optional[str] = None) -> str:
        """Read the GDD template file and return its content."""
        try:
            # Use relative path from game_devs directory (where crew runs)
            template_path = "knowledge/game_design_document/template.mdx"

            if not os.path.exists(template_path):
                return f"Error: Template file not found at {template_path}"

            with open(template_path, 'r', encoding='utf-8') as file:
                content = file.read()

            if section:
                # Extract specific section if requested
                lines = content.split('\n')
                section_content = []
                in_section = False
                section_header = f"## {section}"

                for line in lines:
                    if line.startswith("## ") and in_section:
                        # End of current section
                        break
                    if line.startswith(section_header):
                        in_section = True
                        section_content.append(line)
                    elif in_section:
                        section_content.append(line)

                if section_content:
                    return "\n".join(section_content)
                else:
                    return f"Section '{section}' not found in template. Available sections include: Core Concept, Design Pillars, Game Mechanics, Narrative Overview, Visual and Audio Direction, Development Timeline"

            return content

        except Exception as e:
            return f"Error reading template: {str(e)}"


class DesignGuideSearchInput(BaseModel):
    """Input schema for Design Guide Search Tool."""
    query: str = Field(..., description="Search query to find relevant design guidance and best practices")


class DesignGuideSearchTool(BaseTool):
    name: str = "Design Guide Search"
    description: str = (
        "Searches the comprehensive game design guide for specific guidance, best practices, "
        "and examples related to game design document creation. Use this to find relevant "
        "advice for specific design challenges or to understand best practices for GDD sections."
    )
    args_schema: Type[BaseModel] = DesignGuideSearchInput

    def _run(self, query: str) -> str:
        """Search the design guide for relevant information."""
        try:
            # Use relative path from game_devs directory (where crew runs)
            guide_path = "knowledge/game_design_document/instructions.mdx"

            if not os.path.exists(guide_path):
                return f"Error: Design guide not found at {guide_path}"

            with open(guide_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Simple search implementation - find sections containing the query
            lines = content.split('\n')
            relevant_sections = []
            current_section = []
            current_header = ""

            query_lower = query.lower()

            for line in lines:
                if line.startswith('#'):
                    # Save previous section if it contains the query
                    if current_section and any(query_lower in text.lower() for text in current_section):
                        relevant_sections.append(f"{current_header}\n" + "\n".join(current_section))

                    # Start new section
                    current_header = line
                    current_section = []
                else:
                    current_section.append(line)

            # Check last section
            if current_section and any(query_lower in text.lower() for text in current_section):
                relevant_sections.append(f"{current_header}\n" + "\n".join(current_section))

            if relevant_sections:
                return "\n\n---\n\n".join(relevant_sections[:3])  # Return top 3 relevant sections
            else:
                # Fallback: return sections that might be relevant based on common terms
                fallback_terms = {
                    'pitch': ['Step 1: Define the Core Concept'],
                    'concept': ['Step 1: Define the Core Concept'],
                    'mechanics': ['Step 3: Outline Core Gameplay and Mechanics'],
                    'gameplay': ['Step 3: Outline Core Gameplay and Mechanics'],
                    'narrative': ['Step 4: Outline Narrative and World'],
                    'story': ['Step 4: Outline Narrative and World'],
                    'visual': ['Step 5: Define Visual Style and Audio Direction'],
                    'audio': ['Step 5: Define Visual Style and Audio Direction'],
                    'technical': ['Step 6: Determine Technical Requirements and Tools'],
                    'timeline': ['Step 7: Outline Scope, Milestones, and Next Steps'],
                    'scope': ['Step 7: Outline Scope, Milestones, and Next Steps']
                }

                for term, sections in fallback_terms.items():
                    if term in query_lower:
                        # Find and return the relevant section
                        for section_name in sections:
                            if section_name in content:
                                start_idx = content.find(section_name)
                                if start_idx != -1:
                                    # Find next major section
                                    next_section = content.find('\n### Step', start_idx + 1)
                                    if next_section == -1:
                                        next_section = content.find('\n## ', start_idx + 1)

                                    if next_section != -1:
                                        return content[start_idx:next_section]
                                    else:
                                        return content[start_idx:start_idx + 2000]  # Return reasonable chunk

                return f"No specific guidance found for '{query}'. Consider searching for: pitch, concept, mechanics, gameplay, narrative, visual, audio, technical, timeline, or scope."

        except Exception as e:
            return f"Error searching design guide: {str(e)}"


class KnowledgeDirectoryInput(BaseModel):
    """Input schema for Knowledge Directory Tool."""
    path: Optional[str] = Field("", description="Specific subdirectory to explore (optional)")


class KnowledgeDirectoryTool(BaseTool):
    name: str = "Knowledge Directory Explorer"
    description: str = (
        "Explores the knowledge directory to find available templates, guides, and resources. "
        "Use this to discover what knowledge files are available for reference."
    )
    args_schema: Type[BaseModel] = KnowledgeDirectoryInput

    def _run(self, path: str = "") -> str:
        """Explore the knowledge directory structure."""
        try:
            base_path = "knowledge"
            full_path = os.path.join(base_path, path) if path else base_path

            if not os.path.exists(full_path):
                return f"Error: Path not found at {full_path}"

            result = []
            result.append(f"Contents of {full_path}:")
            result.append("=" * 50)

            for item in sorted(os.listdir(full_path)):
                item_path = os.path.join(full_path, item)
                if os.path.isdir(item_path):
                    result.append(f"📁 {item}/")
                else:
                    # Get file size for reference
                    size = os.path.getsize(item_path)
                    result.append(f"📄 {item} ({size} bytes)")

            return "\n".join(result)

        except Exception as e:
            return f"Error exploring directory: {str(e)}"


class GDDTemplateTools:
    """
    Collection of template integration tools for the CrewAI game development crew.
    Provides easy access to all template-related tools.
    """

    def __init__(self):
        self.template_reader = GDDTemplateReaderTool()
        self.guide_search = DesignGuideSearchTool()
        self.directory_explorer = KnowledgeDirectoryTool()

    @property
    def all_tools(self):
        """Returns a list of all available template tools."""
        return [self.template_reader, self.guide_search, self.directory_explorer]

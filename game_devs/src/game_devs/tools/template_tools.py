"""
Template Integration Tools for CrewAI Game Development Crew

This module provides tools for agents to access the GDD template and design guide
to ensure professional, consistent document generation following best practices.
"""

from crewai.tools import BaseTool
from typing import Type, Optional, List, Dict
from pydantic import BaseModel, Field
import os
import re


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
                # Try alternative paths
                alt_paths = [
                    "../knowledge/game_design_document/template.mdx",
                    "game_devs/knowledge/game_design_document/template.mdx",
                    os.path.join(os.getcwd(), "knowledge/game_design_document/template.mdx")
                ]

                for alt_path in alt_paths:
                    if os.path.exists(alt_path):
                        template_path = alt_path
                        break
                else:
                    return f"❌ Error: Template file not found at {template_path} or alternative paths"

            with open(template_path, 'r', encoding='utf-8') as file:
                content = file.read()

            if not content.strip():
                return "❌ Error: Template file is empty"

            if section:
                # Extract specific section if requested
                section_content = self._extract_section(content, section)
                if section_content:
                    return section_content
                else:
                    available_sections = self._get_available_sections(content)
                    return f"❌ Section '{section}' not found in template.\n\n📋 Available sections:\n{chr(10).join(available_sections)}"

            return content

        except UnicodeDecodeError:
            return "❌ Error: Template file contains invalid characters. Please ensure it's UTF-8 encoded."
        except PermissionError:
            return "❌ Error: Permission denied reading template file."
        except Exception as e:
            return f"❌ Error reading template: {str(e)}"

    def _extract_section(self, content: str, section: str) -> Optional[str]:
        """Extract a specific section from the template."""
        lines = content.split('\n')
        section_content = []
        in_section = False

        # Try different section header formats
        possible_headers = [
            f"## {section}",
            f"### {section}",
            f"# {section}",
            section  # Exact match
        ]

        for line in lines:
            # Check if we've reached the next section
            if line.strip().startswith("#") and in_section and section_content:
                # Check if this is a new section at the same or higher level
                current_level = len(line) - len(line.lstrip('#'))
                section_level = 2  # Assume we're looking for ## level sections
                if current_level <= section_level:
                    break

            # Check if this line starts our target section
            if not in_section:
                for header in possible_headers:
                    if line.strip().startswith(header):
                        in_section = True
                        section_content.append(line)
                        break
            elif in_section:
                section_content.append(line)

        return "\n".join(section_content) if section_content else None

    def _get_available_sections(self, content: str) -> List[str]:
        """Get list of available sections in the template."""
        sections = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('##') and not line.startswith('###'):
                # Extract section name
                section_name = line.lstrip('#').strip()
                sections.append(f"• {section_name}")

        return sections if sections else ["• No sections found"]


class TemplateValidationInput(BaseModel):
    """Input schema for Template Validation Tool."""
    document_content: str = Field(..., description="The GDD document content to validate against template")


class TemplateValidationTool(BaseTool):
    name: str = "Template Structure Validator"
    description: str = (
        "Validates that a generated GDD document follows the template structure and contains "
        "all required sections. Returns a validation report with missing sections and formatting issues."
    )
    args_schema: Type[BaseModel] = TemplateValidationInput

    def _run(self, document_content: str) -> str:
        """Validate document structure against template."""
        try:
            # Get template structure
            template_reader = GDDTemplateReaderTool()
            template_content = template_reader._run()

            if template_content.startswith("❌"):
                return f"❌ Cannot validate: {template_content}"

            # Extract required sections from template
            required_sections = self._extract_required_sections(template_content)

            # Extract sections from document
            document_sections = self._extract_document_sections(document_content)

            # Validate structure
            validation_report = self._generate_validation_report(required_sections, document_sections)

            return validation_report

        except Exception as e:
            return f"❌ Error during validation: {str(e)}"

    def _extract_required_sections(self, template_content: str) -> List[str]:
        """Extract required sections from template."""
        sections = []
        lines = template_content.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('##') and not line.startswith('###'):
                section_name = line.lstrip('#').strip()
                sections.append(section_name)

        return sections

    def _extract_document_sections(self, document_content: str) -> List[str]:
        """Extract sections from the document being validated."""
        sections = []
        lines = document_content.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('##') and not line.startswith('###'):
                section_name = line.lstrip('#').strip()
                sections.append(section_name)

        return sections

    def _generate_validation_report(self, required_sections: List[str], document_sections: List[str]) -> str:
        """Generate a validation report."""
        report = ["📋 Template Structure Validation Report", "=" * 50]

        # Check for missing sections
        missing_sections = []
        for required in required_sections:
            if not any(self._sections_match(required, doc_section) for doc_section in document_sections):
                missing_sections.append(required)

        # Check for extra sections
        extra_sections = []
        for doc_section in document_sections:
            if not any(self._sections_match(doc_section, required) for required in required_sections):
                extra_sections.append(doc_section)

        # Generate report
        if not missing_sections and not extra_sections:
            report.append("✅ Document structure is complete and follows template!")
        else:
            if missing_sections:
                report.append(f"❌ Missing {len(missing_sections)} required section(s):")
                for section in missing_sections:
                    report.append(f"  • {section}")

            if extra_sections:
                report.append(f"ℹ️  Found {len(extra_sections)} additional section(s):")
                for section in extra_sections:
                    report.append(f"  • {section}")

        report.append("")
        report.append("📊 Section Coverage:")
        report.append(f"Required sections: {len(required_sections)}")
        report.append(f"Document sections: {len(document_sections)}")
        report.append(f"Missing sections: {len(missing_sections)}")

        return "\n".join(report)

    def _sections_match(self, section1: str, section2: str) -> bool:
        """Check if two section names match (case-insensitive, flexible matching)."""
        # Normalize section names for comparison
        s1 = re.sub(r'[^a-zA-Z0-9\s]', '', section1.lower()).strip()
        s2 = re.sub(r'[^a-zA-Z0-9\s]', '', section2.lower()).strip()

        # Direct match
        if s1 == s2:
            return True

        # Partial match (one contains the other)
        if s1 in s2 or s2 in s1:
            return True

        return False


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
                # Try alternative paths
                alt_paths = [
                    "../knowledge/game_design_document/instructions.mdx",
                    "game_devs/knowledge/game_design_document/instructions.mdx",
                    os.path.join(os.getcwd(), "knowledge/game_design_document/instructions.mdx")
                ]

                for alt_path in alt_paths:
                    if os.path.exists(alt_path):
                        guide_path = alt_path
                        break
                else:
                    return f"❌ Error: Design guide not found at {guide_path} or alternative paths"

            with open(guide_path, 'r', encoding='utf-8') as file:
                content = file.read()

            if not content.strip():
                return "❌ Error: Design guide file is empty"

            # Perform enhanced search
            relevant_sections = self._enhanced_search(content, query)

            if relevant_sections:
                return f"🔍 Search results for '{query}':\n\n" + "\n\n---\n\n".join(relevant_sections)
            else:
                # Provide helpful suggestions
                suggestions = self._get_search_suggestions(query)
                return f"🔍 No specific guidance found for '{query}'.\n\n💡 Try searching for:\n{suggestions}"

        except UnicodeDecodeError:
            return "❌ Error: Design guide file contains invalid characters. Please ensure it's UTF-8 encoded."
        except PermissionError:
            return "❌ Error: Permission denied reading design guide file."
        except Exception as e:
            return f"❌ Error searching design guide: {str(e)}"

    def _enhanced_search(self, content: str, query: str) -> List[str]:
        """Enhanced search with better matching and ranking."""
        lines = content.split('\n')
        relevant_sections = []
        current_section = []
        current_header = ""

        query_terms = query.lower().split()

        for line in lines:
            if line.startswith('#'):
                # Process previous section
                if current_section:
                    score = self._calculate_relevance_score(current_section, query_terms)
                    if score > 0:
                        relevant_sections.append((score, f"{current_header}\n" + "\n".join(current_section)))

                # Start new section
                current_header = line
                current_section = []
            else:
                current_section.append(line)

        # Check last section
        if current_section:
            score = self._calculate_relevance_score(current_section, query_terms)
            if score > 0:
                relevant_sections.append((score, f"{current_header}\n" + "\n".join(current_section)))

        # Sort by relevance score and return top results
        relevant_sections.sort(key=lambda x: x[0], reverse=True)
        return [section[1] for section in relevant_sections[:3]]

    def _calculate_relevance_score(self, section_lines: List[str], query_terms: List[str]) -> float:
        """Calculate relevance score for a section."""
        section_text = " ".join(section_lines).lower()

        score = 0
        for term in query_terms:
            # Exact matches get higher score
            score += section_text.count(term) * 2

            # Partial matches get lower score
            for word in section_text.split():
                if term in word:
                    score += 0.5

        return score

    def _get_search_suggestions(self, query: str) -> str:
        """Get search suggestions based on common terms."""
        suggestions = {
            'pitch': ['concept', 'elevator pitch', 'game hook', 'core gameplay'],
            'concept': ['core concept', 'design pillars', 'game vision'],
            'mechanics': ['gameplay mechanics', 'core loop', 'game systems'],
            'gameplay': ['core gameplay', 'player actions', 'game loop'],
            'narrative': ['story', 'characters', 'world building'],
            'story': ['narrative', 'plot', 'characters'],
            'visual': ['art style', 'visual design', 'graphics'],
            'audio': ['sound design', 'music', 'audio direction'],
            'technical': ['implementation', 'architecture', 'tools'],
            'timeline': ['development timeline', 'milestones', 'schedule'],
            'scope': ['project scope', 'constraints', 'limitations']
        }

        query_lower = query.lower()
        suggested_terms = []

        for key, terms in suggestions.items():
            if key in query_lower:
                suggested_terms.extend(terms)

        if not suggested_terms:
            suggested_terms = ['concept', 'mechanics', 'gameplay', 'narrative', 'visual', 'audio', 'technical', 'timeline', 'scope']

        return "\n".join(f"  • {term}" for term in suggested_terms[:5])


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

            # Try alternative paths if not found
            if not os.path.exists(full_path):
                alt_paths = [
                    f"../{base_path}",
                    f"game_devs/{base_path}",
                    os.path.join(os.getcwd(), base_path)
                ]

                for alt_path in alt_paths:
                    test_path = os.path.join(alt_path, path) if path else alt_path
                    if os.path.exists(test_path):
                        full_path = test_path
                        break
                else:
                    return f"❌ Error: Knowledge directory not found at {full_path} or alternative paths"

            result = []
            result.append(f"📁 Contents of {full_path}:")
            result.append("=" * 50)

            items = sorted(os.listdir(full_path))
            if not items:
                result.append("📭 Directory is empty")
                return "\n".join(result)

            for item in items:
                item_path = os.path.join(full_path, item)
                if os.path.isdir(item_path):
                    # Count items in subdirectory
                    try:
                        subitem_count = len(os.listdir(item_path))
                        result.append(f"📁 {item}/ ({subitem_count} items)")
                    except PermissionError:
                        result.append(f"📁 {item}/ (access denied)")
                else:
                    # Get file size and type
                    try:
                        size = os.path.getsize(item_path)
                        size_str = self._format_file_size(size)
                        file_type = self._get_file_type(item)
                        result.append(f"{file_type} {item} ({size_str})")
                    except (OSError, PermissionError):
                        result.append(f"📄 {item} (inaccessible)")

            return "\n".join(result)

        except PermissionError:
            return f"❌ Error: Permission denied accessing directory {full_path}"
        except Exception as e:
            return f"❌ Error exploring directory: {str(e)}"

    def _format_file_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    def _get_file_type(self, filename: str) -> str:
        """Get file type icon based on extension."""
        ext = os.path.splitext(filename)[1].lower()

        type_map = {
            '.md': '📝', '.mdx': '📝', '.txt': '📄',
            '.py': '🐍', '.js': '📜', '.ts': '📜',
            '.json': '📊', '.yaml': '⚙️', '.yml': '⚙️',
            '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️',
            '.pdf': '📕', '.doc': '📄', '.docx': '📄'
        }

        return type_map.get(ext, '📄')


class GDDTemplateTools:
    """Collection of all template tools for easy access."""

    def __init__(self):
        self.template_reader = GDDTemplateReaderTool()
        self.design_guide_search = DesignGuideSearchTool()
        self.knowledge_explorer = KnowledgeDirectoryTool()
        self.template_validator = TemplateValidationTool()

    @property
    def all_tools(self):
        """Return all available tools."""
        return [
            self.template_reader,
            self.design_guide_search,
            self.knowledge_explorer,
            self.template_validator
        ]

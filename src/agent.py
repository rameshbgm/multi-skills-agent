"""
Multi-Skills Agent - Cost-Effective AI Agent with MCP Tools

Powered by Claude 3 Haiku (cheapest model) with FREE MCP integrations.
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from .mcp import ALL_MCP_TOOLS

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(log_dir / 'agent.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


class MultiSkillsAgent:
    """
    Multi-Skills AI Agent with MCP tool integrations.
    
    Uses claude-3-haiku for cost-effectiveness.
    All MCP tools are FREE (no external API keys needed).
    """
    
    def __init__(self, skills_dir: Optional[str] = None):
        """Initialize the agent."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not found")
        
        self.skills_dir = Path(skills_dir) if skills_dir else Path(__file__).parent / "skills"
        
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0.5,
            max_tokens=250,
            api_key=self.api_key
        )
        
        self.skills = self._discover_skills()
        self.system_prompt = self._build_system_prompt()
        self.memory = MemorySaver()
        
        self.agent_executor = create_react_agent(
            self.llm,
            tools=ALL_MCP_TOOLS,
            checkpointer=self.memory,
            prompt=self.system_prompt
        )
        
        logger.info(f"Agent initialized: {len(self.skills)} skills, {len(ALL_MCP_TOOLS)} tools")
    
    def _discover_skills(self) -> dict:
        """Discover all skills in the skills directory."""
        skills = {}
        if not self.skills_dir.exists():
            return skills
        
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir() and not skill_path.name.startswith('_'):
                skill_file = skill_path / "SKILL.md"
                if skill_file.exists():
                    try:
                        content = skill_file.read_text(encoding='utf-8')
                        skill_name = skill_path.name.replace('_', ' ').title()
                        skills[skill_name] = content
                    except Exception as e:
                        logger.error(f"Failed to load skill {skill_path.name}: {e}")
        return skills
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt from all skills."""
        skill_names = list(self.skills.keys())
        
        prompt = f"""You are a Multi-Skills AI Agent with {len(skill_names)} skills and MCP tools for real-time data.

Skills: {', '.join(skill_names)}

MCP Tools Available:
- Weather: get_current_weather, get_weather_forecast, get_air_quality
- Stocks: get_stock_quote, get_stock_history, get_company_info
- News: get_top_headlines, search_news, get_news_sources
- Database: get_all_employees, get_employee_by_id, search_employees, get_department_stats

Instructions:
1. Identify relevant skill for the query
2. Use MCP tools when real-time data is needed
3. Keep responses concise (max 250 tokens)
4. Follow skill guidelines and guardrails

"""
        for name, content in self.skills.items():
            prompt += f"\n{'='*40}\nSKILL: {name.upper()}\n{'='*40}\n{content}\n"
        
        return prompt
    
    def get_available_skills(self) -> list:
        """Get list of available skills."""
        return list(self.skills.keys())
    
    def process_request(self, user_message: str, thread_id: Optional[str] = None) -> str:
        """Process a user request."""
        thread_id = thread_id or "default"
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            result = self.agent_executor.invoke(
                {"messages": [("user", user_message)]},
                config=config
            )
            messages = result.get("messages", [])
            return messages[-1].content if messages else "No response"
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)}"
    
    def reset_conversation(self, thread_id: str = "default") -> None:
        """Reset conversation memory."""
        self.memory = MemorySaver()
        self.agent_executor = create_react_agent(
            self.llm,
            tools=ALL_MCP_TOOLS,
            checkpointer=self.memory,
            prompt=self.system_prompt
        )

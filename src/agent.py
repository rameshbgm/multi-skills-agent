import os
import logging
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(log_dir / 'agent.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


class MultiSkillsAgent:
    """
    A generalist AI agent that dynamically loads and applies multiple skills.
    
    This agent demonstrates the 'Build Skills, Not Agents' architecture where
    one agent can handle multiple domains by injecting skill-specific knowledge
    into its system prompt.
    """
    
    def __init__(self, skills_dir: Optional[str] = None):
        """
        Initialize the Multi-Skills Agent.
        
        Args:
            skills_dir: Optional path to skills directory. If None, uses default location.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables.")
        
        # Skills directory
        if skills_dir:
            self.skills_dir = Path(skills_dir)
        else:
            self.skills_dir = Path(__file__).parent / "skills"
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=self.api_key
        )
        
        # Load all skills and build system prompt
        self.skills = self._discover_skills()
        self.system_prompt = self._build_system_prompt()
        
        # Initialize Memory
        self.memory = MemorySaver()
        
        # Build Agent (no tools - purely skill-based)
        self.agent_executor = create_react_agent(
            self.llm,
            tools=[],  # No tools - purely knowledge-based
            checkpointer=self.memory,
            prompt=self.system_prompt
        )
        
        logger.info(f"MultiSkillsAgent initialized with {len(self.skills)} skills.")
    
    def _discover_skills(self) -> dict:
        """
        Automatically discover all skills in the skills directory.
        
        Returns:
            Dictionary mapping skill names to their content.
        """
        skills = {}
        
        if not self.skills_dir.exists():
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return skills
        
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir() and not skill_path.name.startswith('_'):
                skill_file = skill_path / "SKILL.md"
                if skill_file.exists():
                    try:
                        content = skill_file.read_text(encoding='utf-8')
                        skill_name = skill_path.name.replace('_', ' ').title()
                        skills[skill_name] = content
                        logger.info(f"Loaded skill: {skill_name}")
                    except Exception as e:
                        logger.error(f"Failed to load skill {skill_path.name}: {e}")
        
        return skills
    
    def _build_system_prompt(self) -> str:
        """
        Build the system prompt by combining all loaded skills.
        
        Returns:
            Complete system prompt string.
        """
        skill_names = list(self.skills.keys())
        
        base_prompt = f"""You are a Multi-Skills AI Agent with expertise in multiple domains.

You have {len(skill_names)} specialized skills:
{chr(10).join(f'  {i+1}. {name}' for i, name in enumerate(skill_names))}

When a user asks you something:
1. Identify which skill(s) are most relevant to their query
2. Apply the specific guidelines, communication style, and guardrails defined for that skill
3. If the query spans multiple skills, integrate knowledge appropriately
4. If no skill is directly applicable, use your general knowledge while maintaining professional standards

Below are your detailed skill definitions. Follow the instructions, guardrails, and response formats specified in each skill.

"""
        # Add each skill's content
        for i, (name, content) in enumerate(self.skills.items(), 1):
            base_prompt += f"\n{'='*60}\n"
            base_prompt += f"SKILL {i}: {name.upper()}\n"
            base_prompt += f"{'='*60}\n\n"
            base_prompt += content
            base_prompt += "\n"
        
        # Add general guidelines
        base_prompt += f"""
{'='*60}
GENERAL GUIDELINES
{'='*60}

1. **Be Professional**: Maintain a helpful, respectful, and professional tone.
2. **Be Accurate**: Provide accurate information within the scope of your skills.
3. **Know Your Limits**: If a question is outside your expertise, say so clearly.
4. **Respect Guardrails**: Always follow the safety guidelines defined in each skill.
5. **Adapt Communication**: Match your communication style to the relevant skill.
6. **Ask for Clarity**: If a request is ambiguous, ask clarifying questions.
7. **Stay in Character**: When using a skill, embody that role fully.
"""
        
        return base_prompt
    
    def get_available_skills(self) -> list:
        """
        Get a list of all available skills.
        
        Returns:
            List of skill names.
        """
        return list(self.skills.keys())
    
    def process_request(self, user_message: str, thread_id: Optional[str] = None) -> str:
        """
        Process a user request using the multi-skills agent.
        
        Args:
            user_message: The user's input message.
            thread_id: Optional conversation thread ID for memory.
            
        Returns:
            The agent's response.
        """
        if not thread_id:
            thread_id = "default_thread"
        
        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(f"Processing request for thread {thread_id}: {user_message[:100]}...")
        
        try:
            inputs = {"messages": [("user", user_message)]}
            result = self.agent_executor.invoke(inputs, config=config)
            
            messages = result.get("messages", [])
            if messages:
                last_msg = messages[-1]
                return last_msg.content
            else:
                return "I'm not sure how to respond to that."
                
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return f"I encountered a system error: {str(e)}"
    
    def reset_conversation(self, thread_id: str = "default_thread") -> None:
        """
        Reset the conversation memory for a specific thread.
        
        Note: With MemorySaver, this creates a new memory state.
        """
        logger.info(f"Resetting conversation for thread: {thread_id}")
        # Re-initialize memory to reset all conversations
        self.memory = MemorySaver()
        self.agent_executor = create_react_agent(
            self.llm,
            tools=[],
            checkpointer=self.memory,
            prompt=self.system_prompt
        )

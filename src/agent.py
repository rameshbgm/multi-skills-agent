import os
import logging
from typing import Optional, List
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Imports from tool modules
from src.tools.roaming_tools import (
    verify_customer_account, check_roaming_eligibility, get_roaming_rates,
    activate_roaming_service, get_customer_balance, send_activation_confirmation
)
from src.tools.broadband_tools import (
    check_service_availability, get_available_slots, schedule_installation,
    check_installation_status, reschedule_appointment, cancel_appointment
)
from src.tools.fee_waiver_tools import (
    check_customer_history, evaluate_waiver_eligibility, process_waiver,
    get_waiver_policy, send_waiver_notification, recommend_prevention, escalate_waiver
)

# Setup logging
logging.basicConfig(
    filename='logs/agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

class TelecomSkillsAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in env.")

        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            api_key=self.api_key
        )
        
        # Gather Tools
        self.tools = [
            # Roaming
            verify_customer_account, check_roaming_eligibility, get_roaming_rates,
            activate_roaming_service, get_customer_balance, send_activation_confirmation,
            # Broadband
            check_service_availability, get_available_slots, schedule_installation,
            check_installation_status, reschedule_appointment, cancel_appointment,
            # Fee Waiver
            check_customer_history, evaluate_waiver_eligibility, process_waiver,
            get_waiver_policy, send_waiver_notification, recommend_prevention, escalate_waiver
        ]
        
        # Load Skills Content for System Prompt
        self.system_prompt = self._build_system_prompt()
        
        # Initialize Memory
        # In actual usage we pass the saver to compile
        self.memory = MemorySaver()
        
        # Build Agent
        self.agent_executor = create_react_agent(
            self.llm, 
            self.tools, 
            checkpointer=self.memory,
            prompt=self.system_prompt
        )
        
        logger.info("TelecomSkillsAgent initialized successfully.")

    def _load_skill_file(self, relative_path: str) -> str:
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__)) # src/..
            path = os.path.join(base_dir, relative_path)
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load skill file {relative_path}: {e}")
            return ""

    def _build_system_prompt(self) -> str:
        roaming_skill = self._load_skill_file("src/skills/roaming_activation/SKILL.md")
        broadband_skill = self._load_skill_file("src/skills/broadband_installation/SKILL.md")
        waiver_skill = self._load_skill_file("src/skills/fee_waiver/SKILL.md")
        
        base_prompt = """You are a Telecom Customer Service AI Agent. 
You are one agent with multiple capabilities.
You have three main areas of expertise (Skills):

1. Roaming Activation
2. Broadband Installation checking & scheduling
3. Late Payment Fee Waivers

Below are the strictly defined SKILL protocols you must follow using the available tools.
Read these instructions carefully. When a user asks for something, identify which skill applies and follow the specific step-by-step process and guardrails defined in that skill.

"""
        full_prompt = f"{base_prompt}\n\n=== SKILL 1: ROAMING ===\n{roaming_skill}\n\n=== SKILL 2: BROADBAND ===\n{broadband_skill}\n\n=== SKILL 3: FEE WAIVER ===\n{waiver_skill}\n\n"
        full_prompt += """
GENERAL RULES:
- Be polite, professional, and concise.
- If the user request is ambiguous, ask clarifying questions.
- VERIFY IDENTITY: Almost all actions require knowing who the customer is (Customer ID). If you don't know, ASK.
- Use the tools provided to perform actions. Do not hallucinate data.
- Determine the tool to use based on the user's intent.
"""
        return full_prompt

    def process_customer_request(self, customer_message: str, thread_id: Optional[str] = None) -> str:
        """
        Processes a single turn of conversation.
        """
        if not thread_id:
            # If no thread_id, we can generate one or just use a default, 
            # but usually the CLI manages this.
            thread_id = "default_thread"

        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(f"Processing request for thread {thread_id}: {customer_message}")
        
        try:
            inputs = {"messages": [("user", customer_message)]}
            
            # The agent returns the full state or a chunk. We want the final response.
            # create_react_agent returns a CompiledGraph. invoke returns dict with 'messages'.
            result = self.agent_executor.invoke(inputs, config=config)
            
            # Extract the last message content
            messages = result.get("messages", [])
            if messages:
                last_msg = messages[-1]
                return last_msg.content
            else:
                return "I'm not sure how to respond to that."
                
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return f"I encountered an system error: {str(e)}"

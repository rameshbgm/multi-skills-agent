from src.tools.fee_waiver_tools import evaluate_waiver_eligibility
from src.agent import TelecomSkillsAgent
from langchain_core.messages import HumanMessage

def test_tool_direct():
    print("Testing tool directly...")
    try:
        result = evaluate_waiver_eligibility.invoke({"customer_id": "CUST001", "hardship_reason": "hospital"})
        print(f"Tool Result: {result}")
    except Exception as e:
        print(f"Tool Direct Error: {e}")
        import traceback
        traceback.print_exc()

def test_agent_run():
    print("\nTesting agent run...")
    try:
        agent = TelecomSkillsAgent()
        # We access the internal executor to see if we can run it step by step or just invoke
        result = agent.agent_executor.invoke(
            {"messages": [HumanMessage(content="I'm CUST001. I missed payment due to hospital. Waive fee.")]},
            config={"configurable": {"thread_id": "debug_1"}}
        )
        print("Agent Result OK")
    except Exception as e:
        print(f"Agent Run Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tool_direct()
    test_agent_run()

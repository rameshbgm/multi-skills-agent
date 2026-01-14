import sys
import uuid
import logging
from src.agent import TelecomSkillsAgent

# Configure basic logging to avoid cluttering CLI unless verbose
# The agent.py sets up file logging. We'll leave stdout clean.

def print_banner():
    banner = """
    =====================================================
    |         TELECOM SKILLS AGENT v1.0                 |
    |  Roaming | Broadband | Fee Waiver Specialists     |
    =====================================================
    Type 'quit' or 'exit' to leave.
    Type 'clear' to start a new conversation.
    Type 'examples' to see what you can ask.
    """
    print(banner)

def print_examples():
    examples = """
    [Roaming]
    - "I'm travelling to Japan next week for 10 days. Customer CUST001."
    - "Can you activate a weekly pass for France for me? Account CUST001."

    [Broadband]
    - "Is fiber available at 123 Main St, zip 10001?"
    - "I need to book an installation for next Monday. CUST002."

    [Fee Waiver]
    - "I was charged a late fee but I was in the hospital. Can you waive it? CUST001."
    - "Why is my bill so high? I demand a refund! CUST003."
    """
    print(examples)

def main():
    print_banner()
    
    try:
        agent = TelecomSkillsAgent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    # Generate a random thread ID for the session
    current_thread_id = str(uuid.uuid4())
    print(f"Session ID: {current_thread_id}\n")

    while True:
        try:
            user_input = input("Customer >> ").strip()
            
            if not user_input:
                continue
                
            command = user_input.lower()
            
            if command in ["quit", "exit"]:
                print("Goodbye!")
                break
                
            if command == "clear":
                current_thread_id = str(uuid.uuid4())
                print(f"--- Conversation cleared. New Session ID: {current_thread_id} ---")
                continue
                
            if command == "examples":
                print_examples()
                continue
            
            # Process Request
            print("Agent is thinking...", end="\r", flush=True)
            response = agent.process_customer_request(user_input, thread_id=current_thread_id)
            
            # Clear "thinking" line
            print(" " * 20, end="\r")
            
            print(f"Agent >> {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

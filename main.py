import sys
import uuid
from src.agent import MultiSkillsAgent


def print_banner(skills: list):
    """Print the welcome banner with available skills."""
    skills_text = " | ".join(skills) if skills else "No skills loaded"
    
    banner = f"""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                   MULTI-SKILLS AGENT v2.0                         ║
    ║           "Build Skills, Not Agents" Architecture                 ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║  Available Skills:                                                ║
    ║  {skills_text:<64}║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║  Commands:                                                        ║
    ║    'skills'  - List all available skills                          ║
    ║    'examples'- Show example interactions                          ║
    ║    'clear'   - Start a new conversation                           ║
    ║    'quit'    - Exit the application                               ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_skills(skills: list):
    """Print detailed list of available skills."""
    print("\n📚 Available Skills:\n")
    for i, skill in enumerate(skills, 1):
        print(f"   {i}. {skill}")
    print()


def print_examples():
    """Print example interactions for each skill."""
    examples = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                      EXAMPLE INTERACTIONS                          ║
    ╠═══════════════════════════════════════════════════════════════════╣

    💰 Financial Analyst:
       • "Should I invest in index funds or individual stocks?"
       • "Explain the P/E ratio and how to use it"
       • "What's a good strategy for retirement savings?"

    📐 Maths Teacher:
       • "Solve the equation 3x² - 12x + 9 = 0"
       • "Explain derivatives with a real-world example"
       • "What is 15% of 240?"

    😂 Comedian:
       • "Tell me a joke"
       • "I need a laugh, my day has been terrible"
       • "Write a funny story about working from home"

    🏥 Doctor:
       • "What causes headaches?"
       • "How much water should I drink daily?"
       • "What are the benefits of regular exercise?"

    ⚖️ Lawyer:
       • "What makes a contract legally binding?"
       • "Explain the difference between civil and criminal law"
       • "What are my rights as a tenant?"

    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(examples)


def main():
    """Main entry point for the Multi-Skills Agent CLI."""
    try:
        agent = MultiSkillsAgent()
        skills = agent.get_available_skills()
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return

    print_banner(skills)
    
    # Generate a random thread ID for the session
    current_thread_id = str(uuid.uuid4())
    print(f"    Session ID: {current_thread_id[:8]}...\n")

    while True:
        try:
            user_input = input("You >> ").strip()
            
            if not user_input:
                continue
                
            command = user_input.lower()
            
            if command in ["quit", "exit", "q"]:
                print("👋 Goodbye! Thanks for using Multi-Skills Agent.")
                break
                
            if command == "clear":
                agent.reset_conversation(current_thread_id)
                current_thread_id = str(uuid.uuid4())
                print(f"🔄 Conversation cleared. New Session: {current_thread_id[:8]}...\n")
                continue
                
            if command == "examples":
                print_examples()
                continue
            
            if command == "skills":
                print_skills(skills)
                continue
            
            # Process Request
            print("🤔 Thinking...", end="\r", flush=True)
            response = agent.process_request(user_input, thread_id=current_thread_id)
            
            # Clear "thinking" line
            print(" " * 20, end="\r")
            
            print(f"\n🤖 Agent:\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()

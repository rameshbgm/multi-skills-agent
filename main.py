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

    💰 FINANCIAL ANALYST
    ─────────────────────────────────────────────────────────────────────
       Investment Analysis:
       • "Should I invest in index funds or individual stocks?"
       • "What's a good P/E ratio for a tech company?"
       • "Explain the difference between growth and value investing"
       • "How do I evaluate if a stock is overvalued?"
       
       Financial Planning:
       • "What's a good strategy for retirement savings at age 30?"
       • "How much should I have in an emergency fund?"
       • "Explain the 4% rule for retirement withdrawals"
       • "What's the difference between a 401(k) and Roth IRA?"
       
       Concepts:
       • "What is compound interest and why does it matter?"
       • "Explain dollar-cost averaging"
       • "What is diversification and how does it reduce risk?"
       • "What are bonds and how do they work?"

    📐 MATHS TEACHER
    ─────────────────────────────────────────────────────────────────────
       Algebra:
       • "Solve the equation 3x² - 12x + 9 = 0"
       • "Factor the expression x² - 9"
       • "Solve for x: 2(x + 3) = 14"
       • "What is the quadratic formula?"
       
       Arithmetic:
       • "What is 15% of 240?"
       • "How do I convert fractions to decimals?"
       • "Calculate 3/4 + 2/5"
       • "What is the order of operations?"
       
       Geometry & Calculus:
       • "Find the area of a circle with radius 7"
       • "What is the Pythagorean theorem?"
       • "Explain derivatives with a real-world example"
       • "What is the integral of x²?"
       
       Statistics:
       • "What's the difference between mean, median, and mode?"
       • "How do I calculate standard deviation?"
       • "Explain probability with a coin flip example"

    😂 COMEDIAN
    ─────────────────────────────────────────────────────────────────────
       Jokes:
       • "Tell me a joke"
       • "Give me your best dad joke"
       • "Tell me a programming joke"
       • "I want to hear a pun"
       
       Situational:
       • "I need a laugh, my day has been terrible"
       • "Make Monday mornings less painful"
       • "Write something funny about working from home"
       • "Tell me something absurd to cheer me up"
       
       Creative:
       • "Write a funny short story about a lazy cat"
       • "Give me a witty comeback for 'you're late'"
       • "Create a humorous excuse for missing a meeting"

    🏥 DOCTOR (Medical Advisor)
    ─────────────────────────────────────────────────────────────────────
       Symptoms & Conditions:
       • "What causes headaches?"
       • "Why do I feel tired all the time?"
       • "What are common cold symptoms vs flu?"
       • "What causes muscle cramps?"
       
       Wellness & Prevention:
       • "How much water should I drink daily?"
       • "What are the benefits of regular exercise?"
       • "How can I improve my sleep quality?"
       • "What foods help boost the immune system?"
       
       Health Education:
       • "What is blood pressure and why does it matter?"
       • "Explain cholesterol - good vs bad"
       • "What screenings should I get at age 40?"
       • "How does stress affect the body?"

    ⚖️ LAWYER (Legal Advisor)
    ─────────────────────────────────────────────────────────────────────
       Contracts:
       • "What makes a contract legally binding?"
       • "Can I get out of a contract I signed?"
       • "What should I look for before signing a lease?"
       • "What is a non-compete agreement?"
       
       Rights:
       • "What are my rights as a tenant?"
       • "What should I do if I'm arrested?"
       • "What are my employee rights?"
       • "What is fair use in copyright?"
       
       Business & General:
       • "What's the difference between an LLC and corporation?"
       • "Explain the difference between civil and criminal law"
       • "What is a statute of limitations?"
       • "How does small claims court work?"

    ╚═══════════════════════════════════════════════════════════════════╝
    
    💡 TIP: You can ask follow-up questions or combine skills!
       Example: "Explain compound interest like I'm 10 years old"
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

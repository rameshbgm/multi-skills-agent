"""
Multi-Skills Agent CLI

Cost-effective AI agent with FREE MCP tools.
Model: claude-3-haiku | Temp: 0.5 | Max Tokens: 250
"""

import uuid
from src.agent import MultiSkillsAgent


def print_banner(skills: list):
    skills_text = " | ".join(skills) if skills else "No skills"
    print(f"""
    ╔════════════════════════════════════════════════════════════════════════════════╗
    ║                           MULTI-SKILLS AGENT v3.1                              ║
    ║            💰 Cost-Effective: claude-3-haiku + FREE MCP Tools                  ║
    ╠════════════════════════════════════════════════════════════════════════════════╣
    ║  Skills: {skills_text:<70}║
    ╠════════════════════════════════════════════════════════════════════════════════╣
    ║  MCP Tools (All FREE):                                                         ║
    ║    🌤️ Weather    📈 Stocks    📰 News    🗄️ Database                             ║
    ╠════════════════════════════════════════════════════════════════════════════════╣
    ║  Commands: skills | examples | clear | quit                                    ║
    ╚════════════════════════════════════════════════════════════════════════════════╝
    """)


def print_skills(skills: list):
    print("\n📚 Skills:", ", ".join(skills))
    print("\n🔧 MCP Tools (All FREE):")
    print("   🌤️ Weather: get_current_weather, get_weather_forecast, get_air_quality")
    print("   📈 Stocks:  get_stock_quote, get_stock_history, get_company_info")
    print("   📰 News:    get_top_headlines, search_news, get_news_sources")
    print("   🗄️ Database: get_all_employees, get_employee_by_id, search_employees, get_department_stats\n")


def print_examples():
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                      EXAMPLE INTERACTIONS                          ║
    ╠═══════════════════════════════════════════════════════════════════╣

    🌤️ WEATHER (Open-Meteo - Free)
    ─────────────────────────────────────────────────────────────────────
       • "What's the weather in Tokyo?"
       • "5-day forecast for London"
       • "Air quality in Beijing"

    📈 STOCKS (Yahoo Finance - Free)
    ─────────────────────────────────────────────────────────────────────
       • "Price of AAPL"
       • "Tell me about MSFT stock"
       • "NVDA performance this year"
       
       Tickers: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META

    📰 NEWS (Google News RSS - Free)
    ─────────────────────────────────────────────────────────────────────
       • "Top tech news"
       • "News about Tesla"
       • "What's happening in India?"

    🗄️ DATABASE (In-Memory SQLite - Free)
    ─────────────────────────────────────────────────────────────────────
       • "Show all employees"
       • "Who is employee #5?"
       • "Find engineers"
       • "Search employees in San Francisco"
       • "Department salary statistics"

    ╚═══════════════════════════════════════════════════════════════════╝
    """)


def main():
    try:
        agent = MultiSkillsAgent()
        skills = agent.get_available_skills()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Set ANTHROPIC_API_KEY in .env file")
        return

    print_banner(skills)
    thread_id = str(uuid.uuid4())
    print(f"    Session: {thread_id[:8]}...\n")

    while True:
        try:
            user_input = input("You >> ").strip()
            if not user_input:
                continue
            
            cmd = user_input.lower()
            if cmd in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break
            if cmd == "clear":
                agent.reset_conversation(thread_id)
                thread_id = str(uuid.uuid4())
                print(f"🔄 New session: {thread_id[:8]}...\n")
                continue
            if cmd == "examples":
                print_examples()
                continue
            if cmd == "skills":
                print_skills(skills)
                continue
            
            print("🤔 ", end="", flush=True)
            response = agent.process_request(user_input, thread_id=thread_id)
            print(f"\r🤖 {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

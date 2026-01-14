# Telecom Skills Agent

A CLI-based AI agent demonstrating the "Build Skills, Not Agents" architecture using LangChain, LangGraph, and OpenAI.

This agent handles three distinct domain skills using a single ReAct loop:

1. **Roaming Activation**: International travel plans and rates.
2. **Broadband Installation**: Availability checks and scheduling.
3. **Fee Waivers**: Policy-based decision making for late fees.

## Architecture

- **One Generalist Agent**: A single `TelecomSkillsAgent` class.
- **Dynamic Tools**: Each domain exposes specific tools (e.g., `check_service_availability`, `activate_roaming`).
- **Knowledge Injection**: Domain constraints and processes are defined in `SKILL.md` files and injected into the System Prompt.
- **LangGraph**: Manages the agent state and tool execution loop.
- **Memory**: Maintains conversation context via `MemorySaver`.

## Prerequisites

- Python 3.11+
- An OpenAI API Key (`gpt-4o-mini` access recommmended)

## Setup

1. **Clone/Navigate to the project**:

    ```bash
    cd telecom-skills-agent
    ```

2. **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Mac/Linux
    # or .\venv\Scripts\activate on Windows
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configuration**:
    Copy the example env file and add your API key:

    ```bash
    cp .env.example .env
    # Edit .env and paste your OPENAI_API_KEY
    ```

## Usage

Run the main entry point:

```bash
python3 main.py
```

### Commands

- `examples`: Show sample queries.
- `clear`: Reset the conversation context.
- `quit` / `exit`: Stop the program.

## Mock Data

The system uses in-memory mock databases located in `src/database/mock_db.py` and various JSON files in `src/skills/`.

**Sample Customer IDs:**

- `CUST001` (Active, clean history)
- `CUST002` (Active, owing money)
- `CUST003` (Suspended, bad history)

## Example Scenarios to Try

**1. Roaming**
> "Hi, I am CUST001. I am going to Japan for 2 weeks."
(Agent should suggest a Monthly plan or 2 Weekly passes, check rates, and ask to confirm.)

**2. Broadband**
> "Is internet available at 123 Main St, zip 10001?"
(Agent should find Fiber availability.)
> "Book an appointment for CUST002 next Tuesday morning."

**3. Fee Waiver**
> "I missed my payment because the bank app was down. Customer CUST001."
(Agent should check history, see high score, and approve waiver.)

## Project Structure

```
telecom-skills-agent/
├── main.py            # CLI Entrypoint
├── src/
│   ├── agent.py       # Main LangGraph Agent
│   ├── skills/        # Domain knowledge (Markdown + JSON)
│   ├── tools/         # Python functions (@tool)
│   └── database/      # Mock in-memory DB
└── logs/
```

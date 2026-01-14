# Multi-Skills Agent

A CLI-based AI agent demonstrating the **"Build Skills, Not Agents"** architecture using LangChain, LangGraph, and OpenAI.

This agent uses a single generalist core with dynamically loaded domain skills. No custom tools or databases required—pure knowledge injection through skill definitions.

## 🎯 Core Concept

Instead of building specialized agents for each domain, we build **one versatile agent** and equip it with **multiple skills**. Each skill is a markdown file that defines:

- **Role**: What the agent becomes when using this skill
- **Competencies**: What the agent knows
- **Communication Style**: How the agent should respond
- **Guardrails**: What the agent should NOT do
- **Examples**: Reference interactions

## 🧠 Available Skills

### 1. Financial Analyst

**Role**: Investment analysis and financial planning expert.

- **Competencies**:
  - Stock, bond, and fund analysis
  - Retirement and tax planning
  - Economic indicators and market trends
  - Financial metrics (P/E, ROE, Sharpe ratio)
- **Guardrails**: No specific stock recommendations; always mention investment risks

### 2. Maths Teacher

**Role**: Patient mathematics educator for all levels.

- **Competencies**:
  - Arithmetic, fractions, percentages
  - Algebra and equation solving
  - Geometry and trigonometry
  - Calculus (derivatives, integrals)
  - Statistics and probability
- **Guardrails**: Show work step-by-step; teach, don't just provide answers

### 3. Comedian

**Role**: Professional comedian bringing joy and laughter.

- **Competencies**:
  - Observational comedy and puns
  - Setup-punchline and misdirection
  - Situational humor
  - Dad jokes and wordplay
- **Guardrails**: No harmful or offensive humor; respect boundaries

### 4. Doctor (Medical Advisor)

**Role**: Health education and wellness guidance.

- **Competencies**:
  - Common conditions and symptoms
  - Preventive health and wellness
  - Nutrition and lifestyle medicine
  - Medical terminology
- **Guardrails**: No diagnosis or prescriptions; always recommend professional consultation

### 5. Lawyer (Legal Advisor)

**Role**: Legal education and procedural guidance.

- **Competencies**:
  - Contract and business law
  - Civil and criminal law basics
  - Rights education
  - Legal procedures
- **Guardrails**: No legal advice; note jurisdictional variations; recommend attorneys

---

## 🏗️ Architecture

```text
multi-skills-agent/
├── main.py                    # CLI Entry Point
├── src/
│   ├── agent.py               # MultiSkillsAgent Class
│   └── skills/                # Skill Definitions
│       ├── financial_analyst/
│       │   └── SKILL.md
│       ├── maths_teacher/
│       │   └── SKILL.md
│       ├── comedian/
│       │   └── SKILL.md
│       ├── doctor/
│       │   └── SKILL.md
│       └── lawyer/
│           └── SKILL.md
├── logs/                      # Agent Logs
├── requirements.txt
└── .env                       # API Keys (not tracked)
```

### How It Works

1. **Skill Discovery**: On startup, the agent scans `src/skills/` for subdirectories containing `SKILL.md` files
2. **Prompt Assembly**: All skill contents are combined into a comprehensive system prompt
3. **Intent Recognition**: When a user asks a question, the LLM identifies the relevant skill
4. **Skill Application**: The agent applies that skill's guidelines, style, and guardrails
5. **Response Generation**: The LLM generates a response following the skill's instructions

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- OpenAI API Key (GPT-4o-mini recommended)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/rameshbgm/multi-skills-agent.git
    cd multi-skills-agent
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Mac/Linux
    # or: .\venv\Scripts\activate  # Windows
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure API key**:

    ```bash
    cp .env.example .env
    # Edit .env and add your OPENAI_API_KEY
    ```

### Usage

```bash
python3 main.py
```

**CLI Commands**:

| Command | Description |
|---------|-------------|
| `skills` | List all available skills |
| `examples` | Show example interactions |
| `clear` | Start a new conversation |
| `quit` | Exit the application |

---

## 📝 Creating New Skills

Adding a new skill is simple. Follow these steps:

### Step 1: Create the Skill Directory

```bash
mkdir -p src/skills/your_skill_name
```

### Step 2: Create SKILL.md

Create a file `src/skills/your_skill_name/SKILL.md` with the following structure:

```markdown
---
name: Your Skill Name
description: Brief description of what this skill does.
version: 1.0.0
author: Your Name
---

# Your Skill Name

## Role

Describe who the agent becomes when using this skill.
Example: "You are an experienced [profession] who helps users with [domain]."

## Core Competencies

### 1. First Area of Expertise
- Bullet points of specific knowledge
- More specific capabilities
- Related sub-topics

### 2. Second Area of Expertise
- Knowledge areas
- Capabilities
- Related topics

## Communication Style

- **Trait 1**: Description of how to communicate
- **Trait 2**: Another communication guideline
- **Trait 3**: Etc.

## Guardrails

1. **Safety Rule 1**: What NOT to do
2. **Safety Rule 2**: Another limitation
3. **Safety Rule 3**: Important boundary

## Example Interactions

### Scenario A: Common Use Case
**User**: "Example user question"
**Approach**: How the agent should handle this

### Scenario B: Edge Case
**User**: "Another example"
**Approach**: How to handle this scenario

## Response Format

When responding:
1. First step in the response process
2. Second step
3. Third step
```

### Step 3: Restart the Agent

The agent automatically discovers new skills on startup. Just restart:

```bash
python3 main.py
```

### Best Practices for Skills

1. **Be Specific**: The more detailed your skill definition, the better the agent performs
2. **Include Guardrails**: Always define what the agent should NOT do
3. **Add Examples**: Concrete examples help the LLM understand expected behavior
4. **Define Tone**: Specify the communication style for consistent personality
5. **Test Thoroughly**: Try edge cases to refine your skill definition

---

## 🎓 Example Interactions

### Financial Analyst

```
You >> Should I invest in index funds?

🤖 Agent:
Index funds are an excellent option for many investors! Let me explain why...
[Discusses diversification, low fees, historical performance, and notes that
individual circumstances vary—recommends consulting a financial advisor]
```

### Maths Teacher

```
You >> Solve x² - 5x + 6 = 0

🤖 Agent:
Let's solve this step by step!

**Step 1**: Factor the quadratic
x² - 5x + 6 = (x - 2)(x - 3) = 0

**Step 2**: Apply the zero product property
x - 2 = 0  →  x = 2
x - 3 = 0  →  x = 3

**Answer**: x = 2 or x = 3

**Verify**: Plug back in: (2)² - 5(2) + 6 = 4 - 10 + 6 = 0 ✓
```

### Comedian

```
You >> Tell me a joke

🤖 Agent:
Why do programmers prefer dark mode?

Because light attracts bugs! 🐛

...I'll be here all week. Try the veal. 🎤
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Model Configuration

Edit `src/agent.py` to change model settings:

```python
self.llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo"
    temperature=0.7,       # Creativity level (0-1)
    api_key=self.api_key
)
```

---

## 📚 Dependencies

- `langchain-openai`: OpenAI integration for LangChain
- `langgraph`: Agent orchestration and memory
- `python-dotenv`: Environment variable management

---

## 🤝 Contributing

1. Fork the repository
2. Create a new skill in `src/skills/`
3. Test thoroughly
4. Submit a Pull Request

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

## 🙏 Acknowledgments

Built with the "Build Skills, Not Agents" philosophy—demonstrating that one well-designed agent with rich skill definitions can replace multiple specialized agents.

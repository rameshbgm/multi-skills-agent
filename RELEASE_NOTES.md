# Release Notes

## Version 3.1.0 - January 18, 2026

### 🎉 New Features

#### Database Admin Skill & MCP

- Added new **Database Admin** skill for employee data queries
- Created **database_mcp.py** with in-memory SQLite database
- Pre-populated with 15 employee records
- 4 MCP tools: `get_all_employees`, `get_employee_by_id`, `search_employees`, `get_department_stats`
- No external database or API key required

### 💰 Cost Optimization

- Switched to **claude-3-haiku-20240307** (cheapest Claude model)
  - Input: $0.25 per 1M tokens
  - Output: $1.25 per 1M tokens
- Reduced temperature to **0.5** for focused responses
- Limited max_tokens to **250** for concise output

### 🔧 MCP Updates

- All MCPs now use **FREE public APIs** - no API keys required for data!
- Weather: Switched from OpenWeatherMap to **Open-Meteo** (free, no key)
- News: Fixed Google News RSS topic codes for proper category filtering
- Database: New in-memory SQLite (local, free)

---

## Version 3.0.0 - January 18, 2026

### 🔄 Major Changes

#### SDK Migration

- Replaced **OpenAI SDK** with **Anthropic Claude SDK**
- Updated from `langchain-openai` to `langchain-anthropic`
- Environment variable changed from `OPENAI_API_KEY` to `ANTHROPIC_API_KEY`

#### MCP Architecture

- Created dedicated `src/mcp/` folder for all MCP tools
- Each MCP in separate file:
  - `weather_mcp.py` - Open-Meteo API
  - `stock_mcp.py` - Yahoo Finance
  - `news_mcp.py` - Google News RSS
  - `database_mcp.py` - In-memory SQLite

#### Skill Cleanup

- **Removed**: comedian, doctor, financial_analyst, lawyer, maths_teacher
- **Added**: weather_forecaster, stock_analyst, news_reporter, database_admin
- All skills now have MCP integrations

### 📁 Project Structure

```
multi-skills-agent/
├── main.py
├── src/
│   ├── agent.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── weather_mcp.py    # Open-Meteo (free)
│   │   ├── stock_mcp.py      # Yahoo Finance (free)
│   │   ├── news_mcp.py       # Google News RSS (free)
│   │   └── database_mcp.py   # SQLite (local)
│   └── skills/
│       ├── weather_forecaster/
│       ├── stock_analyst/
│       ├── news_reporter/
│       └── database_admin/
├── .env
├── .env.example
├── requirements.txt
├── README.md
└── RELEASE_NOTES.md
```

---

## API Summary

### Required API Key

| Service | Variable | Cost |
| ------- | -------- | ---- |
| Anthropic (Claude) | `ANTHROPIC_API_KEY` | ~$0.25-1.25/1M tokens |

### Free Data APIs (No Keys Required)

| API | MCP | Description |
| --- | --- | ----------- |
| Open-Meteo | weather_mcp | Weather data |
| Yahoo Finance | stock_mcp | Stock market data |
| Google News RSS | news_mcp | News headlines |
| SQLite | database_mcp | Employee database |

---

## MCP Tools (13 Total)

### Weather (3 tools)

- `get_current_weather(location)`
- `get_weather_forecast(location, days)`
- `get_air_quality(location)`

### Stocks (3 tools)

- `get_stock_quote(ticker)`
- `get_stock_history(ticker, period)`
- `get_company_info(ticker)`

### News (3 tools)

- `get_top_headlines(category, country)`
- `search_news(query)`
- `get_news_sources(category)`

### Database (4 tools)

- `get_all_employees(limit)`
- `get_employee_by_id(id)`
- `search_employees(query, search_by)`
- `get_department_stats()`

---

## Employee Database Schema

| Column | Type | Description |
| ------ | ---- | ----------- |
| id | INTEGER | 1-15 |
| first_name | TEXT | First name |
| last_name | TEXT | Last name |
| email | TEXT | Email |
| department | TEXT | Engineering, Sales, Marketing, Finance, HR |
| job_title | TEXT | Job title |
| salary | REAL | USD |
| hire_date | TEXT | YYYY-MM-DD |
| phone | TEXT | Phone |
| city | TEXT | Office city |

---

## Configuration

### LLM Settings

```python
model = "claude-3-haiku-20240307"
temperature = 0.5
max_tokens = 250
```

### .env File

```env
ANTHROPIC_API_KEY=your-key-here
```

---

## Dependencies

```
langchain>=0.1.0
langchain-anthropic>=0.1.0
langgraph>=0.0.10
python-dotenv>=1.0.0
httpx>=0.25.0
```

---

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
echo "ANTHROPIC_API_KEY=your-key" > .env

# Run
python main.py
```

---

## Example Queries

```
Weather:  "What's the weather in Tokyo?"
Stocks:   "Price of AAPL"
News:     "Top tech news"
Database: "Show all employees"
```

# Multi-Skills Agent

Cost-effective AI agent using **Claude 3 Haiku** with **FREE MCP tools**.

## Features

- 💰 **Cheapest Model**: claude-3-haiku ($0.25/1M input, $1.25/1M output)
- ✅ **Free Data APIs**: All MCP tools use free public APIs
- 🔧 **13 MCP Tools**: Weather, Stocks, News, Database
- 📦 **4 Skills**: Weather, Stock, News, Database Admin

## Quick Start

```bash
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your-key" > .env
python main.py
```

## MCP Tools (All FREE)

| MCP | API | Tools |
| --- | --- | ----- |
| Weather | Open-Meteo | get_current_weather, get_weather_forecast, get_air_quality |
| Stocks | Yahoo Finance | get_stock_quote, get_stock_history, get_company_info |
| News | Google News RSS | get_top_headlines, search_news, get_news_sources |
| Database | SQLite (local) | get_all_employees, get_employee_by_id, search_employees, get_department_stats |

## Skills

| Skill | Description |
| ----- | ----------- |
| Weather Forecaster | Current conditions, forecasts, air quality |
| Stock Analyst | Quotes, history, company info by ticker |
| News Reporter | Headlines, search, sources |
| Database Admin | Employee queries (15 records) |

## Project Structure

```
multi-skills-agent/
├── main.py                  # CLI
├── src/
│   ├── agent.py             # Agent (claude-3-haiku)
│   ├── mcp/                 # MCP tools
│   │   ├── weather_mcp.py   # Open-Meteo
│   │   ├── stock_mcp.py     # Yahoo Finance
│   │   ├── news_mcp.py      # Google News
│   │   └── database_mcp.py  # SQLite
│   └── skills/              # Skill definitions
│       ├── weather_forecaster/
│       ├── stock_analyst/
│       ├── news_reporter/
│       └── database_admin/
├── .env                     # ANTHROPIC_API_KEY
├── requirements.txt
├── README.md
└── RELEASE_NOTES.md
```

## Configuration

| Setting | Value |
| ------- | ----- |
| Model | claude-3-haiku-20240307 |
| Temperature | 0.5 |
| Max Tokens | 250 |

## Examples

```
# Weather
"What's the weather in Tokyo?"
"5-day forecast for London"

# Stocks
"Price of AAPL"
"Tell me about MSFT"

# News
"Top tech news"
"News about Tesla"

# Database
"Show all employees"
"Find engineers"
"Department statistics"
```

## CLI Commands

| Command | Action |
| ------- | ------ |
| skills | List skills |
| examples | Show examples |
| clear | Reset conversation |
| quit | Exit |

## API Keys

| Service | Required | Cost |
| ------- | -------- | ---- |
| Anthropic | Yes | $0.25-1.25/1M |
| Open-Meteo | No | Free |
| Yahoo Finance | No | Free |
| Google News | No | Free |
| SQLite | No | Local |

## Dependencies

```
langchain>=0.1.0
langchain-anthropic>=0.1.0
langgraph>=0.0.10
python-dotenv>=1.0.0
httpx>=0.25.0
```

## License

MIT License

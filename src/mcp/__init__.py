"""
MCP (Model Context Protocol) Tools Package

All MCP tools use FREE APIs or local resources - NO API keys required for data!

Available MCPs:
- weather_mcp: Open-Meteo API (free)
- stock_mcp: Yahoo Finance (free)
- news_mcp: Google News RSS (free)
- database_mcp: In-memory SQLite employee database (local)
"""

from .weather_mcp import (
    get_current_weather,
    get_weather_forecast,
    get_air_quality,
    WEATHER_TOOLS
)

from .stock_mcp import (
    get_stock_quote,
    get_stock_history,
    get_company_info,
    STOCK_TOOLS
)

from .news_mcp import (
    get_top_headlines,
    search_news,
    get_news_sources,
    NEWS_TOOLS
)

from .database_mcp import (
    get_all_employees,
    get_employee_by_id,
    search_employees,
    get_department_stats,
    DATABASE_TOOLS
)

ALL_MCP_TOOLS = WEATHER_TOOLS + STOCK_TOOLS + NEWS_TOOLS + DATABASE_TOOLS

__all__ = [
    'get_current_weather',
    'get_weather_forecast',
    'get_air_quality',
    'WEATHER_TOOLS',
    'get_stock_quote',
    'get_stock_history',
    'get_company_info',
    'STOCK_TOOLS',
    'get_top_headlines',
    'search_news',
    'get_news_sources',
    'NEWS_TOOLS',
    'get_all_employees',
    'get_employee_by_id',
    'search_employees',
    'get_department_stats',
    'DATABASE_TOOLS',
    'ALL_MCP_TOOLS'
]

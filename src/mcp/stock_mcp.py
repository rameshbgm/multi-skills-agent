"""
Stock MCP - Yahoo Finance Public API Integration (No API Key Required)

This module provides MCP tools for fetching stock market data from Yahoo Finance.
Uses public Yahoo Finance endpoints that require NO API key.

Tools:
- get_stock_quote: Get real-time stock price by ticker symbol
- get_stock_history: Get historical price data by ticker symbol
- get_company_info: Get company profile and financials by ticker symbol

Note: Uses unofficial public endpoints. No API key needed.
"""

import json
import logging
import httpx
from datetime import datetime
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# User-Agent header to avoid blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


@tool
def get_stock_quote(ticker: str) -> str:
    """
    Get real-time stock quote for a given ticker symbol (FREE, no API key).
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL", "MSFT", "TSLA")
    
    Returns:
        Current stock price and basic market data
    """
    try:
        # Normalize ticker to uppercase
        ticker = ticker.upper().strip()
        
        # Using Yahoo Finance public API
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        response = httpx.get(url, headers=HEADERS, timeout=10.0)
        data = response.json()
        
        if response.status_code == 200 and data.get('chart', {}).get('result'):
            result = data['chart']['result'][0]
            meta = result['meta']
            
            current_price = meta.get('regularMarketPrice', 0)
            previous_close = meta.get('previousClose', 0)
            change = current_price - previous_close if previous_close else 0
            change_percent = (change / previous_close * 100) if previous_close else 0
            
            quote = {
                "ticker": meta['symbol'],
                "name": meta.get('longName', meta['symbol']),
                "current_price": f"${current_price:.2f}",
                "previous_close": f"${previous_close:.2f}",
                "change": f"${change:+.2f}",
                "change_percent": f"{change_percent:+.2f}%",
                "currency": meta.get('currency', 'USD'),
                "exchange": meta.get('exchangeName', 'Unknown'),
                "market_state": meta.get('marketState', 'Unknown')
            }
            return json.dumps(quote, indent=2)
        else:
            error_msg = data.get('chart', {}).get('error', {}).get('description', f'Unable to fetch data for ticker: {ticker}')
            return f"Error: {error_msg}"
    except Exception as e:
        logger.error(f"Stock quote error for {ticker}: {e}")
        return f"Error fetching stock quote for {ticker}: {str(e)}"


@tool
def get_stock_history(ticker: str, period: str = "1mo") -> str:
    """
    Get historical stock prices for a given ticker symbol (FREE, no API key).
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL", "MSFT", "TSLA")
        period: Time period - "1d", "5d", "1mo", "3mo", "6mo", "1y", "5y" (default: "1mo")
    
    Returns:
        Historical price data with open, high, low, close, volume
    """
    try:
        # Normalize ticker to uppercase
        ticker = ticker.upper().strip()
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {"range": period, "interval": "1d"}
        response = httpx.get(url, params=params, headers=HEADERS, timeout=10.0)
        data = response.json()
        
        if response.status_code == 200 and data.get('chart', {}).get('result'):
            result = data['chart']['result'][0]
            timestamps = result.get('timestamp', [])
            quotes = result['indicators']['quote'][0]
            
            # Get last 10 data points
            history = []
            start_idx = max(0, len(timestamps) - 10)
            
            for i in range(start_idx, len(timestamps)):
                ts = timestamps[i]
                close_val = quotes['close'][i] if quotes['close'][i] else None
                if close_val is not None:
                    history.append({
                        "date": datetime.fromtimestamp(ts).strftime('%Y-%m-%d'),
                        "open": f"${quotes['open'][i]:.2f}" if quotes['open'][i] else "N/A",
                        "high": f"${quotes['high'][i]:.2f}" if quotes['high'][i] else "N/A",
                        "low": f"${quotes['low'][i]:.2f}" if quotes['low'][i] else "N/A",
                        "close": f"${close_val:.2f}",
                        "volume": f"{quotes['volume'][i]:,}" if quotes['volume'][i] else "N/A"
                    })
            
            # Calculate performance
            if len(history) >= 2:
                first_close = float(history[0]['close'].replace('$', ''))
                last_close = float(history[-1]['close'].replace('$', ''))
                period_change = ((last_close - first_close) / first_close) * 100
            else:
                period_change = 0
            
            return json.dumps({
                "ticker": ticker,
                "period": period,
                "period_performance": f"{period_change:+.2f}%",
                "data_points": len(history),
                "history": history
            }, indent=2)
        else:
            error_msg = data.get('chart', {}).get('error', {}).get('description', f'Unable to fetch history for ticker: {ticker}')
            return f"Error: {error_msg}"
    except Exception as e:
        logger.error(f"Stock history error for {ticker}: {e}")
        return f"Error fetching stock history for {ticker}: {str(e)}"


@tool
def get_company_info(ticker: str) -> str:
    """
    Get company information and key statistics for a given ticker symbol (FREE, no API key).
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL", "MSFT", "TSLA")
    
    Returns:
        Company profile, sector, industry, and key financial metrics
    """
    try:
        # Normalize ticker to uppercase
        ticker = ticker.upper().strip()
        
        url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
        params = {"modules": "summaryProfile,financialData,defaultKeyStatistics,price"}
        response = httpx.get(url, params=params, headers=HEADERS, timeout=10.0)
        data = response.json()
        
        if response.status_code == 200 and data.get('quoteSummary', {}).get('result'):
            result = data['quoteSummary']['result'][0]
            profile = result.get('summaryProfile', {})
            financials = result.get('financialData', {})
            stats = result.get('defaultKeyStatistics', {})
            price = result.get('price', {})
            
            def get_value(d, key):
                val = d.get(key, {})
                if isinstance(val, dict):
                    return val.get('fmt', val.get('raw', 'N/A'))
                return val if val else 'N/A'
            
            info = {
                "ticker": ticker,
                "name": get_value(price, 'longName'),
                "sector": profile.get('sector', 'N/A'),
                "industry": profile.get('industry', 'N/A'),
                "country": profile.get('country', 'N/A'),
                "employees": profile.get('fullTimeEmployees', 'N/A'),
                "website": profile.get('website', 'N/A'),
                "summary": (profile.get('longBusinessSummary', 'N/A')[:500] + "...") if profile.get('longBusinessSummary') else 'N/A',
                "financials": {
                    "market_cap": get_value(price, 'marketCap'),
                    "revenue": get_value(financials, 'totalRevenue'),
                    "profit_margin": get_value(financials, 'profitMargins'),
                    "operating_margin": get_value(financials, 'operatingMargins'),
                    "current_price": get_value(financials, 'currentPrice'),
                    "target_price": get_value(financials, 'targetMeanPrice'),
                    "recommendation": get_value(financials, 'recommendationKey')
                },
                "key_stats": {
                    "pe_ratio": get_value(stats, 'trailingPE'),
                    "forward_pe": get_value(stats, 'forwardPE'),
                    "peg_ratio": get_value(stats, 'pegRatio'),
                    "price_to_book": get_value(stats, 'priceToBook'),
                    "beta": get_value(stats, 'beta'),
                    "52_week_high": get_value(stats, 'fiftyTwoWeekHigh'),
                    "52_week_low": get_value(stats, 'fiftyTwoWeekLow')
                }
            }
            return json.dumps(info, indent=2)
        else:
            error_msg = data.get('quoteSummary', {}).get('error', {}).get('description', f'Unable to fetch company info for ticker: {ticker}')
            return f"Error: {error_msg}"
    except Exception as e:
        logger.error(f"Company info error for {ticker}: {e}")
        return f"Error fetching company info for {ticker}: {str(e)}"


# Export all stock tools
STOCK_TOOLS = [
    get_stock_quote,
    get_stock_history,
    get_company_info
]

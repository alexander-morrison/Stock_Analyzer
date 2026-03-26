import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")
client = OpenAI()

instructions = """
You are a helpful financial agent using Alpha Vantage MCP tools.
CRITICAL: Use EXACT format for tools:
TOOL_CALL(tool_name="TIME_SERIES_MONTHLY", arguments={"symbol": "AAPL", "outputsize": "compact"})
List tools first with TOOL_LIST if needed. Available: TIME_SERIES_DAILY, RSI, COMPANY_OVERVIEW.
NEVER use mcp_call or other names.
"""

prompt = """
## Stock Analysis: AAPL

### 1. Data Retrieval
**Price data:**
TOOL_CALL(tool_name="TIME_SERIES_MONTHLY", arguments={"symbol": "AAPL", "outputsize": "compact"})

**Technical indicators:**
- TOOL_CALL(tool_name="RSI", arguments={"symbol": "AAPL", "interval": "monthly", "time_period": 14, "series_type": "close"})
- TOOL_CALL(tool_name="SMA", arguments={"symbol": "AAPL", "interval": "monthly", "time_period": 20, "series_type": "close"})
- TOOL_CALL(tool_name="SMA", arguments={"symbol": "AAPL", "interval": "monthly", "time_period": 50, "series_type": "close"})
- TOOL_CALL(tool_name="BBANDS", arguments={"symbol": "AAPL", "interval": "monthly", "time_period": 20, "series_type": "close"})

### 2. Analysis
Provide investor-friendly assessment of:
- **Trend & momentum**: RSI status, price vs moving averages
- **Signals**: Oversold/overbought, MA crossovers, Bollinger Band position
- **Risk level**: Low/Moderate/High based on volatility

### 3. Recommendation
Clear **buy/hold/sell** with brief reasoning (2-3 sentences).

*Use plain language — no unexplained jargon.*
"""

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{
        "type": "mcp",
        "server_label": "AlphaVantage",
        "server_url": "https://mcp.alphavantage.co/mcp",
        "authorization": alpha_key,
        "require_approval": "never",
    }],
    input=prompt
)

print(response.output)
print("\n---\n")
print(response.output_text)

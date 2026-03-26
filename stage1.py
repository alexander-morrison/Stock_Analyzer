import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")

client = OpenAI()


instructions = """
You are a helpful financial agent with access to market data through Alpha Vantage MCP Server.
IMPORTANT: Alpha Vantage functions are accessed via wrapper tools:
  - Use TOOL_LIST to see available functions (TIME_SERIES_DAILY, RSI, COMPANY_OVERVIEW, etc.)
  - Use TOOL_CALL with the format: TOOL_CALL(tool_name="FUNCTION_NAME", arguments={...})
  - Example: TOOL_CALL(tool_name="TIME_SERIES_DAILY", arguments={"symbol": "AAPL", "outputsize": "compact"})
"""

prompt = """
## Stock Summary: AAPL

### 1. Data Retrieval
Retrieve daily data for 'AAPL' (last 3 days):
TOOL_CALL(tool_name="TIME_SERIES_DAILY", arguments={"symbol": "AAPL", "outputsize": "compact"})

### 2. Summary
Provide a brief overview:
- Price movement (up/down/flat)
- Day-over-day % change
- Notable volume changes
"""

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[
        {
            "type": "mcp",
            "server_label": "AlphaVantage",
            "server_url": "https://mcp.alphavantage.co/mcp",
            "authorization": alpha_key,
            "require_approval": "never",
        },
    ],
    input=prompt
)

print(response.output)
print("\n---\n")
print(response.output_text)

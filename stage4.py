import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")
client = OpenAI()

instructions = """
Expert financial analyst. Follow prompt exactly.

After TIME_SERIES_MONTHLY data retrieval:
1. Use code_interpreter to parse JSON → pandas DataFrame (latest 3 months)
2. Calculate MoM % changes, volatility, volume trends
3. CRITICAL: Generate matplotlib charts:
   - Price chart: Close prices line plot
   - Volume chart: bars
   - plt.figure(figsize=(12,8)); plt.subplot(2,1,1/2); labels/titles/legends
   - plt.savefig('aapl_analysis.png', dpi=150, bbox_inches='tight')
4. Confirm 'Charts saved as aapl_analysis.png'
Investor summary in plain language.
"""

prompt = """
## Stock Analysis Task

### 1. Data Retrieval
Retrieve monthly time series data for **'AAPL'** (latest 3 months) using:
TOOL_CALL(tool_name="TIME_SERIES_MONTHLY", arguments={"symbol": "AAPL", "outputsize": "compact"})

### 2. Analysis (using code_interpreter) (REQUIRED)
- Calculate month-over-month price changes (%)
- Identify trend direction (up/down/sideways)
- Compute key metrics: avg closing price, volatility, volume trends

### 3. Visualization (REQUIRED)
Generate using `code_interpreter`:
- **Price chart**: Monthly OHLC data
- **Volume chart**: Trading volume per month

Ensure charts have clear titles, labels, and legends.

### 4. Summary
Provide a brief trend assessment with key insights.
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
        {
            "type": "code_interpreter",
            "container": {
                "type": "auto",
                "memory_limit": "4g"
            }
        }
    ],
    input=prompt
)

print(response.output)
print("\n---\n")
print(response.output_text)

# --- Find chart file in annotations and save as stock_image.png ---

container_id = None
file_id = None

for item in response.output:
    if item.type == "message":
        for content in item.content:
            if content.type == "output_text":
                for ann in getattr(content, "annotations", []) or []:
                    if getattr(ann, "type", None) == "container_file_citation":
                        container_id = ann.container_id
                        file_id = ann.file_id
                        break
        if container_id and file_id:
            break

if container_id and file_id:
    file_content = client.containers.files.content.retrieve(
        container_id=container_id,
        file_id=file_id,
    )
    data = file_content.read()
    with open("stock_image.png", "wb") as f:
        f.write(data)
else:
    print("No container_file_citation found in response.")

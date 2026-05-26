#!/usr/bin/env python3
import anthropic
from datetime import datetime
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(response):
    """Concatenate the text blocks from a Claude response."""
    return "".join(block.text for block in response.content if block.type == "text")


# Get profitable markets with detailed betting strategy
result = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": """Visit Polymarket.com right now and research the CURRENT real markets. Create a detailed, actionable betting strategy:

1. Find 5 SPECIFIC markets currently trading on Polymarket that have high potential ROI
2. For each market:
   - List the EXACT market name
   - Provide the CURRENT odds in percentages (YES/NO prices)
   - Recommend which position to take (YES/NO) based on your research
   - Suggest a specific amount to bet from a $1000 total budget
   - Calculate potential profit in dollars
   - Estimate your confidence level and expected value

3. Create a simple, compact summary table with:
   [Market Name | Position | Bet Amount | Expected Profit]

4. Calculate total expected profit across all bets and ROI percentage

Focus on REAL markets currently available on Polymarket.com with exact numbers and calculations.
Use a maximum of 250 words for your response to ensure all information fits in the output.
"""}],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
)

# Print results
print(f"POLYMARKET BETTING STRATEGY ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 80)
print(extract_text(result))

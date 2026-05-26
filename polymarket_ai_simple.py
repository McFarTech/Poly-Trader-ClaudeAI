#!/usr/bin/env python3
import anthropic
from datetime import datetime
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Create a prompt asking about current Polymarket markets
prompt = """Based on your most recent knowledge, list the current popular markets on Polymarket.com.
Include political markets like presidential elections and sports betting markets.
For each market, include:
1. The market question
2. The current odds or probability
3. The expected resolution date

Format as a numbered list of at least 10 markets. If you don't have current information,
provide the most recent markets you're aware of and clearly note that the information might
be outdated."""

# Get response from the Claude API
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": prompt}]
)

# Print results
print(f"POLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 70)
print(response.content[0].text)

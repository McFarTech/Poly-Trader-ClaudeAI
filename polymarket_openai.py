#!/usr/bin/env python3
# NOTE: This script now uses the Anthropic Claude API despite its filename.
import anthropic
from datetime import datetime
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Create a prompt asking about current Polymarket markets
prompt = """List the current active markets on Polymarket.com for today 
(including their odds if available). Focus on trending political and sports 
markets. Format as a numbered list."""

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

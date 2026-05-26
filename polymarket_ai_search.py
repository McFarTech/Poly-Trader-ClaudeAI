#!/usr/bin/env python3
import anthropic
from datetime import datetime
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(response):
    """Concatenate the text blocks from a Claude response."""
    return "".join(block.text for block in response.content if block.type == "text")


# Anthropic has no Assistants/threads API: a single Messages call with the
# web_search tool replaces the create-assistant / create-thread / poll-run flow.
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    system="Search for the current active markets on Polymarket.com. Focus on trending political and sports markets. Format as a numbered list with odds for each market.",
    messages=[
        {
            "role": "user",
            "content": "List the current trending markets on Polymarket.com including odds. Focus on political and sports markets."
        }
    ],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
)

# Print the assistant response
print(f"\nPOLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 70)
print(extract_text(response))

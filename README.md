# PolyTrader: AI-Powered Automated Trading System for Polymarket

An autonomous AI trading agent for Polymarket that identifies market inefficiencies, calculates optimal bet sizes, and executes trades automatically. This system leverages Claude's predictive capabilities against existing market odds to find profitable edges.

## 🚀 Getting Started

### Prerequisites

- Python 3.11+ recommended (3.9 is the minimum required by the Anthropic SDK and py-clob-client; 3.8 is end-of-life)
- A Polygon network wallet with MATIC (for gas) and USDC (for trading)
- API keys for Anthropic and SerpAPI
- Basic understanding of prediction markets and crypto wallets

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/PolyTrader.git
cd PolyTrader
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Run the application
```bash
python app.py
```

6. Visit http://127.0.0.1:5000 in your browser

## 📋 Features

* **Market Analysis:** Continuously scans Polymarket for opportunities
* **AI-Powered Predictions:** Uses Claude to analyze various events
* **Edge Detection:** Compares AI predictions with market consensus to find inefficiencies
* **Intelligent Bet Sizing:** Implements Kelly Criterion for optimal bankroll management
* **Automated Execution:** Places trades via Polymarket Agents SDK
* **Risk Management:** Includes safety features to protect your bankroll

## 🏗️ Architecture

The system consists of three core modules:

1. **Analysis Module**  
   * Uses Claude to analyze upcoming events  
   * Compares predictions with current Polymarket odds  
   * Identifies opportunities with significant edge

2. **Decision Module**  
   * Evaluates opportunities based on edge percentage  
   * Calculates optimal bet size using Kelly Criterion  
   * Manages risk to preserve bankroll

3. **Execution Module**  
   * Connects to Polymarket using their official Agents SDK  
   * Places trades automatically with verification  
   * Implements safety measures and error handling

## ⚙️ Configuration

Edit your `.env` file with the following variables:

```
# Anthropic API key (required for AI functionality)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Flask app settings
FLASK_SECRET_KEY=your_flask_secret_key_here

# SerpAPI key (required for market data)
SERPAPI_API_KEY=your_serpapi_api_key_here

# Polymarket API credentials
POLYMARKET_API_KEY=your_polymarket_api_key_here

# Wallet information (required for transactions)
POLYGON_WALLET_PRIVATE_KEY=your_private_key_here
POLYMARKET_WALLET_ADDRESS=your_wallet_address_here

# Trading settings
INITIAL_BANKROLL=1000
MAX_BET_PERCENTAGE=0.05
MIN_EDGE_PERCENTAGE=0.15
```

> ⚠️ **IMPORTANT**: Never commit your `.env` file or hardcode API keys in the source code. The `.env` file is included in `.gitignore` to prevent accidental exposure of your credentials.

## 🚀 Usage

Start the web interface:
```bash
python app.py
```

Run in simulation mode (no real trades):
```bash
python app.py --simulation
```

Analyze specific markets:
```bash
python polymarket_ai_search.py --query "NBA games tonight"
```

## ⚠️ Risk Warning

Trading involves substantial risk and is not suitable for all investors. Past performance is not indicative of future results. Start with small amounts to test the system before scaling up. Implement proper risk management.

## 🔍 Main Files

* `app.py` - Main entry point for the Flask application
* `polymarket_ai_search.py` - Search and analysis of Polymarket events
* `place_polymarket_bet.py` - Automated bet execution
* `fetch_current_markets.py` - Real-time market data retrieval

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Craig McFarlane

## 🙏 Acknowledgements

* Siraj Raval for original ChatGPT method
* Anthropic for the Claude API
* Polymarket team for the Agents SDK
* All contributors and testers

---

⭐ Star this repo if you find it useful! Join our Discord community to discuss improvements and share results.

**Note:** This system is for educational purposes. Always do your own research before trading.

#!/usr/bin/env python3
"""
Place a bet on a Polymarket market via the CLOB.

Migrated from the archived `py-clob-client` (v1) to `py-clob-client-v2`.
Install with:  pip install py-clob-client-v2   (import name: py_clob_client_v2)

IMPORTANT — values you must confirm for YOUR account (see notes at bottom of file):
  * CLOB_HOST           – v2 may use a different host than v1; verify before live use.
  * POLYMARKET_SIGNATURE_TYPE – depends on how you log in / fund Polymarket.
  * POLYMARKET_FUNDER_ADDRESS – the address that actually HOLDS your funds
                                (your Polymarket deposit/proxy wallet), which is
                                NOT the same as the address of your signing key
                                when you fund through Polymarket directly.
"""
import os
import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- Configuration (read from environment) -------------------------------
# The v1 host was https://clob.polymarket.com. The v2 service may be hosted
# elsewhere (e.g. https://clob-v2.polymarket.com per the Rust v2 client), so this
# is read from env and MUST be confirmed against the v2 README/examples.
CLOB_HOST = os.getenv("CLOB_HOST", "https://clob.polymarket.com")
CHAIN_ID = 137  # Polygon mainnet


def get_nba_markets():
    """Fetch NBA markets from Polymarket's Gamma API."""
    url = "https://gamma-api.polymarket.com/markets"

    now = datetime.datetime.now()
    min_date = now.strftime("%Y-%m-%dT00:00:00Z")

    params = {
        "limit": 20,
        "active": True,
        "start_date_min": min_date
    }

    resp = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        print(f"API request failed with status {resp.status_code}")
        return []

    markets = resp.json()
    if not isinstance(markets, list):
        print(f"Unexpected response format: {type(markets)}")
        return []

    nba_markets = []
    for market in markets:
        question = market.get('question', '').lower()
        if any(term in question for term in ['mavericks', 'nets', 'lakers', 'celtics', 'spread', 'over ']):
            nba_markets.append(market)

    return nba_markets


def parse_token_ids(market):
    """Parse token IDs from market data."""
    token_ids = market.get("clobTokenIds", [])

    if isinstance(token_ids, list):
        return [str(t) for t in token_ids]

    if isinstance(token_ids, str):
        try:
            import ast
            parsed = ast.literal_eval(token_ids)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            if token_ids.startswith("[") and token_ids.endswith("]"):
                tokens = token_ids[1:-1].split(",")
                return [t.strip(' "\'') for t in tokens if t.strip()]
            return [token_ids]

    return []


def _build_client():
    """
    Build an authenticated v2 CLOB client.

    Auth is two-step in v2:
      L1 (private key / EIP-712) -> derive API credentials
      L2 (HMAC API creds)        -> required for placing/cancelling orders
    """
    from py_clob_client_v2 import ApiCreds, ClobClient

    private_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY", "")
    if not private_key:
        print("No private key found in environment variables.")
        print("Add it to .env as POLYGON_WALLET_PRIVATE_KEY=your_key_here")
        print("NEVER hardcode your private key in the script!")
        return None

    # Optional proxy/deposit-wallet settings. When you fund through Polymarket
    # directly, your funds sit in a proxy/deposit wallet whose address differs
    # from your signing key, so both of these are typically required.
    funder = os.getenv("POLYMARKET_FUNDER_ADDRESS") or os.getenv("POLYMARKET_WALLET_ADDRESS")
    sig_type_env = os.getenv("POLYMARKET_SIGNATURE_TYPE")

    # Extra kwargs are only passed when set, so an EOA-only setup still works.
    extra = {}
    if sig_type_env not in (None, ""):
        extra["signature_type"] = int(sig_type_env)
    if funder:
        extra["funder"] = funder

    # Step 1 (L1): derive API credentials from the wallet signature.
    print("Deriving API credentials (L1)...")
    l1_client = ClobClient(host=CLOB_HOST, chain_id=CHAIN_ID, key=private_key, **extra)
    creds = l1_client.create_or_derive_api_key()

    # Optionally reuse pre-generated L2 creds from env instead of deriving them.
    if all(os.getenv(k) for k in ("CLOB_API_KEY", "CLOB_SECRET", "CLOB_PASS_PHRASE")):
        creds = ApiCreds(
            api_key=os.getenv("CLOB_API_KEY"),
            api_secret=os.getenv("CLOB_SECRET"),
            api_passphrase=os.getenv("CLOB_PASS_PHRASE"),
        )

    # Step 2 (L2): fully-authenticated client used for trading.
    print("Initializing authenticated client (L2)...")
    client = ClobClient(host=CLOB_HOST, chain_id=CHAIN_ID, key=private_key, creds=creds, **extra)
    return client


def place_bet(market, amount=1.0, bet_side="BUY"):
    """Place a single GTC limit order on the given market."""
    question = market.get('question', 'Unknown')
    token_ids = parse_token_ids(market)
    if not token_ids:
        print("No token IDs found for this market")
        return False

    try:
        from py_clob_client_v2 import OrderArgs, OrderType, PartialCreateOrderOptions, Side
    except ImportError:
        print("py-clob-client-v2 is not installed. Run: pip install py-clob-client-v2")
        return False

    try:
        client = _build_client()
        if client is None:
            return False

        token_id = token_ids[0]
        side = Side.BUY if bet_side.upper() == "BUY" else Side.SELL

        # Get the current best price from the order book.
        book_resp = requests.get(f"{CLOB_HOST}/book", params={"token_id": token_id})
        price = 0.5  # fallback to 50c if the book is unavailable
        if book_resp.status_code == 200:
            asks = book_resp.json().get("asks", [])
            if asks:
                price = float(asks[0]["price"])

        # NOTE: `size` is the number of OUTCOME SHARES, not USDC. The original
        # v1 script passed the USDC amount straight in as size, which is a bug:
        # at a 0.40 price, 100 shares costs ~40 USDC, not 100. Here we convert
        # the USDC budget into a share count for BUY orders so "bet N USDC"
        # spends roughly N USDC. Adjust if you intend `amount` to mean shares.
        if side == Side.BUY and price > 0:
            size = round(amount / price, 2)
        else:
            size = amount  # for SELL, interpret `amount` as shares to sell

        print(f"Creating GTC order: {size} shares of '{question}' @ {price} ({bet_side})...")
        resp = client.create_and_post_order(
            order_args=OrderArgs(
                token_id=token_id,
                price=price,
                side=side,
                size=size,
            ),
            options=PartialCreateOrderOptions(tick_size="0.01"),
            order_type=OrderType.GTC,
        )

        print("Order submitted.")
        print(f"Response: {resp}")
        return True

    except Exception as e:
        print(f"Error placing bet: {e}")
        return False


def main():
    print("=" * 60)
    print("POLYMARKET BET PLACER")
    print("=" * 60)

    print("Fetching NBA markets...")
    nba_markets = get_nba_markets()
    if not nba_markets:
        print("No NBA markets found")
        return

    print(f"Found {len(nba_markets)} NBA markets")
    for i, market in enumerate(nba_markets[:5]):
        print(f"{i+1}. {market.get('question', 'Unknown')}")

    print("\nWhich market would you like to bet on? (enter number, or 1 for first market)")
    choice = input("> ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(nba_markets):
            print("Invalid selection, using first market")
            idx = 0
    except Exception:
        print("Invalid input, using first market")
        idx = 0

    selected_market = nba_markets[idx]
    question = selected_market.get('question', 'Unknown')
    print(f"\nSelected market: {question}")

    print("\nBet amount in USDC (default: 1.0):")
    amount_str = input("> ").strip()
    try:
        amount = float(amount_str) if amount_str else 1.0
        if amount <= 0:
            print("Invalid amount, using 1.0 USDC")
            amount = 1.0
    except Exception:
        print("Invalid amount, using 1.0 USDC")
        amount = 1.0

    print("\nBet side (buy/sell) - default: buy")
    side = input("> ").strip().upper()
    if side not in ["BUY", "SELL"]:
        print("Invalid side, using BUY")
        side = "BUY"

    print("\n" + "=" * 60)
    print(f"PLACING BET ON: {question}")
    print(f"AMOUNT: {amount} USDC")
    print(f"SIDE: {side}")
    print("=" * 60)

    print("\nConfirm bet placement? (y/n)")
    confirm = input("> ").strip().lower()
    if confirm == 'y':
        place_bet(selected_market, amount, side)
    else:
        print("Bet cancelled")


if __name__ == "__main__":
    main()

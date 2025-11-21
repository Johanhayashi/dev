"""Agent core stub."""

class Agent:
    def __init__(self):
        self.name = "agent"

    def run(self):
        print("Agent running...")

    def check(self):
        print("Agent health check...")
# agent.py
import requests
from dataclasses import dataclass
from typing import List
import logging

logger = logging.getLogger("agent")

@dataclass
class TokenInfo:
    address: str
    symbol: str
    name: str
    price: float
    liquidity: float
    volume_24h: float
    change_24h: float


@dataclass
class TradingSignal:
    token: TokenInfo
    score: int
    action: str  # buy / sell / hold
    reasons: List[str]


class SolanaTradingAgent:

    def fetch_tokens(self, limit=30) -> List[TokenInfo]:
        """
        Busca tokens da DexScreener (Solana only)
        """
        url = "https://api.dexscreener.com/latest/dex/search?q=sol"
        r = requests.get(url, timeout=15)
        data = r.json()

        tokens = []
        for pair in data.get("pairs", []):
            if pair.get("chainId") != "solana":
                continue

            base = pair["baseToken"]
            tokens.append(TokenInfo(
                address=base["address"],
                symbol=base["symbol"],
                name=base.get("name", "Unknown"),
                price=float(pair.get("priceUsd", 0)),
                liquidity=float(pair.get("liquidity", {}).get("usd", 0)),
                volume_24h=float(pair.get("volume", {}).get("h24", 0)),
                change_24h=float(pair.get("priceChange", {}).get("h24", 0))
            ))

        return tokens[:limit]

    def score_token(self, token: TokenInfo) -> TradingSignal:
        score = 0
        reasons = []

        if token.liquidity > 50_000:
            score += 10
            reasons.append("Liquidez saudável")

        if token.volume_24h > 100_000:
            score += 20
            reasons.append("Volume 24h forte")

        if token.change_24h > 20:
            score += 15
            reasons.append("Momentum positivo")

        if token.change_24h < -20:
            score -= 20
            reasons.append("Queda acentuada")

        action = "hold"
        if score >= 40:
            action = "buy"
        elif score <= -20:
            action = "sell"

        return TradingSignal(token, score, action, reasons)

    def scan(self, limit=30, top_k=5):
        tokens = self.fetch_tokens(limit)
        signals = [self.score_token(t) for t in tokens]
        signals.sort(key=lambda s: s.score, reverse=True)
        return signals[:top_k]


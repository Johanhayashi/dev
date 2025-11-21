"""Estratégia simples de exemplo.

Decide comprar se houver movimento de alta recente, vender se queda.
Substitua pelo seu modelo de AI/ML conforme necessário.
"""
from typing import Dict, Any


class Strategy:
    def __init__(self, env: Dict[str, str]):
        self.env = env
        self.threshold = float(env.get("STRATEGY_THRESHOLD", 0.01))  # 1% por padrão

    def decide(self, market: Dict[str, Any], portfolio) -> Dict[str, Any]:
        # market: {"symbol": str, "price": float, "change_1h": float, ...}
        symbol = market.get("symbol", "UNKNOWN")
        price = float(market.get("price", 0))
        change = float(market.get("change_1h", 0))

        # regra simples: se subiu mais que threshold, comprar um pequeno lote
        if change >= self.threshold:
            qty = round((portfolio.cash * 0.01) / price, 8)
            return {"type": "buy", "symbol": symbol, "price": price, "qty": qty}

        # se caiu mais que threshold, vender posição completa
        if change <= -self.threshold and portfolio.positions.get(symbol, 0) > 0:
            qty = portfolio.positions.get(symbol)
            return {"type": "sell", "symbol": symbol, "price": price, "qty": qty}

        return {"type": None}

"""Gerencia risco e dimensionamento simples."""
from typing import Dict, Any


class RiskManager:
    def __init__(self, env: Dict[str, str]):
        self.env = env
        self.max_position_pct = float(env.get("MAX_POSITION_PCT", 0.05))  # 5% default

    def check(self, action: Dict[str, Any], portfolio) -> Dict[str, Any]:
        # Se for buy, dimensiona pra não exceder max_position_pct do portfólio
        if action.get("type") == "buy":
            price = float(action.get("price", 0))
            qty = float(action.get("qty", 0))
            value = price * qty
            max_value = portfolio.total_value() * self.max_position_pct
            if value > max_value:
                # redimensionar
                safe_qty = max_value / price if price > 0 else 0
                action["qty"] = round(safe_qty, 8)
                if action["qty"] <= 0:
                    return None
            # checar caixa
            if value > portfolio.cash:
                return None
        if action.get("type") == "sell":
            symbol = action.get("symbol")
            if portfolio.positions.get(symbol, 0) <= 0:
                return None
        return action

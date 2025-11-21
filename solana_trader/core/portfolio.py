"""Portfólio simulado em memória."""
from typing import Dict


class Portfolio:
    def __init__(self, starting_cash: float = 1000.0):
        self.cash = float(starting_cash)
        self.positions: Dict[str, float] = {}  # symbol -> qty

    def total_value(self, price_lookup=lambda s: 0):
        # preço da posição não disponível por padrão; usar 0 ou passar um lookup
        value_positions = sum(qty * price_lookup(sym) for sym, qty in self.positions.items())
        return self.cash + value_positions

    def apply_trade(self, action: Dict) -> bool:
        t = action.get("type")
        sym = action.get("symbol")
        qty = float(action.get("qty", 0))
        price = float(action.get("price", 0))

        if t == "buy":
            cost = qty * price
            if cost > self.cash:
                return False
            self.cash -= cost
            self.positions[sym] = self.positions.get(sym, 0) + qty
            return True
        elif t == "sell":
            pos = self.positions.get(sym, 0)
            if qty > pos:
                qty = pos
            revenue = qty * price
            self.positions[sym] = pos - qty
            if self.positions[sym] <= 0:
                del self.positions[sym]
            self.cash += revenue
            return True
        return False

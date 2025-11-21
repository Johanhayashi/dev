"""Comando: status — mostra o estado do portfólio (stub)."""
from solana_trader.core.portfolio import Portfolio


def status_text(portfolio: Portfolio) -> str:
    lines = [f"Cash: {portfolio.cash:.2f}"]
    for sym, qty in portfolio.positions.items():
        lines.append(f"{sym}: {qty}")
    return "\n".join(lines)

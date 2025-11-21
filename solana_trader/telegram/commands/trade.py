"""Comando: trade — executar uma ordem via agente (simulação)."""
from solana_trader.core.agent import Agent


def run_trade_once():
    agent = Agent()
    agent.step()
    return True

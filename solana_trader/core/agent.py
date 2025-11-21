"""Agent coordinator: integra data sources, estratégia, risco e portfólio.

Este é um agente de exemplo: usa módulos internos para decidir ações e aplica-las
no `Portfolio` (simulação). Troque o executor de ordens por integração real
quando for necessário.
"""
import logging
import time
from typing import Optional

from solana_trader.core.strategy import Strategy
from solana_trader.core.risk import RiskManager
from solana_trader.core.portfolio import Portfolio
from solana_trader.core.data_sources.dexscreener import DexScreener
from solana_trader.utils import load_env


logger = logging.getLogger("solana_trader.agent")


class Agent:
    def __init__(self, env_path: Optional[str] = None):
        self.env = load_env(env_path) if env_path else load_env(".env")
        self.poll_interval = int(self.env.get("POLLING_INTERVAL", 30))
        self.data_source = DexScreener()
        self.strategy = Strategy(self.env)
        self.risk = RiskManager(self.env)
        self.portfolio = Portfolio(starting_cash=float(self.env.get("STARTING_CASH", 1000)))

    def step(self):
        market = self.data_source.get_market_snapshot()
        logger.debug("Market snapshot: %s", market)

        # Strategy decides an action dict: {"type": "buy"|"sell"|None, "symbol":..., "price":..., "qty":...}
        action = self.strategy.decide(market, self.portfolio)
        if not action or action.get("type") is None:
            logger.info("No action decided this step")
            return

        # Risk manager adjusts/validates the action
        safe_action = self.risk.check(action, self.portfolio)
        if not safe_action:
            logger.info("Action rejected by risk manager: %s", action)
            return

        # Apply action to portfolio (simulated execution)
        executed = self.portfolio.apply_trade(safe_action)
        if executed:
            logger.info("Executed action: %s", safe_action)
        else:
            logger.warning("Failed to execute action: %s", safe_action)

    def run(self):
        logger.info("Agent started; poll interval=%s seconds", self.poll_interval)
        try:
            while True:
                self.step()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            logger.info("Agent stopped by user")

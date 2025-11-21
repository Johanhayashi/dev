"""Watcher que executa o agente uma vez ou em loop (entrypoint).
Use `python solana_trader/watcher.py` para iniciar.
"""
import logging
import argparse
from solana_trader.core.agent import Agent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("solana_trader.watcher")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run only one step and exit")
    args = parser.parse_args()

    agent = Agent()
    if args.once:
        agent.step()
    else:
        agent.run()


if __name__ == "__main__":
    main()

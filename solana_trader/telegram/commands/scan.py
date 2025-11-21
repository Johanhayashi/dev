"""Comando: scan — dispara um scan de mercado (stub)."""
from solana_trader.core.data_sources.dexscreener import DexScreener


def scan_market():
    ds = DexScreener()
    m = ds.get_market_snapshot()
    return m

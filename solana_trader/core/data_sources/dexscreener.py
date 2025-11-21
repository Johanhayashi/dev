"""Stub que simula consulta ao DexScreener (retorna dados mock).
Troque pela implementação real que consome a API do serviço.
"""
import time


class DexScreener:
    def __init__(self):
        pass

    def get_market_snapshot(self):
        # Retorna um dict simples com campos esperados pela Strategy
        # Em produção, substitua por chamada HTTP para buscar price e changes
        now = int(time.time())
        return {"symbol": "SOL-USD", "price": 20.0, "change_1h": 0.015, "timestamp": now}

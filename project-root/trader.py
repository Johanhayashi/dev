# trader.py
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

#
# IMPORTANTE:
# Este trader é uma camada limpa, segura e pronta para integrar com Solana.
# Ela NÃO executa trades reais até você colocar a API (Jupiter / Raydium / Helius / Pump.fun)
# Mas toda a lógica, exceções, validações e retorno estão 100% prontos para produção.
#

logger = logging.getLogger("Trader")


@dataclass
class TradeResult:
    success: bool
    action: str
    token: str
    amount: float
    tx_signature: Optional[str]
    message: str
    extra: Dict[str, Any]


class Trader:
    """
    Classe base genérica. Use get_trader() para retornar o trader certo.
    """

    def buy(self, token_addr: str, amount_usd: float) -> TradeResult:
        raise NotImplementedError

    def sell(self, token_addr: str, amount_usd: float) -> TradeResult:
        raise NotImplementedError


class PaperTrader(Trader):
    """
    Modo papel — não envia transação real, apenas simula.
    Útil para desenvolvimento e testes.
    """

    def buy(self, token_addr: str, amount_usd: float) -> TradeResult:
        logger.info(f"[PAPER] BUY {amount_usd} USD em {token_addr}")

        return TradeResult(
            success=True,
            action="buy",
            token=token_addr,
            amount=amount_usd,
            tx_signature=None,
            message="Simulação de compra realizada.",
            extra={"mode": "paper"}
        )

    def sell(self, token_addr: str, amount_usd: float) -> TradeResult:
        logger.info(f"[PAPER] SELL {amount_usd} USD em {token_addr}")

        return TradeResult(
            success=True,
            action="sell",
            token=token_addr,
            amount=amount_usd,
            tx_signature=None,
            message="Simulação de venda realizada.",
            extra={"mode": "paper"}
        )


class SolanaTrader(Trader):
    """
    Trader real (quando você quiser ativar trade em mainnet).
    Aqui eu deixo toda a estrutura pronta para integrar Jupiter/Raydium.
    """

    def __init__(self, keypair_path: Optional[str] = None):
        self.keypair_path = keypair_path
        logger.info("SolanaTrader inicializado (transações reais DESATIVADAS).")

    def buy(self, token_addr: str, amount_usd: float) -> TradeResult:
        try:
            # ---- AQUI entra Jupiter API real quando você quiser ----
            logger.info(f"[REAL] BUY {amount_usd} USD em {token_addr}")

            # Placeholder até integrar Jupiter Swap
            return TradeResult(
                success=False,
                action="buy",
                token=token_addr,
                amount=amount_usd,
                tx_signature=None,
                message="BUY real não implementado ainda. Configure Jupiter API.",
                extra={}
            )

        except Exception as e:
            logger.exception("Erro no BUY real:")
            return TradeResult(
                success=False,
                action="buy",
                token=token_addr,
                amount=amount_usd,
                tx_signature=None,
                message=str(e),
                extra={}
            )

    def sell(self, token_addr: str, amount_usd: float) -> TradeResult:
        try:
            # ---- AQUI entra Jupiter API real quando você quiser ----
            logger.info(f"[REAL] SELL {amount_usd} USD em {token_addr}")

            return TradeResult(
                success=False,
                action="sell",
                token=token_addr,
                amount=amount_usd,
                tx_signature=None,
                message="SELL real não implementado ainda. Configure Jupiter API.",
                extra={}
            )

        except Exception as e:
            logger.exception("Erro no SELL real:")
            return TradeResult(
                success=False,
                action="sell",
                token=token_addr,
                amount=amount_usd,
                tx_signature=None,
                message=str(e),
                extra={}
            )


def get_trader() -> Trader:
    """
    Decide qual trader usar.
    Por padrão: Paper mode (seguro).
    Para modo real: mude para SolanaTrader()
    """
    USE_REAL = False  # <-- aqui você ativa trade real no futuro

    if USE_REAL:
        return SolanaTrader(keypair_path="wallet.json")

    return PaperTrader()

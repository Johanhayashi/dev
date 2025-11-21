"""Watcher stub to monitor events or prices."""

import time


def watch():
    try:
        while True:
            print("Watching for changes...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Watcher stopped")
# watcher.py (VERSÃO PRO)
import asyncio
import logging
import time
import math
from typing import List, Optional

from utils import get_env
from agent import SolanaTradingAgent
from trader import get_trader
from telegram import Bot

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("watcher")

# ENV CONFIG
BOT_TOKEN = get_env("BOT_TOKEN")
NOTIFY_CHAT = get_env("TELEGRAM_CHAT_ID")
INTERVAL = int(get_env("WATCH_INTERVAL", 300))
RATE_LIMIT_SECONDS = int(get_env("TELEGRAM_RATE_LIMIT_SECONDS", 1))
MAX_MESSAGE_CHARS = 3500
ENABLE_HEARTBEAT = get_env("HEARTBEAT", "false").lower() == "true"

# IA + TRADER
agent = SolanaTradingAgent(max_position_size=100)
trader = get_trader()

bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None

_last_send_ts = 0
_last_signal_hash = None
_last_heartbeat_ts = 0


# --------------------------------------------------------
# Funções auxiliares
# --------------------------------------------------------

def _hash_signals(signals) -> str:
    """Cria hash simples para saber se os sinais mudaram (anti-spam)."""
    return "|".join(f"{s.token.symbol}:{s.score:.3f}" for s in signals)


def _wait_rate_limit() -> float:
    global _last_send_ts
    now = time.time()
    return max(0, RATE_LIMIT_SECONDS - (now - _last_send_ts))


async def _send_text(chat_id: str, text: str):
    """Envio seguro com rate-limit + chunking."""
    global _last_send_ts

    if not bot:
        logger.warning("Bot não configurado.")
        return

    # dividir chunks
    chunks: List[str] = []
    if len(text) <= MAX_MESSAGE_CHARS:
        chunks = [text]
    else:
        buffer = ""
        for line in text.splitlines(keepends=True):
            if len(buffer) + len(line) > MAX_MESSAGE_CHARS:
                chunks.append(buffer)
                buffer = line
            else:
                buffer += line
        if buffer:
            chunks.append(buffer)

    # enviar
    for chunk in chunks:
        wait = _wait_rate_limit()
        if wait > 0:
            await asyncio.sleep(wait)
        try:
            await bot.send_message(chat_id=chat_id, text=chunk)
            _last_send_ts = time.time()
        except Exception as e:
            logger.exception("Erro ao enviar mensagem: %s", e)
            break


def _compose_signal_message(signals) -> str:
    """Texto amigável, resumido e organizado."""
    longs = [s for s in signals if s.action.lower() == "long"]
    shorts = [s for s in signals if s.action.lower() == "short"]

    lines = []
    lines.append(f"🚨 *{len(signals)} Oportunidades Detectadas*")
    lines.append("")

    if longs:
        lines.append("🟢 *Long Opportunities*")
        for s in longs:
            lines.append(
                f"- {s.token.symbol}: score={s.score:.3f}"
            )
        lines.append("")

    if shorts:
        lines.append("🔴 *Short Opportunities*")
        for s in shorts:
            lines.append(
                f"- {s.token.symbol}: score={s.score:.3f}"
            )
        lines.append("")

    return "\n".join(lines)


async def _run_scan():
    """Executa IA + formatação + anti-spam."""
    global _last_signal_hash

    # IA scan (executa em thread para não travar event loop)
    try:
        signals = await asyncio.to_thread(agent.scan, 30, 5)
    except Exception as e:
        logger.exception("Falha no scan IA: %s", e)
        return None

    if not signals:
        logger.info("Nenhuma oportunidade.")
        return None

    # anti-spam: só enviar se novo
    sig_hash = _hash_signals(signals)
    if sig_hash == _last_signal_hash:
        logger.info("Sinais idênticos ao último — não enviando.")
        return None
    _last_signal_hash = sig_hash

    return signals


async def _maybe_send_heartbeat():
    """Envia heartbeat a cada X horas para mostrar que está rodando."""
    global _last_heartbeat_ts
    if not ENABLE_HEARTBEAT:
        return
    now = time.time()
    if now - _last_heartbeat_ts < 3600:  # 1 hora
        return
    _last_heartbeat_ts = now
    await _send_text(NOTIFY_CHAT, "💙 Watcher ativo e monitorando o mercado.")


async def loop():
    """Loop principal com adaptação de mercado e backoff seguro."""
    attempt = 0

    while True:
        try:
            attempt = 0

            signals = await _run_scan()
            if signals:
                msg = _compose_signal_message(signals)
                await _send_text(NOTIFY_CHAT, msg)

            await _maybe_send_heartbeat()

            await asyncio.sleep(INTERVAL)

        except asyncio.CancelledError:
            raise

        except Exception as e:
            attempt += 1
            backoff = min(300, (2 ** attempt) + (0.1 * attempt))
            logger.error(f"Erro no loop: {e}. Backoff {backoff}s")
            await asyncio.sleep(backoff)


def main():
    try:
        asyncio.run(loop())
    except KeyboardInterrupt:
        logger.info("Watcher finalizado manualmente.")
    except Exception as e:
        logger.exception("Falha fatal: %s", e)


if __name__ == "__main__":
    main()
# watcher.py
import asyncio
import logging
from utils import get_env
from telegram import Bot
from agent import SolanaTradingAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("watcher")

BOT_TOKEN = get_env("BOT_TOKEN")
CHAT_ID = get_env("TELEGRAM_CHAT_ID")
INTERVAL = int(get_env("WATCH_INTERVAL", 300))

bot = Bot(token=BOT_TOKEN)
agent = SolanaTradingAgent()


async def send(chat_id, text):
    try:
        await bot.send_message(chat_id, text)
    except Exception as e:
        logger.error("Falha ao enviar no Telegram: %s", e)


async def loop():
    while True:
        signals = agent.scan(limit=30, top_k=5)
        msg = "📈 **Sinais detectados:**\n\n"
        for s in signals:
            msg += f"→ {s.token.symbol} | Score {s.score}\n"
            for r in s.reasons:
                msg += f"   • {r}\n"
            msg += "\n"
        await send(CHAT_ID, msg)
        await asyncio.sleep(INTERVAL)


def main():
    asyncio.run(loop())


if __name__ == "__main__":
    main()

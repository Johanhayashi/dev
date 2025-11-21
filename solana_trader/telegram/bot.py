"""Bot Telegram simples usando Bot API via requests (lightweight stub).
Substitua por `python-telegram-bot` se preferir funcionalidades mais completas.
"""
import os
import requests
from typing import Optional

from solana_trader.utils import load_env


class TelegramBot:
    def __init__(self, token: Optional[str] = None):
        env = load_env()
        self.token = token or env.get("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN not set in env")
        self.base = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id: int, text: str):
        resp = requests.post(f"{self.base}/sendMessage", json={"chat_id": chat_id, "text": text})
        return resp.json()


if __name__ == "__main__":
    # quick test (requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in env)
    env = load_env()
    bot_token = env.get("TELEGRAM_BOT_TOKEN")
    chat_id = env.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        tb = TelegramBot(bot_token)
        print(tb.send_message(int(chat_id), "solana_trader bot initialized"))
    else:
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env to test")

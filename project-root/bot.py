# bot.py
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from utils import get_env
from agent import SolanaTradingAgent
from trader import get_trader

# ------------------------- CONFIG -------------------------
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN")
CHAT_ID = get_env("TELEGRAM_CHAT_ID")

if not BOT_TOKEN:
    raise RuntimeError("ERRO: TELEGRAM_BOT_TOKEN não definido no .env")

# ------------------------- OBJETOS -------------------------
agent = SolanaTradingAgent(max_position_size=100)
trader = get_trader()

# ------------------------- HANDLERS -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Bot Solana ativado!\n\n"
        "Comandos disponíveis:\n"
        "/status – ver status do bot\n"
        "/scan – escanear oportunidades\n"
        "/sendtest – testar envio\n"
        "/trade buy|sell <token> <valor>\n"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"📊 STATUS DO BOT\n\n"
        f"Posições abertas: {len(agent.positions)}\n"
        f"Total trades: {len(agent.trade_history)}\n"
        f"Módulo trader: {type(trader).__name__}"
    )
    await update.message.reply_text(text)

async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Escaneando oportunidades…")

    signals = agent.scan(limit=20, top_k=3)

    if not signals:
        await update.message.reply_text("Nenhuma oportunidade encontrada.")
        return

    for s in signals:
        msg = (
            f"📌 Token: {s.token.symbol}\n"
            f"Address: {s.token.address}\n"
            f"Score: {s.score}\n"
            "Motivos:\n" + "\n".join(f"• {r}" for r in s.reasons)
        )
        await update.message.reply_text(msg)

async def send_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Testa envio automático para TELEGRAM_CHAT_ID"""
    target = CHAT_ID or update.effective_chat.id

    await update.message.reply_text(f"Enviando teste para {target}…")

    try:
        await context.bot.send_message(
            chat_id=target,
            text="✅ Teste de envio: bot funcionando!"
        )
        await update.message.reply_text("Mensagem enviada com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"Erro ao enviar: {e}")

async def trade_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text(
                "Uso correto:\n/trade buy|sell <token_address> <valor>"
            )
            return
        
        side, token_addr, value = args[0], args[1], float(args[2])

        if side == "buy":
            res = trader.buy(token_addr, value)
        elif side == "sell":
            res = trader.sell(token_addr, value)
        else:
            await update.message.reply_text("Opção inválida: use buy ou sell.")
            return

        await update.message.reply_text(f"Resultado:\n{res}")

    except Exception as e:
        await update.message.reply_text(f"Erro no trade: {e}")

# ------------------------- MAIN -------------------------
def main():
    logger.info("Iniciando bot…")

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("scan", scan_cmd))
    app.add_handler(CommandHandler("sendtest", send_test))
    app.add_handler(CommandHandler("trade", trade_cmd))

    logger.info("Bot rodando! Aguarde mensagens no Telegram.")
    app.run_polling()

if __name__ == "__main__":
    main()


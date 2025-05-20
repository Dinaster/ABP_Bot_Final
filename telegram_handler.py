import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application
from signal_engine import analyze_market
from io import BytesIO

chat_ids = set()

# Leer ID desde variable de entorno si existe
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
if GROUP_CHAT_ID:
    try:
        group_id = int(GROUP_CHAT_ID)
        chat_ids.add(group_id)
        print(f"✅ Loaded GROUP_CHAT_ID from .env: {group_id}")
    except Exception as e:
        print(f"⚠️ Error loading GROUP_CHAT_ID: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(GROUP_CHAT_ID):
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text("✅ Alpha Break Pro 777 is online. Use /check BTC-USD")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(GROUP_CHAT_ID):
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    if not context.args:
        await update.message.reply_text("⚠️ Please use the command like: /check BTC-USD")
        return
    pair = context.args[0]
    signal, chart = analyze_market(pair)
    if signal:
        await update.message.reply_text(signal)
        if chart:
            await update.message.reply_photo(photo=chart)
    else:
        await update.message.reply_text("❌ No signal for this pair.")

async def why(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(GROUP_CHAT_ID):
        return
    await update.message.reply_text("📊 This signal is based on EMA, MACD, Volume and ATR-based Stop Loss & Take Profit.")

async def periodic_analysis(app: Application):
    import asyncio
    pairs = ["BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD"]
    while True:
        for pair in pairs:
            signal, chart = analyze_market(pair)
            if signal:
                for cid in chat_ids:
                    await app.bot.send_message(cid, signal)
                    if chart:
                        await app.bot.send_photo(cid, photo=chart)
        await asyncio.sleep(1800)  # Every 30 minutes


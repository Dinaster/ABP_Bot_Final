# telegram_handler.py
import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application
from signal_engine import analyze_market
from io import BytesIO

chat_ids = set()

# Leer ID desde variable de entorno
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
if GROUP_CHAT_ID:
    try:
        chat_ids.add(int(GROUP_CHAT_ID))
        print(f"✅ Loaded GROUP_CHAT_ID from .env: {GROUP_CHAT_ID}")
    except Exception as e:
        print(f"⚠️ Error reading GROUP_CHAT_ID: {e}")

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    print(f"📢 /start received from chat ID: {cid}")
    
    if GROUP_CHAT_ID and cid != int(GROUP_CHAT_ID):
        print("⛔ Ignoring unauthorized chat.")
        return

    chat_ids.add(cid)
    await update.message.reply_text("✅ Alpha Break Pro 777 is online. Use /check BTC-USD")

# CHECK
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    print(f"📢 /check received from chat ID: {cid}")
    
    if GROUP_CHAT_ID and cid != int(GROUP_CHAT_ID):
        print("⛔ Unauthorized chat tried to use /check")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Please use like /check BTC-USD")
        return

    pair = context.args[0]
    print(f"🔍 Analyzing pair: {pair}")
    
    signal, chart = analyze_market(pair)
    print(f"📈 Signal: {signal}")

    if signal:
        await update.message.reply_text(signal)
        if chart:
            await update.message.reply_photo(photo=chart)
    else:
        await update.message.reply_text("❌ No signal for this pair.")

import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application
from signal_engine import analyze_market

chat_ids = set()
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
if GROUP_CHAT_ID:
    try:
        chat_ids.add(int(GROUP_CHAT_ID))
    except Exception as e:
        print(f"⚠️ Error setting GROUP_CHAT_ID: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if cid != int(GROUP_CHAT_ID):
        return
    await update.message.reply_text("✅ Bot is online. Use /check BTC-USD")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if cid != int(GROUP_CHAT_ID):
        return
    if not context.args:
        await update.message.reply_text("⚠️ Please use like /check BTC-USD")
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
    cid = update.effective_chat.id
    if cid != int(GROUP_CHAT_ID):
        return
    await update.message.reply_text("📊 This signal is based on EMA, MACD, Volume and ATR.")

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
        await asyncio.sleep(1800)
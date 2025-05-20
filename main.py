import os
import asyncio
from telegram.ext import ApplicationBuilder, ContextTypes
from setup_handlers import setup_handlers
from telegram_handler import periodic_analysis

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def periodic_job(context: ContextTypes.DEFAULT_TYPE):
    app = context.application
    await periodic_analysis(app)

async def main():
    print("🚀 Alpha Break Pro 777 bot is starting...", flush=True)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    setup_handlers(app)
    app.job_queue.run_repeating(periodic_job, interval=3600, first=10)
    await app.initialize()
    await app.start()
    print("✅ Bot is running...", flush=True)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

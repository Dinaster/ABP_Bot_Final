from telegram.ext import CommandHandler
from telegram_handler import start, check, why

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("why", why))

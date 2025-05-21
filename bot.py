from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")














#lanzar el bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
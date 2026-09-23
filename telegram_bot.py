import logging
from telegram.ext import Application
from telegram import Update
from config.settings import Config
from bot.handlers import setup_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = Config.TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError("Установите переменную окружения TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(token).build()
    
    setup_handlers(application)

    logger.info("Starting Telegram bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования для отладки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Уменьшаем уровень логирования для библиотеки httpx
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду /start и предоставляет информацию о боте."""
    await update.message.reply_text("Привет! Я могу создавать опросы с несколькими вариантами ответа. Используйте команду /poll.")

async def send_multiple_choice_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет опрос с несколькими вариантами ответа в чат.
    Бот должен быть администратором в группе или канале, чтобы создавать опросы.
    """
    if update.effective_chat.type == 'private':
        await update.message.reply_text("Эта команда работает только в группах и каналах. Добавьте меня в группу и используйте команду там.")
        return

    # Вопрос для опроса
    question = "Какой ваш любимый язык программирования?"
    # Варианты ответов
    options = ["Python", "JavaScript", "Java", "C++"]
    # Разрешает выбирать несколько вариантов
    allows_multiple_answers = True
    
    try:
        # Отправка опроса в чат
        await context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=question,
            options=options,
            is_anonymous=False, # Опрос не будет анонимным
            allows_multiple_answers=allows_multiple_answers,
        )
        logger.info("Отправлен опрос с несколькими вариантами ответа.")
    except Exception as e:
        logger.error(f"Не удалось отправить опрос: {e}")
        await update.message.reply_text(f"Не удалось отправить опрос. Возможно, у бота нет прав администратора для создания опросов. Ошибка: {e}")

def main() -> None:
    """Запускает бота."""
    # Получение токена из BotFather и создание экземпляра Application
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("poll", send_multiple_choice_poll))

    # Запуск бота в режиме long-polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()


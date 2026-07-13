import logging
import os

from groq import AsyncGroq
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
Ты — FOODHALL AI, цифровой помощник фудхолла и кофейни.
Отвечай на русском языке, понятно и по делу.
Помогай с блюдами, напитками, рецептами, сервисом,
маркетингом и работой фудхолла.
Не выдумывай цены, составы, акции и правила заведения.
""".strip()

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    user = update.effective_user
    name = user.first_name if user and user.first_name else "Гость"

    await update.effective_message.reply_text(
        f"{name}, FOODHALL AI запущен. Задай вопрос."
    )


async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message

    if not message or not message.text:
        return

    try:
        async with AsyncGroq(
            api_key=os.environ["GROQ_API_KEY"],
            timeout=60.0,
            max_retries=2,
        ) as client:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": message.text,
                    },
                ],
                temperature=0.4,
                max_completion_tokens=800,
            )

        answer = response.choices[0].message.content or (
            "Groq вернул пустой ответ."
        )

        for index in range(0, len(answer), 4000):
            await message.reply_text(
                answer[index:index + 4000]
            )

    except Exception as error:
        logger.exception(
            "Ошибка при обработке сообщения: %s",
            error,
        )

        await message.reply_text(
            "Не удалось получить ответ. Проверь логи Railway."
        )


def main() -> None:
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not telegram_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не найден")

    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY не найден")

    application = (
        Application.builder()
        .token(telegram_token)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat,
        )
    )

    logger.info(
        "FOODHALL AI запущен. Модель: %s",
        MODEL,
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()

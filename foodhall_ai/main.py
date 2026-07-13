import logging
import os

from groq import AsyncGroq
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters


MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b",
)

SYSTEM_PROMPT = (
    "Ты — FOODHALL AI, цифровой помощник фудхолла и кофейни. "
    "Отвечай на русском языке, понятно и по делу. "
    "Помогай с блюдами, напитками, рецептами, сервисом, "
    "маркетингом и операционной работой фудхолла. "
    "Не выдумывай цены, составы, акции и правила заведения. "
    "Если точной внутренней информации нет, прямо сообщай об этом."
)


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def ask_groq(question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY не найден")

    async with AsyncGroq(
        api_key=api_key,
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
                    "content": question,
                },
            ],
        )

    if not response.choices:
        raise RuntimeError("Groq не вернул варианты ответа")

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("Groq вернул пустой ответ")

    return answer.strip()


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message
    user = update.effective_user

    if not message:
        return

    name = "Гость"

    if user and user.first_name:
        name = user.first_name

    await message.reply_text(
        f"{name}, FOODHALL AI запущен. Задай вопрос."
    )


async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message

    if not message:
        return

    if not message.text:
        return

    try:
        answer = await ask_groq(message.text)

        for index in range(0, len(answer), 3900):
            await message.reply_text(
                answer[index:index + 3900]
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
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN не найден"
        )

    if not groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY не найден"
        )

    application = (
        Application.builder()
        .token(telegram_token)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
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
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()

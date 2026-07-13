import asyncio
import json
import logging
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = """
Ты — FOODHALL AI, цифровой помощник фудхолла и кофейни.

Отвечай на русском языке.
Пиши понятно, конкретно и без лишней воды.
Помогай с блюдами, напитками, рецептами, сервисом,
маркетингом и работой фудхолла.

Если точной внутренней информации нет, прямо сообщай об этом.
Не выдумывай цены, составы, акции и правила заведения.
""".strip()


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def ask_groq_sync(question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY не найден")

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        "temperature": 0.4,
        "max_completion_tokens": 800,
    }

    request = Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Ошибка Groq API {error.code}: {details}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Нет соединения с Groq API: {error.reason}"
        ) from error

    choices = result.get("choices", [])

    if not choices:
        raise RuntimeError("Groq API не вернул ответ")

    answer = choices[0].get("message", {}).get("content", "").strip()

    if not answer:
        raise RuntimeError("Groq API вернул пустой ответ")

    return answer


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "Привет! Я FOODHALL AI. Задай мне вопрос."
        )


async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message

    if not message or not message.text:
        return

    try:
        answer = await asyncio.to_thread(
            ask_groq_sync,
            message.text,
        )

        for start_index in range(0, len(answer), 4000):
            await message.reply_text(
                answer[start_index:start_index + 4000]
            )

    except Exception:
        logger.exception("Ошибка при обработке сообщения")

        await message.reply_text(
            "Не удалось получить ответ. "
            "Проверь GROQ_API_KEY и логи Railway."
        )


def main() -> None:
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    groq_api_key = os.getenv("GROQ_API_KEY")

    missing_variables = []

    if not telegram_token:
        missing_variables.append("TELEGRAM_BOT_TOKEN")

    if not groq_api_key:
        missing_variables.append("GROQ_API_KEY")

    if missing_variables:
        raise RuntimeError(
            "Не найдены переменные: "
            + ", ".join(missing_variables)
        )

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

    logger.info("FOODHALL AI запущен")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()

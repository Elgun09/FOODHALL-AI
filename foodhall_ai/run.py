from telegram_bot import create_bot
import os

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found")

    app = create_bot(token)
    app.run_polling()

if __name__ == "__main__":
    main()

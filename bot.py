# ==================== EsprssAI Telegram Bot ====================
# Автор: l3nuksoid
# Версия: 2.0 (с поддержкой Railway и Linux)
# ===============================================================

import os
import telebot
import openai

# 🔑 === НАСТРОЙКА КЛЮЧЕЙ ===
# Бот сначала попытается взять ключи из переменных окружения.
# Если не найдёт — использует значения, указанные ниже.
BOT_TOKEN = os.getenv("BOT_TOKEN") or "вставь_сюда_токен_бота_если_тестируешь_локально"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "вставь_сюда_API_ключ_OpenAI"

# === ИНИЦИАЛИЗАЦИЯ ===
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# === ОБРАБОТЧИК КОМАНДЫ /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я — EsprssAI ☕\n"
        "Задай мне вопрос или попроси сгенерировать код."
    )

# === ОСНОВНОЙ ОБРАБОТЧИК СООБЩЕНИЙ ===
@bot.message_handler(func=lambda _: True)
def handle_message(message):
    user_text = message.text.strip()

    try:
        # === Запрос к OpenAI ===
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # можно заменить на gpt-4-turbo, если доступен
            messages=[
                {"role": "system", "content": "Ты — умный, дружелюбный Telegram-бот EsprssAI."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message["content"]

        # === Отправка ответа пользователю ===
        bot.send_message(message.chat.id, reply)

    except openai.error.AuthenticationError:
        bot.send_message(
            message.chat.id,
            "❌ Ошибка: неверный OpenAI API ключ. Проверь переменную окружения OPENAI_API_KEY."
        )

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

# === ЗАПУСК БОТА ===
if __name__ == "__main__":
    print("✅ EsprssAI запущен и ждёт сообщений...")
    bot.infinity_polling()


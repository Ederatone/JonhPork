# 🤖 JonhPork — Telegram бот-нагадувач

## 🔍 Опис

**JonhPork** — це телеграм-бот, який дозволяє користувачам створювати персональні нагадування. Завдяки простому інтерфейсу через Telegram, бот допомагає не забути про важливі справи.

## 🛠 Технології

- [Python 3.x](https://www.python.org/)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [pytz](https://pypi.org/project/pytz/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pytest](https://docs.pytest.org/en/stable/)

## 📦 Встановлення

1. Клонуйте репозиторій:

```
git clone https://github.com/Ederatone/JonhPork.git
cd JonhPork
```

2. Встановіть залежності

```
pip install -r requirements.txt
```

3. Створіть файл `.env` у корені проєкту та додайте:

```
BOT_TOKEN=your_telegram_bot_token
```

4. Запустіть бота:

```
python run.py
```
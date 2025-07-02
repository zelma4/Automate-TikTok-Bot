#!/bin/bash

# TikTok Bot Production Startup Script

echo "🤖 Запуск TikTok Bot для продакшену..."

# Перевірити Python середовище
if [ ! -d ".venv" ]; then
    echo "❌ Віртуальне середовище не знайдено!"
    echo "Запустіть: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Активувати віртуальне середовище
source .venv/bin/activate

# Перевірити .env файл
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не знайдено!"
    echo "Створіть .env файл з TikTok кредами:"
    echo "TIKTOK_USERNAME=ваш_username"
    echo "TIKTOK_PASSWORD=ваш_пароль"
    exit 1
fi

# Перевірити наявність серіалів
if [ ! -d "Serial" ] || [ -z "$(ls -A Serial)" ]; then
    echo "⚠️  Папка Serial пуста або не існує"
    echo "Скопіюйте ваші .mkv файли у папку Serial/"
fi

echo "✅ Середовище готове до роботи"
echo ""
echo "Доступні команди:"
echo "  python run_bot.py setup     # Початкове налаштування"
echo "  python run_bot.py process   # Нарізати відео"
echo "  python run_bot.py run       # Запустити бота"
echo ""

# Якщо передано аргумент - виконати команду
if [ $# -eq 1 ]; then
    echo "🚀 Виконуємо: python run_bot.py $1"
    python run_bot.py $1
fi

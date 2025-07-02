#!/usr/bin/env python3
"""
Скрипт запуску та управління TikTok ботом
"""

import asyncio
import sys
import argparse
from pathlib import Path
import logging

# Імпортуємо наші модулі
from tiktok_bot import TikTokBot

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def process_videos():
    """Обробити всі відео та створити кліпи"""
    logger.info("🎬 Початок обробки відео...")
    bot = TikTokBot()
    await bot.process_all_videos()
    logger.info("✅ Обробка відео завершена!")


async def run_bot():
    """Запустити бота в безперервному режимі"""
    logger.info("🤖 Запуск TikTok бота...")
    bot = TikTokBot()
    await bot.run_continuous()


def setup_project():
    """Початкове налаштування проекту"""
    logger.info("🔧 Налаштування проекту...")
    
    # Створити необхідні папки
    folders = ['clips', 'logs', 'sessions']
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        logger.info(f"📁 Створено папку: {folder}")
    
    # Перевірити наявність серіалів
    serial_folder = Path("Serial")
    if not serial_folder.exists():
        logger.warning("⚠️  Папка 'Serial' не знайдена. Створюємо...")
        serial_folder.mkdir(exist_ok=True)
        logger.info("📂 Скопіюйте ваші серіали у папку 'Serial'")
    else:
        video_files = list(serial_folder.glob("*.mkv"))
        logger.info(f"📺 Знайдено {len(video_files)} відеофайлів")
    
    logger.info("✅ Налаштування завершено!")


def main():
    """Головна функція"""
    parser = argparse.ArgumentParser(description='TikTok Bot')
    parser.add_argument(
        'command',
        choices=['setup', 'process', 'run'],
        help='Команда для виконання'
    )
    
    args = parser.parse_args()
    
    try:
        if args.command == 'setup':
            setup_project()
        elif args.command == 'process':
            asyncio.run(process_videos())
        elif args.command == 'run':
            asyncio.run(run_bot())
            
    except KeyboardInterrupt:
        logger.info("\n👋 Зупинка програми...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

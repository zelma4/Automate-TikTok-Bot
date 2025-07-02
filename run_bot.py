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


async def post_now():
    """Опублікувати наступне відео з черги зараз"""
    logger.info("🚀 Миттєвий постинг...")
    bot = TikTokBot()
    
    if not bot.scheduler.schedule["queue"]:
        logger.warning("❌ Черга порожня! Спочатку обробіть відео.")
        return
    
    video_path = Path(bot.scheduler.schedule["queue"][0])
    if not video_path.exists():
        logger.error(f"❌ Файл не знайдено: {video_path}")
        return
    
    success = await bot.uploader.upload_video(video_path)
    if success:
        # Видалити з черги після успішного завантаження
        bot.scheduler.schedule["queue"].pop(0)
        bot.scheduler.save_schedule()
        logger.info(f"✅ Відео опубліковано: {video_path.name}")
    else:
        logger.error("❌ Помилка завантаження відео")


async def post_specific(file_path: str):
    """Опублікувати конкретний файл"""
    logger.info(f"🎯 Публікація файлу: {file_path}")
    bot = TikTokBot()
    
    video_path = Path(file_path)
    if not video_path.exists():
        logger.error(f"❌ Файл не знайдено: {video_path}")
        return
    
    success = await bot.uploader.upload_video(video_path)
    if success:
        logger.info(f"✅ Відео опубліковано: {video_path.name}")
    else:
        logger.error("❌ Помилка завантаження відео")


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
        choices=['setup', 'process', 'run', 'post', 'upload'],
        help='Команда для виконання'
    )
    parser.add_argument(
        '--file',
        help='Шлях до конкретного файлу для завантаження'
    )
    
    args = parser.parse_args()
    
    try:
        if args.command == 'setup':
            setup_project()
        elif args.command == 'process':
            asyncio.run(process_videos())
        elif args.command == 'run':
            asyncio.run(run_bot())
        elif args.command == 'post':
            asyncio.run(post_now())
        elif args.command == 'upload':
            if args.file:
                asyncio.run(post_specific(args.file))
            else:
                logger.error("❌ Для команди 'upload' потрібно вказати --file")
                sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n👋 Зупинка програми...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

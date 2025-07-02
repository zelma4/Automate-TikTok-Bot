#!/usr/bin/env python3
"""
TikTok Bot для автоматичного нарізання серіалів та завантаження у TikTok
"""

import os
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import List, Dict, Optional
import random

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tiktok_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VideoProcessor:
    """Клас для обробки відеофайлів"""
    
    def __init__(self, input_dir: str = "Serial", output_dir: str = "clips"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def get_video_files(self) -> List[Path]:
        """Отримати список відеофайлів"""
        video_extensions = ['.mkv', '.mp4', '.avi', '.mov', '.wmv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(self.input_dir.glob(f"*{ext}"))
            
        return sorted(video_files)
    
    def cut_video_to_clips(self, video_path: Path, clip_duration: int = 60) -> List[Path]:
        """
        Нарізати відео на кліпи заданої тривалості
        
        Args:
            video_path: Шлях до відеофайлу
            clip_duration: Тривалість кліпа в секундах (за замовчуванням 60с)
            
        Returns:
            Список шляхів до створених кліпів
        """
        try:
            import ffmpeg
            
            # Отримати інформацію про відео
            probe = ffmpeg.probe(str(video_path))
            
            # Спробувати отримати тривалість з різних джерел
            duration = None
            if 'format' in probe and 'duration' in probe['format']:
                duration = float(probe['format']['duration'])
            else:
                for stream in probe['streams']:
                    if stream['codec_type'] == 'video' and 'duration' in stream:
                        duration = float(stream['duration'])
                        break
                        
            if duration is None:
                logger.error(f"Не вдалося визначити тривалість відео {video_path}")
                return []
            
            clips = []
            clip_count = int(duration // clip_duration)
            
            base_name = video_path.stem
            logger.info(f"Нарізання {video_path.name} на {clip_count} кліпів")
            
            for i in range(clip_count):
                start_time = i * clip_duration
                output_name = f"{base_name}_clip_{i+1:03d}.mp4"
                output_path = self.output_dir / output_name
                
                # Нарізати відео за допомогою FFmpeg
                (
                    ffmpeg
                    .input(str(video_path), ss=start_time, t=clip_duration)
                    .output(
                        str(output_path),
                        vcodec='libx264',
                        acodec='aac',
                        video_bitrate='2M',
                        audio_bitrate='128k',
                        vf='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',  # TikTok розмір 9:16
                        r=30  # 30 FPS для TikTok
                    )
                    .overwrite_output()
                    .run(quiet=True)
                )
                
                if output_path.exists():
                    clips.append(output_path)
                    logger.info(f"Створено кліп: {output_name}")
                
            return clips
            
        except Exception as e:
            logger.error(f"Помилка при нарізанні відео {video_path}: {e}")
            return []


class TikTokUploader:
    """Клас для завантаження відео у TikTok через API"""
    
    def __init__(self, config_file: str = "tiktok_config.json"):
        self.config_file = config_file
        self.load_config()
        
        # Ініціалізувати API клієнт
        from tiktok_api import TikTokAPIClient
        self.api_client = TikTokAPIClient()
        
    def load_config(self):
        """Завантажити конфігурацію TikTok"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # Створити шаблон конфігурації
            self.config = {
                "hashtags": [
                    "#серіал", "#гінніджорджія", "#netflix", "#відео"
                ],
                "description_templates": [
                    "Найкращі моменти з серіалу! 🔥",
                    "Це було епічно! 😱",
                    "Хто ще дивиться цей серіал? 💕",
                    "Ваша реакція на цю сцену? 🤔"
                ],
                "privacy_level": "PUBLIC_TO_EVERYONE"
            }
            self.save_config()
            
    def save_config(self):
        """Зберегти конфігурацію"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def generate_description(self, video_path: Path) -> str:
        """
        Згенерувати опис відео на основі назви файлу
        
        Args:
            video_path: Шлях до відеофайлу
            
        Returns:
            Згенерований опис
        """
        filename = video_path.stem
        
        # Парсинг назви файлу
        # (приклад: "Ginny & Georgia. S03 E01. (Title)_clip_001")
        series_name = "Невідомий серіал"
        season = ""
        episode = ""
        clip_number = ""
        
        try:
            # Витягти назву серіалу (до першої крапки)
            if "." in filename:
                series_name = filename.split(".")[0].strip()
            
            # Знайти сезон і епізод (S03 E01)
            import re
            season_match = re.search(r'S(\d+)', filename)
            episode_match = re.search(r'E(\d+)', filename)
            clip_match = re.search(r'clip_(\d+)', filename)
            
            if season_match:
                season = f"S{season_match.group(1)}"
            if episode_match:
                episode = f"E{episode_match.group(1)}"
            if clip_match:
                clip_number = f"частина {clip_match.group(1)}"
                
        except Exception as e:
            logger.warning(f"Помилка парсингу назви файлу: {e}")
        
        # Створити опис
        description_parts = []
        
        # Додати назву серіалу
        if series_name != "Невідомий серіал":
            description_parts.append(f"🎬 {series_name}")
        
        # Додати сезон та епізод
        if season and episode:
            description_parts.append(f"📺 {season} {episode}")
        
        # Додати номер кліпу
        if clip_number:
            description_parts.append(f"🎞️ {clip_number}")
        
        # Додати випадковий шаблон
        template = random.choice(self.config["description_templates"])
        description_parts.append(template)
        
        # Поєднати все
        description = " | ".join(description_parts)
        
        # Додати хештеги
        hashtags = " ".join(self.config["hashtags"])
        if hashtags:
            description += f"\n\n{hashtags}"
        
        return description
    async def upload_video(self, video_path: Path,
                           description: str = None) -> bool:
        """
        Завантажити відео у TikTok через API
        
        Args:
            video_path: Шлях до відеофайлу
            description: Опис відео
            
        Returns:
            True якщо завантаження успішне
        """
        try:
            # Перевірити авторизацію
            if not self.api_client.is_authenticated():
                logger.error(
                    "API не авторизований. Запустіть setup_tiktok_api.py"
                )
                return False
            
            # Створити опис якщо не вказаний
            if not description:
                description = self.generate_description(video_path)
            
            # Отримати назву файлу для заголовку
            title = video_path.stem
            
            # Завантажити відео через API
            result = self.api_client.upload_video(
                video_path=str(video_path),
                title=title,
                description=description,
                privacy_level=self.config.get("privacy_level", "SELF_ONLY")
            )
            
            if result:
                logger.info(f"Відео успішно завантажено: {video_path.name}")
                return True
            else:
                logger.error(f"Помилка завантаження: {video_path.name}")
                return False
            
        except Exception as e:
            logger.error(f"Помилка при завантаженні {video_path}: {e}")
            return False


class ScheduleManager:
    """Клас для управління розкладом публікацій"""
    
    def __init__(self, schedule_file: str = "schedule.json"):
        self.schedule_file = schedule_file
        self.load_schedule()
        
    def load_schedule(self):
        """Завантажити розклад"""
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                self.schedule = json.load(f)
        else:
            # Створити базовий розклад (3-4 відео на день)
            self.schedule = {
                "posts_per_day": 3,
                "posting_times": ["09:00", "15:00", "21:00"],
                "last_upload": None,
                "queue": []
            }
            self.save_schedule()
            
    def save_schedule(self):
        """Зберегти розклад"""
        with open(self.schedule_file, 'w', encoding='utf-8') as f:
            json.dump(self.schedule, f, indent=2, ensure_ascii=False)
    
    def add_videos_to_queue(self, video_paths: List[Path]):
        """Додати відео до черги"""
        for video_path in video_paths:
            self.schedule["queue"].append(str(video_path))
        self.save_schedule()
        logger.info(f"Додано {len(video_paths)} відео до черги")
    
    def get_next_upload_time(self) -> datetime:
        """Отримати час наступного завантаження"""
        now = datetime.now()
        posting_times = self.schedule["posting_times"]
        
        # Знайти наступний час публікації сьогодні
        for time_str in posting_times:
            hour, minute = map(int, time_str.split(':'))
            upload_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if upload_time > now:
                return upload_time
                
        # Якщо всі часи сьогодні пройшли, взяти перший час завтра
        hour, minute = map(int, posting_times[0].split(':'))
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    def should_upload_now(self) -> bool:
        """Перевірити чи час завантажувати зараз"""
        if not self.schedule["queue"]:
            return False
            
        now = datetime.now()
        next_time = self.get_next_upload_time()
        
        # Завантажувати якщо різниця менше 5 хвилин
        return abs((next_time - now).total_seconds()) < 300


class TikTokBot:
    """Основний клас бота"""
    
    def __init__(self):
        self.processor = VideoProcessor()
        self.uploader = TikTokUploader()
        self.scheduler = ScheduleManager()
        
    async def process_all_videos(self):
        """Обробити всі відео та додати до черги"""
        video_files = self.processor.get_video_files()
        logger.info(f"Знайдено {len(video_files)} відеофайлів")
        
        all_clips = []
        for video_file in video_files:
            clips = self.processor.cut_video_to_clips(video_file)
            all_clips.extend(clips)
            
        if all_clips:
            self.scheduler.add_videos_to_queue(all_clips)
            logger.info(f"Всього створено {len(all_clips)} кліпів")
            
    async def upload_scheduled_videos(self):
        """Завантажити відео згідно розкладу"""
        if self.scheduler.should_upload_now() and self.scheduler.schedule["queue"]:
            video_path = Path(self.scheduler.schedule["queue"].pop(0))
            
            if video_path.exists():
                success = await self.uploader.upload_video(video_path)
                if success:
                    self.scheduler.schedule["last_upload"] = datetime.now().isoformat()
                    self.scheduler.save_schedule()
                else:
                    # Повернути відео в чергу якщо завантаження не вдалося
                    self.scheduler.schedule["queue"].insert(0, str(video_path))
                    self.scheduler.save_schedule()
            else:
                logger.warning(f"Файл не знайдено: {video_path}")
                
    async def run_continuous(self):
        """Запустити бота в безперервному режимі"""
        logger.info("Запуск TikTok бота...")
        
        while True:
            try:
                await self.upload_scheduled_videos()
                await asyncio.sleep(300)  # Перевіряти кожні 5 хвилин
                
            except KeyboardInterrupt:
                logger.info("Зупинка бота...")
                break
            except Exception as e:
                logger.error(f"Помилка в основному циклі: {e}")
                await asyncio.sleep(60)  # Чекати хвилину перед повторною спробою


async def main():
    """Головна функція"""
    bot = TikTokBot()
    await bot.run_continuous()


if __name__ == "__main__":
    asyncio.run(main())

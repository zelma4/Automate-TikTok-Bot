#!/usr/bin/env python3
"""
Тест генерації описів для відео
"""

from pathlib import Path
from tiktok_bot import TikTokUploader

def test_description_generation():
    """Протестувати генерацію описів"""
    print("🧪 Тестування генерації описів...")
    
    uploader = TikTokUploader()
    
    # Тестові назви файлів
    test_files = [
        "Ginny & Georgia. S03 E01. (This Wouldn't Even Be a Podcast)_clip_001.mp4",
        "Ginny & Georgia. S03 E02. (Beep Beep Freaking Beep)_clip_002.mp4",
        "Breaking Bad. S01 E01. (Pilot)_clip_001.mp4",
        "test_video_clip_001.mp4"
    ]
    
    for filename in test_files:
        video_path = Path(filename)
        description = uploader.generate_description(video_path)
        
        print(f"\n📁 Файл: {filename}")
        print(f"📝 Опис:")
        print(description)
        print("-" * 50)

if __name__ == "__main__":
    test_description_generation()

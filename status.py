#!/usr/bin/env python3
"""
Швидка перевірка статусу TikTok бота
"""

import json
from pathlib import Path
from datetime import datetime

def check_bot_status():
    """Перевірити поточний статус бота"""
    print("📊 Статус TikTok Бота")
    print("=" * 40)
    
    # Перевірити розклад
    try:
        with open('schedule.json', 'r') as f:
            schedule = json.load(f)
        
        print(f"📅 Розклад: {', '.join(schedule['posting_times'])}")
        print(f"📊 Кліпів у черзі: {len(schedule['queue'])}")
        
        if schedule['queue']:
            print("\n📹 Наступні кліпи:")
            for i, clip in enumerate(schedule['queue'][:3], 1):
                clip_name = Path(clip).name
                exists = "✅" if Path(clip).exists() else "❌"
                print(f"   {i}. {exists} {clip_name}")
        
        # Час наступної публікації
        now = datetime.now()
        posting_times = schedule['posting_times']
        next_time = None
        
        for time_str in posting_times:
            hour, minute = map(int, time_str.split(':'))
            upload_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if upload_time > now:
                next_time = upload_time
                break
        
        if next_time:
            print(f"\n⏰ Наступна публікація: {next_time.strftime('%H:%M')}")
        else:
            print(f"\n⏰ Наступна публікація: завтра о {posting_times[0]}")
            
    except FileNotFoundError:
        print("❌ Файл schedule.json не знайдено")
    
    # Перевірити кліпи
    clips_dir = Path('clips')
    if clips_dir.exists():
        clips = list(clips_dir.glob('*.mp4'))
        print(f"\n🎬 Всього кліпів у папці: {len(clips)}")
    else:
        print("\n❌ Папка clips не знайдена")
    
    # Перевірити API
    try:
        from tiktok_api import TikTokAPIClient
        api = TikTokAPIClient()
        if api.is_authenticated():
            print("✅ TikTok API авторизований")
        else:
            print("❌ TikTok API не авторизований")
    except Exception as e:
        print(f"❌ Помилка API: {e}")

if __name__ == "__main__":
    check_bot_status()

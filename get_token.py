#!/usr/bin/env python3
"""
Простий скрипт для обміну коду на токени
"""

import os
import sys
from dotenv import load_dotenv
from tiktok_api import TikTokAPIClient

def main():
    load_dotenv()
    
    if len(sys.argv) != 2:
        print("Usage: python get_token.py <authorization_code>")
        print("\n1. Відкрийте посилання:")
        print("https://www.tiktok.com/auth/authorize?client_key=awiw0on952z9r7ct&scope=video.upload&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%3A8080%2Fcallback%3Fstate%3Dunique_state_string&state=unique_state_string")
        print("\n2. Авторизуйтесь і скопіюйте код з URL")
        print("\n3. Запустіть: python get_token.py ВАШ_КОД")
        return
    
    code = sys.argv[1]
    
    try:
        client = TikTokAPIClient()
        success = client.exchange_code_for_token(code)
        
        if success:
            print("✅ Токени успішно отримано!")
            print("🎉 TikTok API готовий до роботи!")
        else:
            print("❌ Помилка отримання токенів")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    main()

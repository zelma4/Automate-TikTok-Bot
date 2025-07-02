#!/usr/bin/env python3
"""
Скрипт для налаштування TikTok API
Допомагає отримати токени доступу для роботи з TikTok Content Posting API
"""

import os
import sys
from dotenv import load_dotenv
from tiktok_api import TikTokAPIClient


def setup_tiktok_api():
    """Налаштувати TikTok API"""
    print("🔧 Налаштування TikTok API")
    print("=" * 50)
    
    # Завантажити змінні середовища
    load_dotenv()
    
    # Перевірити наявність CLIENT_ID та CLIENT_SECRET
    client_id = os.getenv('TIKTOK_CLIENT_ID')
    client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Не знайдено TIKTOK_CLIENT_ID або TIKTOK_CLIENT_SECRET")
        print("\n📝 Для роботи з TikTok API потрібно:")
        print("1. Зареєструвати додаток на https://developers.tiktok.com/")
        print("2. Додати у .env файл:")
        print("   TIKTOK_CLIENT_ID=your_client_id")
        print("   TIKTOK_CLIENT_SECRET=your_client_secret")
        return False
    
    try:
        # Створити API клієнт
        api_client = TikTokAPIClient()
        
        # Перевірити чи є збережені токени
        if api_client.is_authenticated():
            print("✅ Токени доступу вже налаштовані!")
            return True
        
        # Отримати URL для авторизації
        auth_url = api_client.get_authorization_url()
        
        print("\n🔐 Для отримання токенів доступу:")
        print("1. Відкрийте у браузері:")
        print(f"   {auth_url}")
        print("\n2. Авторизуйтесь і скопіюйте код з URL callback")
        print("   (параметр 'code' з URL)")
        
        # Отримати код від користувача
        code = input("\n📋 Введіть код авторизації: ").strip()
        
        if not code:
            print("❌ Код не введено")
            return False
        
        # Обміняти код на токени
        print("\n🔄 Обмін коду на токени...")
        success = api_client.exchange_code_for_token(code)
        
        if success:
            print("✅ Токени успішно отримано та збережено!")
            print("🎉 TikTok API готовий до роботи!")
            return True
        else:
            print("❌ Помилка отримання токенів")
            return False
            
    except Exception as e:
        print(f"❌ Помилка налаштування API: {e}")
        return False


def test_api():
    """Протестувати API"""
    print("\n🧪 Тестування TikTok API...")
    
    try:
        api_client = TikTokAPIClient()
        
        if not api_client.is_authenticated():
            print("❌ API не авторизований")
            return False
        
        print("✅ API авторизований")
        print("🎬 Готовий до завантаження відео!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка тестування API: {e}")
        return False


if __name__ == "__main__":
    print("🚀 TikTok API Setup")
    
    # Налаштування API
    setup_success = setup_tiktok_api()
    
    if setup_success:
        # Тестування API
        test_api()
    else:
        print("\n💡 Інструкції для налаштування:")
        print("1. Перейдіть на https://developers.tiktok.com/")
        print("2. Створіть новий додаток")
        print("3. Отримайте Client Key та Client Secret")
        print("4. Додайте їх у .env файл")
        sys.exit(1)

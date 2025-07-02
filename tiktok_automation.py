#!/usr/bin/env python3
"""
Модуль для автоматизації завантаження відео у TikTok через браузер
"""

import json
import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class TikTokAutomation:
    """Клас для автоматизації TikTok через браузер"""
    
    def __init__(self, config_file: str = "tiktok_config.json"):
        # Завантажити змінні середовища
        load_dotenv()
        
        self.config = self.load_config(config_file)
        self.driver = None
        self.is_logged_in = False
        
        # Отримати креди з .env файлу або конфігу
        self.username = os.getenv('TIKTOK_USERNAME') or self.config.get('username')
        self.password = os.getenv('TIKTOK_PASSWORD') or self.config.get('password')
        
    def load_config(self, config_file: str) -> dict:
        """Завантажити конфігурацію"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def setup_driver(self, headless: bool = False):
        """Налаштувати веб-драйвер"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
            
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Додати user agent для імітації реального користувача
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Виконати JavaScript для приховування автоматизації
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
    def login(self) -> bool:
        """Увійти у TikTok"""
        try:
            logger.info("Спроба входу у TikTok...")
            
            self.driver.get("https://www.tiktok.com/login")
            time.sleep(3)
            
            # Спробувати завантажити збережену сесію
            session_file = self.config.get("session_file", "tiktok_session.json")
            if Path(session_file).exists():
                if self.load_session(session_file):
                    return True
            
            # Якщо сесія не працює, потрібен ручний вхід
            logger.info("Необхідно увійти вручну...")
            logger.info("1. Відкрийте браузер та увійдіть у TikTok")
            logger.info("2. Після входу натисніть Enter у консолі")
            
            input("Натисніть Enter після входу у TikTok...")
            
            # Перевірити чи вдалося увійти
            if self.check_login_status():
                self.save_session(session_file)
                self.is_logged_in = True
                return True
            else:
                logger.error("Не вдалося увійти у TikTok")
                return False
                
        except Exception as e:
            logger.error(f"Помилка при вході: {e}")
            return False
    
    def load_session(self, session_file: str) -> bool:
        """Завантажити збережену сесію"""
        try:
            with open(session_file, 'r') as f:
                cookies = json.load(f)
                
            self.driver.get("https://www.tiktok.com")
            time.sleep(2)
            
            for cookie in cookies:
                self.driver.add_cookie(cookie)
                
            self.driver.refresh()
            time.sleep(3)
            
            return self.check_login_status()
            
        except Exception as e:
            logger.warning(f"Не вдалося завантажити сесію: {e}")
            return False
    
    def save_session(self, session_file: str):
        """Зберегти поточну сесію"""
        try:
            cookies = self.driver.get_cookies()
            with open(session_file, 'w') as f:
                json.dump(cookies, f)
            logger.info("Сесію збережено")
        except Exception as e:
            logger.error(f"Помилка при збереженні сесії: {e}")
    
    def check_login_status(self) -> bool:
        """Перевірити статус входу"""
        try:
            # Шукати елементи, які вказують на успішний вхід
            WebDriverWait(self.driver, 10).until(
                lambda d: "login" not in d.current_url.lower()
            )
            
            # Перевірити наявність кнопки завантаження
            upload_button = self.driver.find_elements(
                By.XPATH, "//a[@href='/upload' or contains(@href, 'upload')]"
            )
            
            return len(upload_button) > 0
            
        except Exception:
            return False
    
    async def upload_video(self, video_path: Path, description: str = "") -> bool:
        """
        Завантажити відео у TikTok
        
        Args:
            video_path: Шлях до відеофайлу
            description: Опис відео
            
        Returns:
            True якщо завантаження успішне
        """
        try:
            if not self.is_logged_in:
                logger.error("Потрібно спочатку увійти у TikTok")
                return False
                
            logger.info(f"Завантажуємо відео: {video_path.name}")
            
            # Перейти на сторінку завантаження
            self.driver.get("https://www.tiktok.com/upload")
            time.sleep(3)
            
            # Знайти поле для завантаження файлу
            file_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            # Завантажити файл
            file_input.send_keys(str(video_path.absolute()))
            logger.info("Файл завантажено, очікуємо обробку...")
            
            # Очікати завершення обробки відео
            time.sleep(30)
            
            # Додати опис
            if description:
                try:
                    description_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR, 
                            "div[data-text='true'] div[contenteditable='true']"
                        ))
                    )
                    description_input.clear()
                    description_input.send_keys(description)
                    logger.info("Опис додано")
                except Exception as e:
                    logger.warning(f"Не вдалося додати опис: {e}")
            
            # Знайти та натиснути кнопку публікації
            publish_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//button[contains(text(), 'Post') or contains(text(), 'Опублікувати')]"
                ))
            )
            
            publish_button.click()
            logger.info("Кнопку публікації натиснуто")
            
            # Очікати підтвердження
            time.sleep(10)
            
            # Перевірити успішність публікації
            success_indicators = self.driver.find_elements(
                By.XPATH, 
                "//*[contains(text(), 'success') or contains(text(), 'posted') or "
                "contains(text(), 'uploaded') or contains(text(), 'опубліковано')]"
            )
            
            if success_indicators:
                logger.info(f"Відео {video_path.name} успішно опубліковано!")
                return True
            else:
                logger.warning("Не вдалося підтвердити успішну публікацію")
                return False
                
        except Exception as e:
            logger.error(f"Помилка при завантаженні відео: {e}")
            return False
    
    def close(self):
        """Закрити браузер"""
        if self.driver:
            self.driver.quit()
            logger.info("Браузер закрито")

#!/usr/bin/env python3
"""
TikTok API клієнт для завантаження відео
Використовує офіційний TikTok Content Posting API
"""

import os
import json
import requests
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class TikTokAPIClient:
    """Клієнт для роботи з TikTok Content Posting API"""

    def __init__(self):
        """Ініціалізація API клієнта"""
        self.base_url = "https://open.tiktokapis.com"
        self.client_id = os.getenv('TIKTOK_CLIENT_ID')
        self.client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
        self.access_token = None
        self.refresh_token = None

        # Завантажити збережені токени
        self._load_tokens()

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Не знайдено TIKTOK_CLIENT_ID або TIKTOK_CLIENT_SECRET "
                "у .env файлі"
            )

    def _load_tokens(self):
        """Завантажити збережені токени з файлу"""
        try:
            with open('tiktok_tokens.json', 'r') as f:
                tokens = json.load(f)
                self.access_token = tokens.get('access_token')
                self.refresh_token = tokens.get('refresh_token')
        except FileNotFoundError:
            logger.info("Файл токенів не знайдено, потрібна авторизація")

    def _save_tokens(self, access_token: str, refresh_token: str):
        """Зберегти токени у файл"""
        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'updated_at': datetime.now().isoformat()
        }
        with open('tiktok_tokens.json', 'w') as f:
            json.dump(tokens, f, indent=2)

        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_authorization_url(self) -> str:
        """Отримати URL для авторизації користувача"""
        params = {
            'client_key': self.client_id,
            'scope': 'video.upload',
            'response_type': 'code',
            'redirect_uri': 'https://localhost:8080/callback',
            'state': 'unique_state_string'
        }

        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"https://www.tiktok.com/auth/authorize/?{query_string}"

    def exchange_code_for_token(self, code: str) -> bool:
        """Обміняти код авторизації на токени доступу"""
        url = f"{self.base_url}/v2/oauth/token/"

        data = {
            'client_key': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://localhost:8080/callback'
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()

            result = response.json()
            if 'access_token' in result:
                self._save_tokens(
                    result['access_token'],
                    result['refresh_token']
                )
                logger.info("Токени успішно отримано та збережено")
                return True
            else:
                logger.error(f"Помилка отримання токенів: {result}")
                return False

        except requests.RequestException as e:
            logger.error(f"Помилка запиту токенів: {e}")
            return False

    def refresh_access_token(self) -> bool:
        """Оновити токен доступу"""
        if not self.refresh_token:
            logger.error("Немає refresh_token для оновлення")
            return False

        url = f"{self.base_url}/v2/oauth/token/"

        data = {
            'client_key': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()

            result = response.json()
            if 'access_token' in result:
                self._save_tokens(
                    result['access_token'],
                    result['refresh_token']
                )
                logger.info("Токен успішно оновлено")
                return True
            else:
                logger.error(f"Помилка оновлення токену: {result}")
                return False

        except requests.RequestException as e:
            logger.error(f"Помилка оновлення токену: {e}")
            return False

    def upload_video(self, video_path: str, title: str = "",
                     description: str = "",
                     privacy_level: str = "SELF_ONLY") -> Optional[Dict]:
        """
        Завантажити відео на TikTok

        Args:
            video_path: Шлях до відео файлу
            title: Заголовок відео
            description: Опис відео
            privacy_level: Рівень приватності (PUBLIC_TO_EVERYONE,
                          SELF_ONLY, MUTUAL_FOLLOW_FRIENDS)

        Returns:
            Результат завантаження або None при помилці
        """
        if not self.access_token:
            logger.error("Немає токену доступу. Потрібна авторизація.")
            return None

        if not os.path.exists(video_path):
            logger.error(f"Відео файл не знайдено: {video_path}")
            return None

        # Крок 1: Ініціалізація завантаження
        init_result = self._initialize_upload()
        if not init_result:
            return None

        upload_url = init_result['upload_url']
        publish_id = init_result['publish_id']

        # Крок 2: Завантаження файлу
        upload_result = self._upload_file(upload_url, video_path)
        if not upload_result:
            return None

        # Крок 3: Публікація відео
        publish_result = self._publish_video(
            publish_id, title, description, privacy_level
        )

        return publish_result

    def _initialize_upload(self) -> Optional[Dict[str, Any]]:
        """Ініціалізувати процес завантаження"""
        url = f"{self.base_url}/v2/post/publish/video/init/"

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'post_info': {
                'title': '',
                'privacy_level': 'SELF_ONLY',
                'disable_duet': False,
                'disable_comment': False,
                'disable_stitch': False,
                'video_cover_timestamp_ms': 1000
            },
            'source_info': {
                'source': 'FILE_UPLOAD',
                'video_size': 0,
                'chunk_size': 0,
                'total_chunk_count': 1
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            if result.get('data'):
                return result['data']
            else:
                logger.error(f"Помилка ініціалізації завантаження: {result}")
                return None

        except requests.RequestException as e:
            logger.error(f"Помилка ініціалізації завантаження: {e}")
            # Можливо, токен застарів
            if hasattr(e, 'response') and e.response.status_code == 401:
                logger.info("Спроба оновити токен...")
                if self.refresh_access_token():
                    return self._initialize_upload()  # Повторна спроба
            return None

    def _upload_file(self, upload_url: str, video_path: str) -> bool:
        """Завантажити файл на TikTok"""
        try:
            with open(video_path, 'rb') as video_file:
                files = {'video': video_file}
                response = requests.put(upload_url, files=files)
                response.raise_for_status()

                logger.info(f"Файл успішно завантажено: {video_path}")
                return True

        except requests.RequestException as e:
            logger.error(f"Помилка завантаження файлу: {e}")
            return False

    def _publish_video(self, publish_id: str, title: str, description: str,
                       privacy_level: str) -> Optional[Dict[str, Any]]:
        """Опублікувати відео"""
        url = f"{self.base_url}/v2/post/publish/status/fetch/"

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'publish_id': publish_id
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            logger.info(f"Відео опубліковано: {result}")
            return result

        except requests.RequestException as e:
            logger.error(f"Помилка публікації відео: {e}")
            return None

    def is_authenticated(self) -> bool:
        """Перевірити чи є валідний токен доступу"""
        return self.access_token is not None

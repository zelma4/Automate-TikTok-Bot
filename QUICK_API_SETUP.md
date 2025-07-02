# 🔧 Налаштування TikTok API - Швидкий Гід

## Крок 1: Заповніть форму TikTok
Використайте ці URLs для заповнення форми реєстрації додатку:

- **Terms of Service URL**: `https://example.com/terms`
- **Privacy Policy URL**: `https://example.com/privacy`  
- **Web/Desktop URL**: `https://example.com`

*Примітка: Ці placeholder URLs працюють для початкового налаштування*

## Крок 2: Отримайте креди
Після схвалення додатку:
1. Скопіюйте **Client Key** 
2. Скопіюйте **Client Secret**

## Крок 3: Додайте у .env
```bash
TIKTOK_CLIENT_ID=ваш_client_key_тут
TIKTOK_CLIENT_SECRET=ваш_client_secret_тут
```

## Крок 4: Авторизація
```bash
python setup_tiktok_api.py
```

## Крок 5: Тестування
```bash
python status.py
python run_bot.py post
```

---

## 📚 Додаткові інструкції

Якщо потрібні справжні URLs:
1. У папці `docs/` є готові HTML файли
2. Завантажте їх на будь-який безкоштовний хостинг
3. Використайте справжні URLs у формі TikTok

## 🆘 Troubleshooting

**"API не авторизований"**
→ Запустіть `python setup_tiktok_api.py`

**"Не знайдено CLIENT_ID"**
→ Перевірте .env файл

**Додаток відхилено**
→ Перевірте інформацію про додаток у формі

---
*Після налаштування ваш бот працюватиме через офіційний TikTok API! 🚀*

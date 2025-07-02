# Міграція на TikTok API 🔄

Ваш бот тепер використовує офіційний TikTok Content Posting API замість автоматизації браузера.

## 🆕 Що змінилося

### Переваги нового API:
- ✅ **Надійність**: Офіційний API без блокувань
- ✅ **Швидкість**: Миттєве завантаження без браузера
- ✅ **Безпека**: Немає потреби зберігати пароль
- ✅ **Стабільність**: Немає проблем з UI змінами TikTok

### Що потрібно зробити:

1. **Зареєструвати додаток на TikTok**
   - Перейдіть на https://developers.tiktok.com/
   - Створіть новий додаток
   - Отримайте Client Key та Client Secret

2. **Оновити .env файл**
   ```bash
   TIKTOK_CLIENT_ID=ваш_client_id
   TIKTOK_CLIENT_SECRET=ваш_client_secret
   ```

3. **Авторизуватись через API**
   ```bash
   python setup_tiktok_api.py
   ```

4. **Видалити старі файли** (опціонально)
   - `tiktok_automation.py` - більше не потрібен
   - Chrome WebDriver - більше не потрібен

## 🔧 Налаштування

### Крок 1: Реєстрація додатку
1. Відкрийте https://developers.tiktok.com/
2. Увійдіть з вашим TikTok аккаунтом
3. Натисніть "Manage apps" → "Create an app"
4. Заповніть інформацію про додаток
5. У розділі "Products" додайте "Content Posting API"
6. Скопіюйте Client Key та Client Secret

### Крок 2: Налаштування бота
```bash
# Відредагуйте .env файл
nano .env

# Додайте креди API
TIKTOK_CLIENT_ID=ваш_client_id_тут
TIKTOK_CLIENT_SECRET=ваш_client_secret_тут

# Запустіть налаштування
python setup_tiktok_api.py
```

### Крок 3: Тестування
```bash
# Запустіть бота для перевірки
python run_bot.py run
```

## 🆘 Troubleshooting

**Проблема**: "Не знайдено TIKTOK_CLIENT_ID"
**Рішення**: Перевірте .env файл та додайте креди API

**Проблема**: "API не авторизований"
**Рішення**: Запустіть `python setup_tiktok_api.py` для авторизації

**Проблема**: "Помилка завантаження відео"
**Рішення**: Перевірте, чи додаток має права на Content Posting API

## 📚 Додаткова інформація

- [TikTok for Developers](https://developers.tiktok.com/)
- [Content Posting API Docs](https://developers.tiktok.com/doc/content-posting-api-quick-start/)
- [API Reference](https://developers.tiktok.com/doc/content-posting-api-reference-video-upload/)

---
*Ваш бот тепер працює швидше та надійніше! 🚀*

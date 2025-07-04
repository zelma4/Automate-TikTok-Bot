# TikTok Bot для Серіалів 🎬

Автоматичний бот для нарізки серіалів на 1-хвилинні кліпи та завантаження у TikTok через офіційний API.

## 🚀 Швидкий старт

### 1. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 2. Встановлення FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

### 3. Початкове налаштування

```bash
python run_bot.py setup
```

### 4. Налаштування TikTok

Створіть файл `.env` та додайте ваші креди:
```
TIKTOK_USERNAME=ваш_username
TIKTOK_PASSWORD=ваш_пароль
```

### 5. Запуск

```bash
# Нарізати відео на кліпи
python run_bot.py process

# Запустити бота за розкладом
python run_bot.py run

# Опублікувати наступне відео з черги зараз
python run_bot.py post

# Опублікувати конкретний файл
python run_bot.py upload --file clips/video.mp4
```

## 🚀 Нові можливості

### Команди постингу:
- **`post`** - Миттєво опублікувати наступне відео з черги
- **`upload --file`** - Опублікувати конкретний відео файл

### Автоматичні описи:
- 🎬 Назва серіалу (з назви файлу)
- 📺 Сезон та епізод (S03 E01)  
- 🎞️ Номер частини кліпу
- 📝 Випадковий опис + хештеги

### Приклад згенерованого опису:
```
🎬 Ginny & Georgia | 📺 S03 E01 | 🎞️ частина 001 | Найкращі моменти з серіалу! 🔥

#серіал #гінніджорджія #netflix #відео
```

## 📁 Структура проекту

```
├── Serial/                 # Папка з серіалами (.mkv файли)
├── clips/                  # Згенеровані кліпи
├── logs/                   # Логи роботи
├── .env                    # TikTok креди (створити вручну)
├── tiktok_config.json     # Конфігурація бота
├── schedule.json          # Розклад публікацій
├── tiktok_bot.py         # Основний бот
├── tiktok_automation.py   # Автоматизація TikTok
└── run_bot.py            # Інтерфейс управління
```

## ⚙️ Конфігурація

### Налаштування відео
- **Розмір:** 1080x1920 (TikTok формат 9:16)
- **FPS:** 30
- **Тривалість кліпу:** 60 секунд
- **Формат:** MP4 з H.264

### Розклад публікацій
- **За замовчуванням:** 3 пости на день
- **Час:** 09:00, 15:00, 21:00
- **Налаштовується** через `schedule.json`

## 🛡️ Безпека

- Використовуйте окремий TikTok акаунт для бота
- Тримайте `.env` файл у безпеці
- Дотримуйтесь авторських прав на контент
- Не перевищуйте ліміти TikTok

## 📊 Команди

```bash
python run_bot.py setup     # Початкове налаштування
python run_bot.py process   # Нарізати відео
python run_bot.py run       # Запустити бота
```

## 🔧 Налагодження

Перевірте логи у файлі `tiktok_bot.log` для деталей роботи.

---

**Увага:** Використовуйте відповідально та дотримуйтесь правил TikTok!

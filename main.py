import os
import random
import logging
import asyncio
from telethon import TelegramClient, events
import chardet

# ТОЛЬКО ТОКЕН БОТА - API ID/HASH НЕ НУЖНЫ!
BOT_TOKEN = "8728120679:AAESNATj8PvyD9wy7czAkGoxCfQFkkUHItk"

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем клиент бота (без API ID/HASH)
bot = TelegramClient("bot", api_id=0, api_hash="").start(bot_token=BOT_TOKEN)

# Глобальные переменные
troll_phrases = []

# Функция загрузки фраз из trolls.txt
def load_troll_phrases():
    global troll_phrases
    try:
        if os.path.exists('trolls.txt'):
            # Определяем кодировку файла
            with open('trolls.txt', 'rb') as f:
                raw_data = f.read()
                encoding_info = chardet.detect(raw_data)
                file_encoding = encoding_info['encoding'] if encoding_info['encoding'] else 'utf-8'
            
            # Читаем файл с правильной кодировкой
            with open('trolls.txt', 'r', encoding=file_encoding, errors='replace') as f:
                troll_phrases = [line.strip() for line in f.readlines() if line.strip()]
            
            logger.info(f"✅ Загружено {len(troll_phrases)} фраз из trolls.txt")
        else:
            logger.warning("⚠️ Файл trolls.txt не найден")
            troll_phrases = []
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки trolls.txt: {e}")
        troll_phrases = []

# Функция добавления новой фразы
def add_troll_phrase(phrase):
    try:
        with open('trolls.txt', 'a', encoding='utf-8') as f:
            f.write(f"{phrase}\n")
        troll_phrases.append(phrase)
        return True
    except Exception as e:
        logger.error(f"Ошибка добавления фразы: {e}")
        return False

# Обработчик команды /start
@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """Приветственное сообщение"""
    await event.reply(
        "✅ **Бот работает!**\n\n"
        "📋 **Доступные команды:**\n"
        "/start - Показать это сообщение\n"
        "/troll - Получить случайную фразу\n"
        "/addtroll [текст] - Добавить новую фразу\n"
        "/help - Помощь\n\n"
        "🤖 Бот готов к работе в Business Mode!"
    )

# Обработчик команды /help
@bot.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    """Помощь по командам"""
    await event.reply(
        "📖 **Помощь по командам:**\n\n"
        "🔹 `/start` - Запуск бота и информация\n"
        "🔹 `/troll` - Получить случайную фразу из базы\n"
        "🔹 `/addtroll [текст]` - Добавить новую фразу\n"
        "🔹 `/help` - Показать эту справку\n\n"
        f"📊 **Статистика:** {len(troll_phrases)} фраз в базе"
    )

# Обработчик команды /troll
@bot.on(events.NewMessage(pattern='/troll'))
async def troll_handler(event):
    """Отправляет случайную фразу из trolls.txt"""
    if troll_phrases:
        phrase = random.choice(troll_phrases)
        await event.reply(f"🎭 **Тролль говорит:**\n\n{phrase}")
    else:
        await event.reply(
            "❌ **Нет загруженных фраз!**\n\n"
            "Добавьте фразы в файл `trolls.txt` или используйте команду:\n"
            "`/addtroll [текст фразы]`"
        )

# Обработчик команды /addtroll
@bot.on(events.NewMessage(pattern='/addtroll'))
async def add_troll_handler(event):
    """Добавляет новую фразу в trolls.txt"""
    # Получаем текст после команды
    text = event.raw_text.replace('/addtroll', '').strip()
    
    if not text:
        await event.reply(
            "❌ **Ошибка:** Не указан текст фразы!\n\n"
            "**Использование:** `/addtroll [ваша фраза]`\n\n"
            "**Пример:** `/addtroll ты лох ебаный`"
        )
        return
    
    # Добавляем фразу
    if add_troll_phrase(text):
        await event.reply(
            f"✅ **Фраза успешно добавлена!**\n\n"
            f"📝 Текст: `{text}`\n"
            f"📊 Всего фраз: {len(troll_phrases)}"
        )
    else:
        await event.reply("❌ **Ошибка:** Не удалось добавить фразу. Проверьте права на запись.")

# Обработчик команды /stats
@bot.on(events.NewMessage(pattern='/stats'))
async def stats_handler(event):
    """Показывает статистику"""
    await event.reply(
        "📊 **Статистика бота:**\n\n"
        f"📝 Фраз в базе: **{len(troll_phrases)}**\n"
        f"🤖 Статус: **Работает**\n"
        f"💾 Файл: `trolls.txt`"
    )

# Загрузка фраз при старте
load_troll_phrases()

# Запуск бота
async def main():
    logger.info("🚀 Бот запускается...")
    logger.info(f"📊 Загружено фраз: {len(troll_phrases)}")
    logger.info("✅ Бот готов к работе!")
    
    # Выводим информацию о боте
    me = await bot.get_me()
    logger.info(f"🤖 Имя бота: {me.first_name}")
    logger.info(f"🔑 Username: @{me.username}")
    
    await bot.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")

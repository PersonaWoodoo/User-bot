from telethon import events
from utils import add_compliment

async def addtroll_command(event, compliments):
    try:
        _, compliment = event.raw_text.split(" ", 1)
        add_compliment(compliment)
        await event.reply(f"✅ Комплимент добавлен: {compliment}")
    except Exception as e:
        await event.reply(f"🚫 Ошибка: {str(e)}")

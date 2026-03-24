from telethon import events

async def clear_command(event, troll_users):
    troll_users.clear()
    await event.reply("✅ Список пользователей для троллинга очищен!", parse_mode='HTML')

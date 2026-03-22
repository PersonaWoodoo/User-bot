from telethon import events
import random

async def troll_command(event, troll_users):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.sender_id == event.sender_id:
            await event.reply("❌ Нельзя троллить самого себя! 😡", parse_mode='HTML')
        else:
            troll_users.add(reply.sender_id)
            await event.reply(f"✅ Теперь я буду отправлять комплименты пользователю {reply.sender_id}!", parse_mode='HTML')
    else:
        await event.reply("❌ Ответьте на сообщение командой .troll.", parse_mode='HTML')

async def troll_handler(event, troll_users, compliments):
    if event.sender_id in troll_users and compliments:
        compliment = random.choice(compliments)
        await event.reply(compliment)

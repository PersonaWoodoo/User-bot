from telethon import events
import g4f

async def gpt_command(event):
    prompt = event.raw_text.replace(".gpt", "").strip()
    processing_msg = await event.reply('⏳ Генерация текста...', parse_mode='HTML')
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        await event.reply(f"🤖 Ответ GPT-4:\n{response}", parse_mode='HTML')
    except Exception as e:
        await event.reply(f"🚫 Ошибка: {str(e)}", parse_mode='HTML')
    finally:
        await processing_msg.delete()

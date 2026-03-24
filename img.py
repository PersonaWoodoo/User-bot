from telethon import events
import requests
from io import BytesIO

async def img_command(client, event):
    prompt = event.raw_text.replace(".img", "").strip()
    processing_msg = await event.reply('⏳ Генерация изображения...', parse_mode='HTML')
    try:
        response = requests.get(f"https://image.pollinations.ai/prompt/{prompt}")
        response.raise_for_status()
        image_data = BytesIO(response.content)
        image_data.name = 'image.png'
        await client.send_file(
            event.chat_id,
            image_data,
            reply_to=event.id
        )
    except requests.exceptions.RequestException as e:
        await event.reply(f"🚫 Ошибка при запросе: {str(e)}", parse_mode='HTML')
    except Exception as e:
        await event.reply(f"🚫 Общая ошибка: {str(e)}", parse_mode='HTML')
    finally:
        await processing_msg.delete()

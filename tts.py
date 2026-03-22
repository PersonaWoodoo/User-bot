from telethon import types
from gtts import gTTS
from io import BytesIO

async def tts_command(client, event):
    try:
        text = event.raw_text.replace(".tts", "").strip()
        if not text:
            await event.reply("❌ Используйте: .tts [текст]")
            return

        tts = gTTS(text, lang="ru")
        voice_bytes = BytesIO()
        tts.write_to_fp(voice_bytes)
        voice_bytes.seek(0)

        with open("unnamed.ogg", "wb") as f:
            f.write(voice_bytes.getvalue())

        await client.send_file(
            event.chat_id,
            "unnamed.ogg",
            voice_note=True,
            attributes=[
                types.DocumentAttributeAudio(
                    voice=True,
                    duration=len(text) // 10
                )
            ]
        )
    except Exception as e:
        await event.reply(f"🚫 Ошибка: {str(e)}")

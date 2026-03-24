from telethon import events

async def emailadd_command(event):
    try:
        input_text = event.raw_text.replace(".emailadd", "").strip()
        if not input_text:
            await event.reply("❌ Используйте: .emailadd \"почта\" \"пароль\"")
            return

        if input_text.count('"') != 4:
            await event.reply("❌ Неверный формат. Используйте: .emailadd \"почта\" \"пароль\"")
            return

        parts = [part.strip('"') for part in input_text.split('"') if part.strip()]
        if len(parts) != 2:
            await event.reply("❌ Неверный формат. Используйте: .emailadd \"почта\" \"пароль\"")
            return

        email, password = parts

        with open("emails.txt", "a", encoding="utf-8") as file:
            file.write(f'"{email}" "{password}"\n')

        await event.reply(f"✅ Почта добавлена: {email}")
    except Exception as e:
        await event.reply(f"🚫 Ошибка: {str(e)}")

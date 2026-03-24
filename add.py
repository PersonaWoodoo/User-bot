from telethon import events
from utils import save_words, check_empty

async def add_command(event, slova):
    try:
        command, value = event.raw_text.replace(".add", "").strip().split(" ", 1)
        key_mapping = {
            "number": "numbers",
            "country": "countries",
            "region": "regions",
            "oper": "operators",
            "names": "names",
            "adres": "addresses",
            "birth": "birth_dates",
            "goodrep": "good_reps",
            "badrep": "bad_reps",
            "interest": "interests",
            "social": "social_marks",
            "comment": "comments_counts"
        }
        if command in key_mapping:
            key = key_mapping[command]
            if command == "social":
                parts = value.split()
                if len(parts) > 1 and parts[-1].isdigit():
                    social_text = " ".join(parts[:-1])
                    social_number = parts[-1]
                    value = f"{social_text} ({social_number})"
                slova[key].append(value)
            elif command in ["names", "adres"]:
                values = value.split()
                slova[key].extend(values)
            else:
                slova[key].append(value)
            save_words(slova)
            await event.reply(f"✅ {value} добавлено в {key}.", parse_mode='HTML')
        else:
            await event.reply("❌ Неизвестный ключ. Используйте: .add [ключ] [значение]", parse_mode='HTML')
    except Exception as e:
        await event.reply(f"🚫 Ошибка: {str(e)}", parse_mode='HTML')

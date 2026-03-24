from telethon import events
import asyncio
import random
from utils import check_empty

async def dox_command(event, slova):
    stages = [
        "⛓ Начинаю докс...",
        "☠️ Запрос принят, получаю информацию...",
        "🚫 Поиск данных...",
        "🔄 Сверяю с базами данных...",
        "✅ Информация найдена",
        "🔁 Вывожу..."
    ]

    message_status = await event.edit(random.choice(stages), parse_mode='HTML')
    for stage in stages:
        await asyncio.sleep(1.5)
        await message_status.edit(stage, parse_mode='HTML')

    result_message = (
        f"📱\n├ Номер: {check_empty(slova['numbers'])}\n"
        f"├ Страна: {check_empty(slova['countries'])}\n"
        f"├ Регион: {check_empty(slova['regions'])}\n"
        f"└ Оператор: {check_empty(slova['operators'])}\n\n"
        f"📓 Имя: {check_empty(slova['names'])}\n"
        f"🏠 Адрес: {check_empty(slova['addresses'])}\n"
        f"🏥 Дата рождения: {check_empty(slova['birth_dates'])}\n\n"
        f"👁 Интересовались: {check_empty(slova['interests'])} человек.\n"
        f"🏅 Репутация: {check_empty(slova['good_reps'])}👍 {check_empty(slova['bad_reps'])}👎\n\n"
        f"💬 Социальная метка: {check_empty(slova['social_marks'])}\n"
        f"👁 Комментариев: {check_empty(slova['comments_counts'])}"
    )
    await message_status.edit(result_message, parse_mode='HTML')

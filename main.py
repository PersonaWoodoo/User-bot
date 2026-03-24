from telethon import TelegramClient, events
import asyncio
import time
import random
import os
from troll import troll_command, troll_handler
from dox import dox_command
from add import add_command
from gpt import gpt_command
from img import img_command
from addtroll import addtroll_command
from menu import MENU
from tts import tts_command
from anon import anon_command
from clear import clear_command
from emailadd import emailadd_command
from utils import load_words, load_compliments, save_words, check_empty

slova = load_words()
compliments = load_compliments()
troll_users = set()

async def main():
    global start_time
    start_time = time.time()
    phone_number = input("Введите номер телефона: ")
    api_id = int(input("Введите API ID: "))
    api_hash = input("Введите API Hash: ")
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone=phone_number)
    me = await client.get_me()
    print(f"Userbot запущен на аккаунте: {me.username}")

    @client.on(events.NewMessage)
    async def handler(event):
        global slova, troll_users
        if event.sender_id != me.id:
            return

        if event.raw_text == ".dox":
            await dox_command(event, slova)
        elif event.raw_text.startswith(".add"):
            await add_command(event, slova)
        elif event.raw_text.startswith(".addtroll"):
            await addtroll_command(event, compliments)
        elif event.raw_text == ".troll":
            await troll_command(event, troll_users)
        elif event.raw_text.startswith(".gpt"):
            await gpt_command(event)
        elif event.raw_text.startswith(".img"):
            await img_command(client, event)
        elif event.raw_text == ".menu":
            await event.reply(MENU, parse_mode='HTML')
        elif event.raw_text.startswith(".tts"):
            await tts_command(client, event)
        elif event.raw_text.startswith(".anon"):
            await anon_command(event)
        elif event.raw_text == ".clear":
            await clear_command(event, troll_users)
        elif event.raw_text.startswith(".emailadd"):
            await emailadd_command(event)

    @client.on(events.NewMessage)
    async def troll_handler(event):
        if event.sender_id in troll_users and compliments:
            compliment = random.choice(compliments)
            await event.reply(compliment)

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

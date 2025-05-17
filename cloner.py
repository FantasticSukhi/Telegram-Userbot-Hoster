from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

SESSION_DIR = 'userbot_sessions'
os.makedirs(SESSION_DIR, exist_ok=True)

async def clone_userbot(api_id, api_hash, phone=None, session_string=None):
    if session_string:
        client = TelegramClient(StringSession(session_string), api_id, api_hash)
    else:
        session_path = os.path.join(SESSION_DIR, f'userbot_{phone}')
        client = TelegramClient(session_path, api_id, api_hash)
        await client.start(phone=phone)

    await client.send_message('me', '✅ Userbot session initialized!')
    return client

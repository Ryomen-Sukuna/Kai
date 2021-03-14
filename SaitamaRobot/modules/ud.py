import requests
from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from pyrogram import filters
from SaitamaRobot import kp
import aiohttp
import os


@kp.on_message(filters.command("ud"))
async def ud(c, m):
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                    f"https://api.urbandictionary.com/v0/define?term={m.text.split('/ud',1)[1]}"
            ) as response:
                resp = await response.json()
                try:
                    text = f"**Word : {resp['list'][0]['word']}**\n\n **Definitions**:\n"
                except IndexError:
                    await m.reply("__Word Not Found__")
                    return
                for x in resp['list']:
                    text += f"\n☞ {x['definition']}\n"
                await m.reply(text, quote=False)
    except Exception:
        with open('ud.txt', 'w+', encoding='utf8') as f:
            f.write(str(text))
        await m.reply_document('ud.txt')
        os.remove('ud.txt')

        
UD_HANDLER = DisableAbleCommandHandler(["ud"], ud)

dispatcher.add_handler(UD_HANDLER)

__command_list__ = ["ud"]
__handlers__ = [UD_HANDLER]

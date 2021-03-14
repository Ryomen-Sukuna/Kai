import requests
from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async
from pyrogram import filters
from SaitamaRobot import app
import aiohttp
import os


def ud(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len("/ud ") :]
    results = requests.get(
        f"https://api.urbandictionary.com/v0/define?term={text}"
    ).json()
    @app.on_message(filters.command("ud"))
async def ud(c, m):
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except:
        reply_text = "No results found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
    
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

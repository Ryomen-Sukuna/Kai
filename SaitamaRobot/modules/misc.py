import html
import time
import git
import os
import re
import codecs
import datetime
import platform
from typing import List
from random import randint

from SaitamaRobot.modules.helper_funcs.chat_status import user_admin
from SaitamaRobot import dispatcher, WALL_API, SUPPORT_CHAT
import requests
import wikipedia
from requests import get, post
from telegram import (
    Chat,
    ChatAction,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Message,
    MessageEntity,
    TelegramError,
    __version__ as ptbver,
)
from SaitamaRobot.__main__ import STATS, USER_INFO, TOKEN
from SaitamaRobot.modules.sql import SESSION
from telegram.error import BadRequest
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from telegram.ext import CallbackContext, Filters
from SaitamaRobot import StartTime
from SaitamaRobot.modules.helper_funcs.chat_status import sudo_plus
from SaitamaRobot.modules.helper_funcs.alternate import send_action, typing_action
from SaitamaRobot.modules.helper_funcs.decorators import kaicmd, kaicallback

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

• <code>_italic_</code>: wrapping text with '_' will produce italic text
• <code>*bold*</code>: wrapping text with '*' will produce bold text
• <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
• <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
<b>Example:</b><code>[test](example.com)</code>

• <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
<b>Example:</b> <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@kaicmd(command='echo', pass_args=True, filters=Filters.chat_type.groups)
@user_admin
def echo(update: Update, _):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(
            args[1], parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    else:
        message.reply_text(
            args[1], quote=False, parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    message.delete()


def markdown_help_sender(update: Update, _):
    update.effective_message.reply_text(MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see, and Use #test!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, code, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )


@kaicmd(command="markdownhelp")
def markdown_help(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        update.effective_message.reply_text(
            "Contact me in pm",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Markdown help",
                            url=f"t.me/{context.bot.username}?start=markdownhelp",
                        )
                    ]
                ]
            ),
        )
        return
    markdown_help_sender(update)


@kigcmd(command="wiki")
def wiki(update: Update, context: CallbackContext):
    kueri = re.split(pattern="wiki", string=update.effective_message.text)
    wikipedia.set_lang("en")
    if len(str(kueri[1])) == 0:
        update.effective_message.reply_text("Enter keywords!")
    else:
        try:
            pertama = update.effective_message.reply_text("🔄 Loading...")
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔧 More Info...",
                            url=wikipedia.page(kueri).url,
                        )
                    ]
                ]
            )
            context.bot.editMessageText(
                chat_id=update.effective_chat.id,
                message_id=pertama.message_id,
                text=wikipedia.summary(kueri, sentences=10),
                reply_markup=keyboard,
            )
        except wikipedia.PageError as e:
            update.effective_message.reply_text(f"⚠ Error: {e}")
        except BadRequest as et:
            update.effective_message.reply_text(f"⚠ Error: {et}")
        except wikipedia.exceptions.DisambiguationError as eet:
            update.effective_message.reply_text(
                f"⚠ Error\n There are too many query! Express it more!\nPossible query result:\n{eet}"
            )


@send_action(ChatAction.UPLOAD_PHOTO)
@kaicmd(command="wall")
def wall(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    args = context.args
    msg_id = update.effective_message.message_id
    bot = context.bot
    query = " ".join(args)
    if not query:
        msg.reply_text("Please enter a query!")
        return
    else:
        caption = query
        term = query.replace(" ", "%20")
        json_rep = requests.get(
            f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}"
        ).json()
        if not json_rep.get("success"):
            msg.reply_text(f"An error occurred! Report this @{SUPPORT_CHAT}")
        else:
            wallpapers = json_rep.get("wallpapers")
            if not wallpapers:
                msg.reply_text("No results found! Refine your search.")
                return
            else:
                index = randint(0, len(wallpapers) - 1)  # Choose random index
                wallpaper = wallpapers[index]
                wallpaper = wallpaper.get("url_image")
                wallpaper = wallpaper.replace("\\", "")
                bot.send_photo(
                    chat_id,
                    photo=wallpaper,
                    caption="Preview",
                    reply_to_message_id=msg_id,
                    timeout=60,
                )
                bot.send_document(
                    chat_id,
                    document=wallpaper,
                    filename="wallpaper",
                    caption=caption,
                    reply_to_message_id=msg_id,
                    timeout=60,
                )


@kaicmd(command="paste")
@typing_action
def paste(update, context):
    msg = update.effective_message

    if msg.reply_to_message and msg.reply_to_message.document:
        file = context.bot.get_file(msg.reply_to_message.document)
        file.download("file.txt")
        text = codecs.open("file.txt", "r+", encoding="utf-8")
        paste_text = text.read()
        link = (
            post(
                "https://nekobin.com/api/documents",
                json={"content": paste_text},
            )
            .json()
            .get("result")
            .get("key")
        )
        text = "**Pasted to Nekobin!!!**"
        buttons = [
            [
                InlineKeyboardButton(
                    text="View Link", url=f"https://nekobin.com/{link}"
                ),
                InlineKeyboardButton(
                    text="View Raw",
                    url=f"https://nekobin.com/raw/{link}",
                ),
            ]
        ]
        msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        os.remove("file.txt")
    else:
        msg.reply_text("Give me a text file to paste on nekobin")
        return


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

stats_str = '''
'''

# Credits to Dank-del <https://github.com/Dank-del/EnterpriseALRobot>

@kaicmd(command="stats", can_disable=False)
@sudo_plus
def stats(update, context):
    db_size = SESSION.execute("SELECT pg_size_pretty(pg_database_size(current_database()))").scalar_one_or_none()
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    botuptime = get_readable_time((time.time() - StartTime))
    status = "*╒═══「 System statistics 」*\n\n"
    status += "*• System Start time:* " + str(uptime) + "\n"
    uname = platform.uname()
    status += "*• System:* " + str(uname.system) + "\n"
    status += "*• Node name:* " + escape_markdown(str(uname.node)) + "\n"
    status += "*• Release:* " + escape_markdown(str(uname.release)) + "\n"
    status += "*• Machine:* " + escape_markdown(str(uname.machine)) + "\n"
    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "*• CPU:* " + str(cpu) + " %\n"
    status += "*• RAM:* " + str(mem[2]) + " %\n"
    status += "*• Storage:* " + str(disk[3]) + " %\n\n"
    status += "*• Python Version:* " + python_version() + "\n"
    status += "*• python-Telegram-Bot:* " + str(ptbver) + "\n"
    status += "*• Uptime:* " + str(botuptime) + "\n"
    status += "*• Database size:* " + str(db_size) + "\n"
    kb = [[InlineKeyboardButton('Ping', callback_data='pingCB')]]
    try:
        update.effective_message.reply_text(status +
            "\n*Bot statistics*:\n"
            + "\n".join([mod.__stats__() for mod in STATS]) +
            "\n\n[⍙ GitHub](https://github.com/Ryomen-Sukuna/Kai) | [⍚ GitLab](https://gitlab.com/Ryomen-Sukuna/Kai)\n\n" +
            "╘══「 by [Ryomen-Sukuna](github.com/Ryomen-Sukuna) 」\n",
        parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb), disable_web_page_preview=True)
    except BaseException:
        update.effective_message.reply_text(
            ((("\n*Bot statistics*:\n" + "\n".join(mod.__stats__() for mod in STATS))
            + "\n\n⍙ [GitHub](https://github.com/Ryomen-Sukuna/Kai) | ⍚ [GitLab](https://gitlab.com/Ryomen-Sukuna/Kai)\n\n")
            + "╘══「 by [Ryomen-Sukuna](github.com/Ryomen-Sukuna) 」\n"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb),
            disable_web_page_preview=True,
        )


@kaicmd(command="ping")
def ping(update: Update, _):
    msg = update.effective_message
    start_time = time.time()
    message = msg.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    message.edit_text(
        "*PONG!!!*\n`{}ms`".format(ping_time), parse_mode=ParseMode.MARKDOWN
    )


@kaicallback(pattern=r"^pingCB")
def pingCallback(update: Update, _):
    query = update.callback_query
    start_time = time.time()
    requests.get('https://api.telegram.org')
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    query.answer('Pong! {}ms'.format(ping_time))



__help__ = """
*Available commands:*

*Markdown:*
>> /markdownhelp: quick summary of how markdown works in telegram - can only be called in private chats.

*Paste:*
>> /paste: Saves replied content to `nekobin.com` and replies with a url.

*React:*
>> /react: Reacts with a random reaction.

*Urban Dictonary:*
>> /ud <word>: Type the word or expression you want to search use.

*Last FM:*
>> /setuser <username>: sets your last.fm username.
>> /clearuser: removes your last.fm username from the bot's database.
>> /lastfm: returns what you're scrobbling on last.fm.

*Reverse:*
>> /reverse: Does a reverse image search of the media which it was replied to.
>> /grs: same like reverse.

*Wikipedia:*
>> /wiki <query>: wikipedia your query.

*Wallpapers:*
>> /wall <query>: get a wallpaper from wall.alphacoders.com.

*Currency converter:* 
>> /cash: currency converter
*An example for using cash:*
`/cash 1 USD INR`  
     _OR_
`/cash 1 usd inr`
Output: `1.0 USD = 75.505 INR`
"""


__mod_name__ = "Misc"

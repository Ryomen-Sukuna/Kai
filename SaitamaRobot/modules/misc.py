import time
from typing import List
from KaiRoboto.modules.helper_funcs.chat_status import user_admin
from KaiRoboto.modules.disable import DisableAbleCommandHandler
from KaiRoboto import dispatcher

import requests
from telegram import ParseMode, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode, Update
from telegram.ext.dispatcher import run_async
from telegram.ext import CallbackContext, Filters, CommandHandler
from KaiRoboto import StartTime, dispatcher
from KaiRoboto.modules.helper_funcs.chat_status import sudo_plus
from KaiRoboto.modules.disable import DisableAbleCommandHandler

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


@run_async
@user_admin
def echo(update: Update, context: CallbackContext):
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


def markdown_help_sender(update: Update):
    update.effective_message.reply_text(MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see, and Use #test!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, code, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )


@run_async
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

def ping(update: Update, _):
    msg = update.effective_message
    start_time = time.time()
    message = msg.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    message.edit_text(
        "*Pong!!!*\n`{}ms`".format(ping_time), parse_mode=ParseMode.MARKDOWN
    )

__help__ = """
*Available commands:*
*Markdown:*
 • `/markdownhelp`*:* quick summary of how markdown works in telegram - can only be called in private chats

 *Paste:*
 • `/paste`*:* Saves replied content to `nekobin.com` and replies with a url

 *React:*
 • `/react`*:* Reacts with a random reaction 

 *Urban Dictonary:*
 • `/ud <word>`*:* Type the word or expression you want to search use

 *Last FM:*
 • `/setuser <username>`*:* sets your last.fm username.
 • `/clearuser`*:* removes your last.fm username from the bot's database.
 • `/lastfm`*:* returns what you're scrobbling on last.fm

 *Reverse:*
 • `/reverse`*:* Does a reverse image search of the media which it was replied to.

 *Wikipedia:*
 • `/wiki <query>`*:* wikipedia your query

 *Wallpapers:*
 • `/wall <query>`*:* get a wallpaper from wall.alphacoders.com

 *Currency converter:* 
 • `/cash`*:* currency converter
 Example:
 `/cash 1 USD INR`  
      _OR_
 `/cash 1 usd inr`
 Output: `1.0 USD = 75.505 INR`
"""

ECHO_HANDLER = DisableAbleCommandHandler("echo", echo, filters=Filters.group)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help)
PING_HANDLER = DisableAbleCommandHandler("ping", ping)

dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(PING_HANDLER)

__mod_name__ = "Extras"
__command_list__ = ["id", "echo","ping"]
__handlers__ = [
    ECHO_HANDLER,
    MD_HELP_HANDLER,
    PING_HANDLER
]

from telethon import events
from pyrogram import filters
from SaitamaRobot import kp
from SaitamaRobot import telethn
from SaitamaRobot.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)
import asyncio
from pyrogram import raw

async def user_can_purge(_, c, m):
    mem = await c.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
    if mem.can_delete_messages or mem.status in ("creator"):
        return True
    await m.reply("You Don't Have Permission To Delete Messages")

can_purge = filters.create(user_can_purge)

@kp.on_message(filters.command("purge")& filters.reply & can_purge, group=0)
async def purge(c, m):
    messages = list(range(m.message_id + 1, m.reply_to_message.message_id, -1))
    while len(messages) != 0:
        await c.send(
            raw.functions.channels.DeleteMessages(
                channel=await c.resolve_peer(m.chat.id), id=messages))
        del messages[0:100]
    await c.send_message(
        text="**Fast Purge Completed!!!**",
        chat_id=m.chat.id)

@kp.on_message(filters.command('purge')& ~filters.reply & can_purge)
async def int_purge(c, m):
    try:
        count = int(m.command[1])
    except IndexError:
        await m.reply("__specifiy number of messages to delete__")
        return
    messages = list(range(m.message_id - 1, m.message_id - 1 - count, -1))
    start, end = messages[-1], messages[0]
    while len(messages) != 0:
        await c.send(
            raw.functions.channels.DeleteMessages(
                channel=await c.resolve_peer(m.chat.id), id=messages))
        del messages[0:100]
    await c.send_message(
        text=f"Purged {count} messages from {start} to {end}",chat_id=m.chat.id)

async def purge_messages(event):
    start = time.perf_counter()
    if event.from_id is None:
        return

    if not await user_is_admin(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("Only Admins are allowed to use this command")
        return

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to purge the message")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return
    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id

    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            messages = []

    try:
        await event.client.delete_messages(event.chat_id, messages)
    except:
        pass
    time_ = time.perf_counter() - start
    text = f"Purged Successfully in {time_:0.2f} Second(s)"
    await event.respond(text, parse_mode="markdown")


async def delete_messages(event):
    if event.from_id is None:
        return

    if not await user_is_admin(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("Only Admins are allowed to use this command")
        return

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to delete this?")
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("Whadya want to delete?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)


__help__ = """
*Admin only:*
 - /del: deletes the message you replied to
 - /purge: deletes all messages between this and the replied to message.
 - /purge <integer X>: deletes the replied message, and X messages following it if replied to a message.
"""

PURGE_HANDLER = purge_messages, events.NewMessage(pattern="^[!/]purge$")
DEL_HANDLER = delete_messages, events.NewMessage(pattern="^[!/]del$")

telethn.add_event_handler(*PURGE_HANDLER)
telethn.add_event_handler(*DEL_HANDLER)

__mod_name__ = "Purges"
__command_list__ = ["del", "purge"]
__handlers__ = [PURGE_HANDLER, DEL_HANDLER]

import logging
import os
import sys, json
import time
import spamwatch
import telegram.ext as tg
from telethon import TelegramClient
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Chat, User
from configparser import ConfigParser
from rich.logging import RichHandler
StartTime = time.time()

def get_user_list(__init__, key):
    with open("{}/SaitamaRobot/{}".format(os.getcwd(), __init__), "r") as json_file:
        return json.load(json_file)[key]

# enable logging
FORMAT = "[ShieHashaikai] %(message)s"
logging.basicConfig(handlers=[RichHandler()], level=logging.INFO, format=FORMAT, datefmt="[%X]")
logging.getLogger("pyrogram").setLevel(logging.WARNING)
log = logging.getLogger("rich")

log.info("[KAI] Kai is starting. | An Zero Union Project. | Licensed under GPLv3.")

log.info("[KAI] Not affiliated to Shie Hashaikai or Vilain in any way whatsoever.")
log.info("[KAI] Project maintained by: github.com/ChisakiKai (t.me/Anomaliii)")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    log.error(
        "[KAI] You MUST have a python version of at least 3.7! Multiple features depend on this. Bot quitting."
    )
    quit(1)

parser = ConfigParser()
parser.read("config.ini")
kaiconfig = parser["kaiconfig"]


OWNER_ID = kaiconfig.getint("OWNER_ID")
OWNER_USERNAME = kaiconfig.get("OWNER_USERNAME")
APP_ID = kaiconfig.getint("APP_ID")
API_HASH = kaiconfig.get("API_HASH")
WEBHOOK = kaiconfig.getboolean("WEBHOOK", False)
URL = kaiconfig.get("URL", None)
CERT_PATH = kaiconfig.get("CERT_PATH", None)
PORT = kaiconfig.getint("PORT", None)
INFOPIC = kaiconfig.getboolean("INFOPIC", False)
DEL_CMDS = kaiconfig.getboolean("DEL_CMDS", False)
STRICT_GBAN = kaiconfig.getboolean("STRICT_GBAN", False)
ALLOW_EXCL = kaiconfig.getboolean("ALLOW_EXCL", False)
CUSTOM_CMD = kaiconfig.get("CUSTOM_CMD", None)
BAN_STICKER = kaiconfig.get("BAN_STICKER", None)
TOKEN = kaiconfig.get("TOKEN")
DB_URI = kaiconfig.get("SQLALCHEMY_DATABASE_URI")
LOAD = kaiconfig.get("LOAD").split()
LOAD = list(map(str, LOAD))
MESSAGE_DUMP = kaiconfig.getfloat("MESSAGE_DUMP")
GBAN_LOGS = kaiconfig.getfloat("GBAN_LOGS")
NO_LOAD = kaiconfig.get("NO_LOAD").split()
NO_LOAD = list(map(str, NO_LOAD))
DRAGONS = get_user_list("elevated_users.json", "sudos")
DEV_USERS = get_user_list("elevated_users.json", "devs")
DEMON = get_user_list("elevated_users.json", "supports")
TIGERS = get_user_list("elevated_users.json", "demons")
WOLVES = get_user_list("elevated_users.json", "tigers")
SPAMMERS = get_user_list("elevated_users.json", "wolves")
spamwatch_api = kaiconfig.get("spamwatch_api")
CASH_API_KEY = kaiconfig.get("CASH_API_KEY")
TIME_API_KEY = kaiconfig.get("TIME_API_KEY")
WALL_API = kaiconfig.get("WALL_API")
LASTFM_API_KEY = kaiconfig.get("LASTFM_API_KEY")
try:
    CF_API_KEY = kaiconfig.get("CF_API_KEY")
    log.info("[NLP] AI antispam powered by Intellivoid.")
except:
    log.info("[NLP] No Coffeehouse API key provided.")
    CF_API_KEY = None


SUDO_USERS.append(OWNER_ID)
DEV_USERS.append(OWNER_ID)

# SpamWatch
if spamwatch_api is None:
    sw = None
    log.warning("SpamWatch API key is missing! Check your config.ini")
else:
    try:
        sw = spamwatch.Client(spamwatch_api)
    except:
        sw = None
        log.warning("Can't connect to SpamWatch!")

updater = tg.Updater(TOKEN, workers=min(32, os.cpu_count() + 4), request_kwargs={"read_timeout": 10, "connect_timeout": 10})
telethn = TelegramClient("kai", API_ID, API_HASH)
dispatcher = updater.dispatcher

kp = Client("KaiPyro", api_id=APP_ID, api_hash=API_HASH, bot_token=TOKEN, workers=min(32, os.cpu_count() + 4))
apps = []
apps.append(kp)


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:
                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from SaitamaRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

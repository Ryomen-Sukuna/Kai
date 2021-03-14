# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os


def get_user_list(config, key):
    with open("{}/SaitamaRobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 1511741  
    API_HASH = "ec3909aaa39889f44148d1f0e3c888be"
    TOKEN = "1608658535:AAEYPj-yr3OgSvdEj4zaCDqHbNIGzD6PPNM"
    OWNER_ID = 645739169  
    OWNER_USERNAME = "Anomaliii"
    SUPPORT_CHAT = "ZeroBotSupport"
    JOIN_LOGGER = (
        -1001253661229
    )  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = (
        -1001190806654
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    # RECOMMENDED
    SQLALCHEMY_DATABASE_URI = "postgres://u6vhed6ujtu306:pa2bd9cba0f797f243ba9e7dc858057b8eef2ab0b4a5a242a165e156767ab43a5@ec2-3-213-66-125.compute-1.amazonaws.com:5432/dehpp360ikbooo"  # needed for any database modules # its "URI" and not "URL" as herok and similar ones only accept it as such
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    # OPTIONAL
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list("elevated_users.json", "supports")
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = None  
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  
    STRICT_GBAN = True
    WORKERS = 8 
    BAN_STICKER = "" 
    ALLOW_EXCL = True 
    CASH_API_KEY = "HTGGP6MNR4723PMX" 
    TIME_API_KEY = "351YPDTFI28B" 
    WALL_API = "5ebd89288c6c23da598151b3b2e366bc"
    AI_API_KEY = "awoo" 
    BL_CHATS = []  
    SPAMMERS = None
    LASTFM_API_KEY = None
    CUSTOM_CMD = False
    CF_API_KEY = "0799060b18b294009263af0e5276044566a9773c3a018c4dfe033f1db8e3e02c879d4740a62c507f47ef0d15d9f84d8dfa7842e02901b5fe986d11cc31f0c749"
    LASTFM_API_KEY = "eb81a880f9e1afe02c9d9f52a72d8e59"
    ALLOW_CHATS = -1001442216071


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True

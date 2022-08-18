# Telegram - Twitter - Bot
# Github.com/New-dev0/TgTwitterStreamer
# GNU General Public License v3.0

import sys
import logging
from Configs import Var
from telethon import TelegramClient
from telethon.tl.custom import Button
from tweepy.asynchronous import AsyncClient

REPO_LINK = "https://github.com/New-dev0/TgTwitterStreamer"

_DEBUG = "--debug" in sys.argv

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO if not _DEBUG else logging.DEBUG,
)

LOGGER = logging.getLogger("TgTwitterStreamer")
LOGGER.debug("Starting in debug mode..")

# Tweepy's Client
Twitter = AsyncClient(
    Var.BEARER_TOKEN,
    Var.CONSUMER_KEY,
    Var.CONSUMER_SECRET,
    Var.ACCESS_TOKEN,
    Var.ACCESS_TOKEN_SECRET,
)

# Telegram's Client
# Used for sending messages to Chat.

_Tlog = logging.getLogger("Telethon")
_Tlog.setLevel(logging.INFO)

Client = TelegramClient(
    None, api_id=Var.API_ID, api_hash=Var.API_HASH, base_logger=_Tlog
).start(bot_token=Var.BOT_TOKEN)

Client.SELF = Client.loop.run_until_complete(Client.get_me())

CUSTOM_BUTTONS = None
TRACK_USERS = None
TRACK_WORDS = None


CUSTOM_FORMAT = """
🔥 <b>Tipster <a href='{SENDER_PROFILE}'>{SENDER}</a></b>
{REPLY_TAG}
💵 1un. (2.00%)
{TWEET_TEXT}
"""


if not Var.CUSTOM_TEXT:
    Client.parse_mode = "html"
    Var.CUSTOM_TEXT = CUSTOM_FORMAT

if Var.LANGUAGES:
    Var.LANGUAGES = Var.LANGUAGES.split()

# Username are easy to Fill and can easy be recognized that Unqiue Chat ids.
# And Ids should be in int form..
if Var.TO_CHAT:
    _chats = []
    for chat in Var.TO_CHAT.split():
        try:
            chat = int(chat)
        except ValueError:
            pass
        _chats.append(chat)
    Var.TO_CHAT = _chats
else:
    LOGGER.info("Please Add 'TO_CHAT' Var to Use TgTwitterStreamer!")
    LOGGER.info(
        "'TO_CHAT' : Fill Telegram Username/Chat ids," + "so that you can get tweets."
    )
    LOGGER.info("Quitting Now..")
    exit()


if Var.CUSTOM_BUTTON:
    button = []
    try:
        for line in Var.CUSTOM_BUTTON.split("||"):
            new = []
            for but in line.split("|"):
                spli_ = but.split("-", maxsplit=1)
                new.append(Button.url(spli_[0].strip(), spli_[1].strip()))
            button.append(new)
        CUSTOM_BUTTONS = button
    except Exception as er:
        LOGGER.exception(er)


LOGGER.info("<<--- Setting Up Bot ! --->>")


if Var.TRACK_USERS:
    TRACK_USERS = Var.TRACK_USERS.strip().split(" ")


if Var.TRACK_WORDS:
    TRACK_WORDS = Var.TRACK_WORDS.split(" | ")

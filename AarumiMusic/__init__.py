from AarumiMusic.core.bot import Aarumi
from AarumiMusic.core.dir import dirr
from AarumiMusic.core.git import git
from AarumiMusic.core.userbot import Userbot
from AarumiMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Aarumi()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

import random
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from AarumiMusic import app
from AarumiMusic.core.call import Aarumi
from AarumiMusic.utils import bot_sys_stats
from AarumiMusic.utils.decorators.language import language
from AarumiMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL

SHASHANK_PIC = [
    "https://files.catbox.moe/t6485t.jpg",
    "https://files.catbox.moe/4osoc3.jpg",
    "https://files.catbox.moe/t6485t.jpg",
    "https://files.catbox.moe/5e18lv.jpg",
    "https://files.catbox.moe/bupvsx.jpg",
    "https://files.catbox.moe/w7f2wa.jpg",
    "https://files.catbox.moe/2b2dam.jpg",
    "https://files.catbox.moe/qity19.jpg"
]

@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo=random.choice(SHASHANK_PIC),
        has_spoiler=True,
       caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Aarumi.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )

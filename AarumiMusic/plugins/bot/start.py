import asyncio
import time
import random 
from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from AarumiMusic import app
from AarumiMusic.misc import _boot_
from AarumiMusic.plugins.sudo.sudoers import sudoers_list
from AarumiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AarumiMusic.utils.decorators.language import LanguageStart
from AarumiMusic.utils.formatters import get_readable_time
from AarumiMusic.utils.inline import first_page, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

STICKER = [
        "CAACAgUAAxkBAAEBL29nho9ewF0e4aUP05Z_haRVCScpkgACngEAAgx_iVfmazE9xbmj_R4E",
        "CAACAgUAAxkBAAEBL3Bnho9edQ3env6-ayR5E4vfS_fx-wACQAEAAg4uiVdelMPu_8BiQR4E"
        "CAACAgUAAxkBAAEBL3Fnho9fSdZgtn18rBHkPVBbVB55fwACtgEAAq-6iVclVowlEMgs9h4E",
        "CAACAgUAAxkBAAEBL3Jnho9hn2Zjjk5xf23hc2ZLNRDw7gACjQEAAlgzyFfn6fcRs_J9YR4E",
        "CAACAgUAAxkBAAEBL3Nnho9hMDuEtzHd3f8YWizPP-aH4gAC8AEAAjREiVdB_ysq-ctClR4E",
        "CAACAgUAAxkBAAEBL3Rnho9jbzfA4Ljox-gdwvWekZY9vQACcwIAAl6TqVWFNPy_WS5bax4E",
        "CAACAgUAAxkBAAEBL3Vnho9ouf4Oig3_neT1mr11BanP8gACfQEAAu14sVcpw-MZJT2S6h4E",
        "CAACAgUAAxkBAAEBL3Znho9pdvbWndWLOXIdZorYaP1VPgACrAEAAkuOwVdzqZh19Ol7RB4E",
        "CAACAgUAAxkBAAEBL3dnho9wj60On5cbNkHj5lgzPO0ZbQACQwIAAp3CsVUV8b4slQg-fh4E",
        "CAACAgUAAxkBAAEBL3hnho9x6apcO7Rw-2F4KCQD6NhzcwACgwIAApbkuFVY51aPcyVZfB4E",
]

START_IMG_URL = [
    "https://files.catbox.moe/u7iwi5.jpg",
    "https://files.catbox.moe/rkskww.jpg",
    "https://files.catbox.moe/uz810n.jpg",
    "https://files.catbox.moe/vzl4xb.jpg",
    "https://files.catbox.moe/j2zdsu.jpg",
    "https://files.catbox.moe/nlweex.jpg",
    "https://files.catbox.moe/pp4god.jpg",
    "https://files.catbox.moe/jslln0.jpg",
    "https://files.catbox.moe/fqmdff.jpg",
    "https://files.catbox.moe/eushjw.jpg",
    "https://files.catbox.moe/39fg3k.jpg",
]

VALID_EMOJII = ["🔥", "💋", "🥺", "😒", "💖",
                "💘", "💕", "✨", "🥰", "🍌", "💔",
                "😓", "🫧"]

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    random_emoji = random.choice(VALID_EMOJII)  # Pick a valid emoji
    try:
        await message.react(random_emoji)
    except Exception as e:
        print(f"Error reacting with emoji: {e}")
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = first_page(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)

        # First start_2 send photo with caption
        sticker_msg = await message.reply_sticker(
                sticker=random.choice(STICKER),  # Random sticker from the list
            )
        await asyncio.sleep(0.5)  # the sticker will be deleted after 0.5 seconds
        await sticker_msg.delete()  # delete the sticker message

        await message.reply_photo(
            photo=random.choice(START_IMG_URL),
            caption=_["start_1"].format(message.from_user.mention), parse_mode=ParseMode.HTML,)

        await message.reply_text(text=_["start_2"].format(app.mention), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(out),)

        # Agar logging on hai, to message bhejo
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_0"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
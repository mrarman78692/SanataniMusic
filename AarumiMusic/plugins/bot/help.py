import random
from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message
from AarumiMusic import app
from AarumiMusic.utils import help_pannel
from AarumiMusic.utils.database import get_lang
from AarumiMusic.utils.decorators.language import LanguageStart, languageCB
from AarumiMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, SUPPORT_CHAT
from strings import get_string, helpers

SHASHANK_PIC = [
    "https://files.catbox.moe/t6485t.jpg",
    "https://files.catbox.moe/4osoc3.jpg",
    "https://files.catbox.moe/5e18lv.jpg",
    "https://files.catbox.moe/bupvsx.jpg",
    "https://files.catbox.moe/w7f2wa.jpg",
    "https://files.catbox.moe/2b2dam.jpg",
    "https://files.catbox.moe/qity19.jpg",
]

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)

    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            random.choice(SHASHANK_PIC),
            has_spoiler=True,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    help_texts = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
    }

    if cb in help_texts:
        await CallbackQuery.edit_message_text(
            help_texts[cb],
            reply_markup=keyboard,
        )

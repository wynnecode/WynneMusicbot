#
# Copyright (C) 2024 by AnonymousX888@Github, < https://github.com/AnonymousX888 >.
#
# This file is part of < https://github.com/hakutakaid/Music-Indo.git > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/Music-Indo.git/blob/master/LICENSE >
#
# All rights reserved.
#
from strings import get_string
from WyneMusic.misc import SUDOERS
from WyneMusic.utils.database import get_lang, is_commanddelete_on, is_maintenance


def language(mystic):
    async def wrapper(_, message, **kwargs):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "» ʙᴏᴛ ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ғᴏʀ sᴏᴍᴇ ᴛɪᴍᴇ, ᴩʟᴇᴀsᴇ ᴠɪsɪᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ ᴛᴏ ᴋɴᴏᴡ ᴛʜᴇ ʀᴇᴀsᴏɴ."
                )
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("id")  # Mengganti default dari "en" menjadi "id"
        return await mystic(_, message, language)

    return wrapper


def languageCB(mystic):
    async def wrapper(_, CallbackQuery, **kwargs):
        if await is_maintenance() is False:
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    "» ʙᴏᴛ ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ғᴏʀ sᴏᴍᴇ ᴛɪᴍᴇ, ᴩʟᴇᴀsᴇ ᴠɪsɪᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ ᴛᴏ ᴋɴᴏᴡ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    show_alert=True,
                )
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            language = get_string(language)
        except:
            language = get_string("id")  # Mengganti default dari "en" menjadi "id"
        return await mystic(_, CallbackQuery, language)

    return wrapper


def LanguageStart(mystic):
    async def wrapper(_, message, **kwargs):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("id")  # Mengganti default dari "en" menjadi "id"
        return await mystic(_, message, language)

    return wrapper

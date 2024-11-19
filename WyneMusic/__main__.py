#
# Copyright (C) 2024 by AnonymousX888@Github, < https://github.com/AnonymousX888 >.
#
# This file is part of < https://github.com/hakutakaid/Music-Indo.git > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/Music-Indo.git/blob/master/LICENSE >
#
# All rights reserved.
import asyncio
import importlib
from pyrogram import idle
import config
from config import BANNED_USERS
from WyneMusic import HELPABLE, LOGGER, app, userbot
from WyneMusic.core.call import Yukki
from WyneMusic.plugins import ALL_MODULES
from WyneMusic.utils.database import get_banned_users, get_gbanned


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("WyneMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("WyneMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                if imported_module.__MODULE__.lower() not in HELPABLE:
                    HELPABLE[imported_module.__MODULE__.lower()] = imported_module
                else:
                    raise Exception(
                        f"Can't have two modules with name! '{imported_module.__MODULE__}' Please Change One"
                    )

    LOGGER("WyneMusic.plugins").info("Successfully Imported All Modules ")
    await userbot.start()
    await Yukki.start()
    await Yukki.decorators()
    LOGGER("WyneMusic").info("WyneMusic Started Successfully")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(init())
    LOGGER("WyneMusic").info("Stopping WyneMusic! GoodBye")

import asyncio

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AloneX import YouTube, app
from AloneX.core.call import Alone
from AloneX.misc import SUDOERS, db   # SPECIAL_ID removed (not used)
from AloneX.utils.database import (
    get_active_chats,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_music_playing,
    is_nonadmin_chat,
    music_off,
    music_on,
    set_loop,
)
from AloneX.utils.decorators.language import languageCB
from AloneX.utils.formatters import seconds_to_min
from AloneX.utils.inline import close_markup, stream_markup, stream_markup_timer
from AloneX.utils.stream.autoclear import auto_clean
from AloneX.utils.thumbnails import get_thumb
from config import (
    BANNED_USERS,
    SUPPORT_CHAT,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
    confirmer,
    votemode,
)
from strings import get_string


checker = {}
upvoters = {}


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]
    chat_id = int(chat)

    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)

    mention = CallbackQuery.from_user.mention

    # --- UPVOTE SYSTEM ---
    if command == "UpVote":
        if chat_id not in votemode:
            votemode[chat_id] = {}
        if chat_id not in upvoters:
            upvoters[chat_id] = {}

        voters = (upvoters[chat_id]).get(CallbackQuery.message.id)
        if not voters:
            upvoters[chat_id][CallbackQuery.message.id] = []

        vote = (votemode[chat_id]).get(CallbackQuery.message.id)
        if not vote:
            votemode[chat_id][CallbackQuery.message.id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            upvoters[chat_id][CallbackQuery.message.id].remove(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            upvoters[chat_id][CallbackQuery.message.id].append(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] += 1

        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.id])

        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]
            except:
                return await CallbackQuery.edit_message_text("ғᴀɪʟᴇᴅ.")

            try:
                if current["vidid"] != exists["vidid"]:
                    return await CallbackQuery.edit_message_text(_["admin_35"])
                if current["file"] != exists["file"]:
                    return await CallbackQuery.edit_message_text(_["admin_35"])
            except:
                return await CallbackQuery.edit_message_text(_["admin_36"])

            try:
                await CallbackQuery.edit_message_text(
                    _["admin_37"].format(upvote)
                )
            except:
                pass

            command = counter
            mention = "ᴜᴘᴠᴏᴛᴇs"

        else:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"👍 {get_upvotes}",
                            callback_data=f"ADMIN  UpVote|{chat_id}_{counter}",
                        )
                    ]
                ]
            )
            await CallbackQuery.answer(_["admin_40"], show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)

    # --- ADMIN CHECK ---
    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                admins = adminlist.get(CallbackQuery.message.chat.id)
                if not admins:
                    return await CallbackQuery.answer(_["admin_13"], show_alert=True)
                else:
                    if CallbackQuery.from_user.id not in admins:
                        return await CallbackQuery.answer(
                            _["admin_14"], show_alert=True
                        )

    # ---- CONTROLS ----
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_1"], show_alert=True)

        await music_off(chat_id)
        await Alone.pause_stream(chat_id)

    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_3"], show_alert=True)

        await music_on(chat_id)
        await Alone.resume_stream(chat_id)

    elif command in ["Stop", "End"]:
        await Alone.stop_stream(chat_id)
        await set_loop(chat_id, 0)

    # (baaki code same rehne diya, tera logic untouched)

# ----- TIMER -----
async def markup_timer():
    while not await asyncio.sleep(7):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                if not await is_music_playing(chat_id):
                    continue

                playing = db.get(chat_id)
                if not playing:
                    continue

                duration_seconds = int(playing[0]["seconds"])
                if duration_seconds == 0:
                    continue

                mystic = playing[0].get("mystic")
                if not mystic:
                    continue

                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")

                buttons = stream_markup_timer(
                    _,
                    chat_id,
                    seconds_to_min(playing[0]["played"]),
                    playing[0]["dur"],
                )

                await mystic.edit_reply_markup(
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            except:
                continue


asyncio.create_task(markup_timer())

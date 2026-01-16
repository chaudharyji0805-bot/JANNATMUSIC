from pyrogram.types import InlineKeyboardButton

import config
from AloneX import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                        text="˹ 𝐒ᴜᴘᴘᴏʀᴛ ˼", url=config.SUPPORT_CHAT
                    ),
            InlineKeyboardButton(
                        text="˹ 𝐔ᴘᴅᴀᴛᴇs ˼", url=config.SUPPORT_CHANNEL
                    ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_7"], callback_data="gib_source"),
            InlineKeyboardButton(
                       text="˹ 𝐎ᴡɴᴇʀ ˼", user_id=config.OWNER_ID
                    ),
        ],
        [InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper")],
        [
            InlineKeyboardButton("˹ 𝐁σт 𝐈иғσ ˼", callback_data="bot_info_data"),
      #  ],
      #  [
           # InlineKeyboardButton("?⃟≛⃝ 𝆺𝅥⃝🍃 𝗗꯭ᴇ꯭ᴠ꯭ᴀ꯭─꯭⃜❰⎯꯭⃜ 🌿•┼⃖‌ꭗ𓆪", url=f"https://t.me/MeDevu"),
        ],
    ]
    return buttons

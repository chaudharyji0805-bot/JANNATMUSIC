from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AloneX import app
from config import BOT_USERNAME
#from AloneX.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
**
┌┬─────────────────⦿
│├─────────────────╮
│├ 𝗧ɢ 𝗡ᴀᴍᴇ - [𝐃ᴇᴠᴀ](https://t.me/btw_deva)
│├ 𝗙ᴜʟʟ 𝗜ɴғᴏ - [𝐂ʟɪᴄᴋ 𝐇ᴇʀᴇ](https://t.me/AboutDeva)
│├─────────────────╯
├┼─────────────────⦿
│├─────────────────╮
│├ 𝗢ᴡɴᴇʀ│ [𝐃ᴇᴠᴀ  𝗖ᴏᴅᴇʀ](https://t.me/btw_deva)
│├─────────────────╯
└┴─────────────────⦿
**
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("ᴠɪᴩ ᴅᴇᴠᴀ", url="https://t.me/btw_deva")
        ],
        [
          InlineKeyboardButton("SUPPORT CHANNEL", url="https://t.me/BotzEmpire"),
          InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/Yaaro_kimehfill"),
          ],
               [
                InlineKeyboardButton("SHAYRI CHANNEL ", url="https://t.me/Matlabi_Duniyah"),
],
[
InlineKeyboardButton("about ", url="https://t.me/@AboutDeva"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://files.catbox.moe/l1y7ab.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )

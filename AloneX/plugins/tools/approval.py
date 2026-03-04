import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from VIP_DEVA import app

active_buttons = {}


@app.on_chat_join_request()
async def join_request_handler(client, join_req):
    chat = join_req.chat
    user = join_req.from_user
    
    request_key = f"{chat.id}_{user.id}"
    if request_key in active_buttons:
        return  
    
    active_buttons[request_key] = True

    text = (
        "**🚨  ɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ  !!**\n\n"
        f"**👤 ᴜsᴇʀ :-** {user.mention}\n"
        f"**🆔 ɪᴅ :-** `{user.id}`\n"
        f"**🔗 ᴜsᴇʀɴᴀᴍᴇ :-** @{user.username if user.username else 'ɴᴏɴᴇ'}\n\n"
        f"**📝 ɴᴏᴛᴇ :-** <i>ᴍᴇssᴀɢᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ɪɴ 5 ᴍɪɴᴜᴛᴇs.</i>"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"approve:{chat.id}:{user.id}"),
                InlineKeyboardButton("❌ ᴅɪsᴍɪss", callback_data=f"dismiss:{chat.id}:{user.id}")
            ]
        ]
    )

    sent = await client.send_message(chat.id, text, reply_markup=buttons)

    async def delete_and_cleanup():
        await asyncio.sleep(300)
        try:
            await client.delete_messages(chat.id, sent.id)
        except:
            pass
        finally:
            active_buttons.pop(request_key, None)

    asyncio.create_task(delete_and_cleanup())


@app.on_callback_query(filters.regex("^(approve|dismiss):"))
async def callback_handler(client: Client, query: CallbackQuery):
    action, chat_id, user_id = query.data.split(":")
    chat_id = int(chat_id)
    user_id = int(user_id)

    
    try:
        member = await client.get_chat_member(chat_id, query.from_user.id)
        if member.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            return await query.answer("⚠️ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ 😜", show_alert=True)
    except:
        return await query.answer("⚠️ ᴀᴅᴍɪɴ ᴄʜᴇᴄᴋ ғᴀɪʟᴇᴅ", show_alert=True)

    
    try:
        check_user = await client.get_chat_member(chat_id, user_id)
        if check_user.status in [
            enums.ChatMemberStatus.MEMBER,
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ]:
            
            await query.answer("✅ ᴜsᴇʀ ᴀʟʀᴇᴀᴅʏ ɪɴ ɢʀᴏᴜᴘ !!", show_alert=True)

            
            try:
                await query.message.delete()
            except:
                pass

            active_buttons.pop(f"{chat_id}_{user_id}", None)
            return
    except:
        pass

    
    if action == "approve":
        try:
            await client.approve_chat_join_request(chat_id, user_id)

            user_obj = await client.get_users(user_id)
            chat_obj = await client.get_chat(chat_id)

            await query.edit_message_text(
                f"**🎉 ᴅᴇᴀʀ {user_obj.mention}, ʏᴏᴜ ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ :-** `{chat_obj.title}`"
            )

        except Exception as e:
            await query.answer(f"⚠️ {str(e)}", show_alert=True)

    elif action == "dismiss":
        try:
            await client.decline_chat_join_request(chat_id, user_id)

            user_obj = await client.get_users(user_id)
            chat_obj = await client.get_chat(chat_id)

            await query.edit_message_text(
                f"**❌ ᴅᴇᴀʀ {user_obj.mention}, ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴅɪsᴍɪssᴇᴅ ғʀᴏᴍ :-** `{chat_obj.title}`"
            )

        except Exception as e:
            await query.answer(f"⚠️ {str(e)}", show_alert=True)

    active_buttons.pop(f"{chat_id}_{user_id}", None)

=======================

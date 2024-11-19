import io
import os
import asyncio
from config import BANNED_USERS  # BANNED_USERS imported from config
import google.generativeai as genai
from WyneMusic import app
from pyrogram import filters

# Define the API key for Google AI
AI_GOOGLE_API = "AIzaSyAM4A7L0Qj3loDZDupt0X74PDne6Tx2YLA"

class GoogleAI:
    @staticmethod
    async def google_ai(question):
        """
        Interact with Google's AI API to get a response for a question.
        """
        genai.configure(api_key=AI_GOOGLE_API)
        model = genai.GenerativeModel(model_name="gemini-1.0-pro")
        convo = model.start_chat(history=[])
        convo.send_message(question)
        return convo.last.text

def get_text(message):
    if message.reply_to_message:
        if len(message.text.split()) < 2:
            text = message.reply_to_message.text or message.reply_to_message.caption
        else:
            text = f"{message.reply_to_message.text or message.reply_to_message.caption}\n\n{message.text.split(None, 1)[1]}"
    else:
        if len(message.text.split()) < 2:
            text = ""
        else:
            text = message.text.split(None, 1)[1]
    return text

@app.on_message(filters.command(["ai", "ask", "gpt", "solve"], prefixes=["/", ".", "-", ""]))
async def ai_cmd(bot, message):
    if message.from_user.id in BANNED_USERS:  # Check if the user is banned
        return await message.reply("You are banned from using this bot.")

    Tm = await message.reply("<code>Processing...</code>")
    args = get_text(message)
    
    if not args:
        return await Tm.edit(f"<b><code>{message.text}</code> [Please provide a question]</b>")
    
    try:
        # Call Google AI to get a response
        response = await GoogleAI.google_ai(args)
        
        # If the response is too long, send it as a file
        if len(response) > 4096:
            with io.BytesIO(str.encode(response)) as out_file:
                out_file.name = "GoogleAI_Response.txt"
                await message.reply_document(document=out_file)
                await Tm.delete()
        else:
            # Reply with the AI's response
            msg = message.reply_to_message or message
            await bot.send_message(message.chat.id, response, reply_to_message_id=msg.id)
            await Tm.delete()
    
    except Exception as error:
        await Tm.edit(f"Error: {str(error)}")

# Module description and help information
__MODULE__ = "CʜᴀᴛGᴘᴛ"
__HELP__ = """
/advice - ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴀᴅᴠɪᴄᴇ ʙʏ ʙᴏᴛ
/ai [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ᴄʜᴀᴛɢᴘᴛ's ᴀɪ
/gemini [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ɢᴏᴏɢʟᴇ's ɢᴇᴍɪɴɪ ᴀɪ
/bard [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ɢᴏᴏɢʟᴇ's ʙᴀʀᴅ ᴀɪ
"""

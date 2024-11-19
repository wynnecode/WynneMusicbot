import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from WyneMusic import app

# Ganti URL ini dengan URL upload website Anda
UPLOAD_URL = 'https://nyxiannetwork.web.id/uploader/upload.php'

# Fungsi untuk memastikan direktori ada
def ensure_directories_exist():
    os.makedirs('uploads/dokumen', exist_ok=True)
    os.makedirs('uploads/img', exist_ok=True)
    os.makedirs('uploads/video', exist_ok=True)

@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ᴛᴏ ᴜᴘʟᴏᴀᴅ."
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 5 * 1024 * 1024:
        return await message.reply_text("Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇᴅɪᴀ ғɪʟᴇ ᴜɴᴅᴇʀ 𝟻MB.")
    
    text = await message.reply("Pʀᴏᴄᴇssɪɴɢ...")

    # Memastikan direktori yang diperlukan ada
    ensure_directories_exist()

    async def progress(current, total):
        await text.edit_text(f"📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ... {current * 100 / total:.1f}%")

    try:
        local_path = await media.download(progress=progress)
        await text.edit_text("📤Uᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛʜᴇ sᴇʀᴠᴇʀ...")

        try:
            # Mengunggah file ke server Anda
            with open(local_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(UPLOAD_URL, files=files)

            if response.status_code == 200:
                media_url = response.text.strip()  # Mengambil URL file yang berhasil diunggah
                if media_url:
                    await text.edit_text(
                        f"🌐 | [ᴜᴘʟᴏᴀᴅ ʟɪɴᴋ]({media_url})",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "📎 Open Link", url=media_url
                                    )
                                ]
                            ]
                        ),
                    )
                else:
                    await text.edit_text("<code>Upload berhasil, tetapi tidak ada URL yang diterima.</code>")
            else:
                await text.edit_text(f"<code>Gagal mengunggah: {response.status_code}</code>")
        except Exception as e:
            await text.edit_text(f"❌ Fɪʟᴇ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ\n\n<i>Rᴇᴀsᴏɴ: {e}</i>")
        finally:
            # Menghapus file lokal setelah diunggah
            try:
                os.remove(local_path)
            except Exception:
                pass

    except Exception as e:
        await text.edit_text(f"❌ Dᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ\n\n<i>Rᴇᴀsᴏɴ: {e}</i>")

__HELP__ = """
**ᴛᴇʟᴇɢʀᴀᴘʜ ᴜᴘʟᴏᴀᴅ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs**

ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴍᴇᴅɪᴀ ᴛᴏ ᴛʜᴇ sᴇʀᴠᴇʀ:

- `/tgm`: ᴜᴘʟᴏᴀᴅ ʀᴇᴘʟɪᴇᴅ ᴍᴇᴅɪᴀ ᴛᴏ ᴛʜᴇ sᴇʀᴠᴇʀ.
- `/tgt`: sᴀᴍᴇ ᴀs `/tgm`.
- `/telegraph`: sᴀᴍᴇ ᴀs `/tgm`.
- `/tl`: sᴀᴍᴇ ᴀs `/tgm`.

**ᴇxᴀᴍᴘʟᴇ:**
- ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ ᴡɪᴛʜ `/tgm` ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ.

**ɴᴏᴛᴇ:**
ʏᴏᴜ ᴍᴜsᴛ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ғɪʟᴇ ғᴏʀ ᴛʜᴇ ᴜᴘʟᴏᴀᴅ ᴛᴏ ᴡᴏʀᴋ.
"""

__MODULE__ = "Tᴇʟᴇɢʀᴀᴘʜ"

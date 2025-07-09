from telethon import TelegramClient, events
import re
import os
import datetime
import shutil

# Ganti dengan API ID dan HASH kamu dari my.telegram.org
api_id = 21737007
api_hash = 'a2245bd65201ebc830fec7d169db6703'

client = TelegramClient('session_userbot', api_id, api_hash)
os.makedirs("downloads", exist_ok=True)

link_regex = re.compile(r't\.me\/c\/(\d+)\/(\d+)')

@client.on(events.NewMessage)
async def handler(event):
    msg = event.raw_text.strip()
    match = link_regex.search(msg)

    if match:
        chat_id = int("-100" + match.group(1))
        message_id = int(match.group(2))

        try:
            pesan = await client.get_messages(chat_id, ids=message_id)

            if pesan.media:
                # Unduh ke folder downloads/
                original_path = await pesan.download_media(file='downloads/')
                ext = os.path.splitext(original_path)[1]

                # Tentukan jenis file
                if pesan.photo:
                    jenis = "photo"
                elif pesan.video or (pesan.document and ext in ['.mp4', '.mov', '.mkv']):
                    jenis = "video"
                elif pesan.document:
                    jenis = "document"
                else:
                    jenis = "file"

                # Format nama file baru
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                new_filename = f"{jenis}-{timestamp}{ext}"
                new_path = os.path.join('downloads', new_filename)

                # Rename file
                shutil.move(original_path, new_path)

                # Kirim file ke Telegram
                await client.send_file(event.chat_id, new_path, caption=f"✅ Berikut media dari link kamu:\n📎 {new_filename}")

                # Hapus file setelah dikirim
                os.remove(new_path)

            else:
                await event.reply("⚠️ Pesan tidak berisi media.")

        except Exception as e:
            await event.reply(f"❌ Gagal mengambil: {e}")
    else:
        await event.reply("❌ Kirim link seperti:\nhttps://t.me/c/123456789/456")

client.start()
print("✅ Bot siap menerima pesan...")
client.run_until_disconnected()

import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace these with your actual channel and group usernames
CHANNEL_USERNAME = '@alcyonebots'
GROUP_USERNAME = '@alcyone_support'

# Define the download function
def download_video(url):
    ydl_opts = {
        'cookiefile': 'cookies.txt',  # Update this path as needed
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,  # Prevent playlist downloading
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url)
        video_title = video_info['title']
        file_path = ydl.prepare_filename(video_info)
        ydl.download([url])
    
    return video_title, file_path

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
            InlineKeyboardButton("Join Support", url=f"https://t.me/{GROUP_USERNAME[1:]}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "𝗛𝗶 𝘁𝗵𝗲𝗿𝗲 👋🏻\n"
        "Welcome to 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, your go-to bot for downloading high-quality content from all the top social platforms!! 🎬\n"
        "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
        "◎ Start a chat with @VidDownld_bot and send /start\n"
        "◎ Add me to your group and I'll be there for you for downloading videos\n\n"
        "Join our channel and support group to use the bot\n\n"
        "Let's Get Started 👾",
        reply_markup=reply_markup
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    
    # Check if the URL is from YouTube or Instagram
    if url.startswith("http") and ("youtube.com" in url or "instagram.com" in url):
        try:
            video_title, file_path = download_video(url)
            update.message.reply_text(f'Downloaded: {video_title}')
            with open(file_path, 'rb') as video_file:
                update.message.reply_video(video_file, caption=f'Downloaded: {video_title}')
            
            # Optionally, delete the file after sending
            os.remove(file_path)  # Uncomment if you want to delete the file right after sending.
        except Exception as e:
            # Optional: log the error instead of sending a message
            print(f'Error: {str(e)}')
    # Ignore messages that are not valid links

def main() -> None:
    updater = Updater("7498896975:AAG3RLHaS-9ikHKislaqtcNGqZY29Z1eTlM")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()

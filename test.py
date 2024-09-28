import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler

# Replace these with your actual channel and group usernames
CHANNEL_USERNAME = '@themassacres'
GROUP_USERNAME = '@Reaper_Support'

# Store user membership status
user_membership = {}

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
            InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "𝗦𝗲𝗻𝗱 𝗺𝗲 𝗮 𝗹𝗶𝗻𝗸 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗮 𝘃𝗶𝗱𝗲𝗼 𝗳𝗿𝗼𝗺 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗼𝗿 𝗬𝗼𝘂𝗧𝘂𝗯𝗲...\n\n"
        "𝗕𝗲𝗳𝗼𝗿𝗲 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗲 𝗯𝗼𝘁, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗷𝗼𝗶𝗻 𝘁𝗵𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗮𝗻𝗱 𝘁𝗵𝗲 𝗴𝗿𝗼𝗼𝗽.",
        reply_markup=reply_markup
    )

def update_membership(update: Update) -> None:
    user_id = update.message.from_user.id
    user_membership[user_id] = True  # Set membership status to True when they join

def leave_group(update: Update) -> None:
    user_id = update.chat_member.user.id
    if user_id in user_membership:
        del user_membership[user_id]  # Remove user from membership tracking

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_membership:
        update.message.reply_text(
            "𝗣𝗹𝗲𝗮𝘀𝗲 𝗺𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘁𝗵𝗮𝘁 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗷𝗼𝗶𝗻𝗲𝗱 𝗯𝗼𝘁 𝗴𝗿𝗼𝘂𝗽 𝗮𝗻𝗱 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁."
        )
        return
    
    url = update.message.text
    try:
        video_title, file_path = download_video(url)
        update.message.reply_text(f'𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱: {video_title}')
        with open(file_path, 'rb') as video_file:
            update.message.reply_video(video_file, caption=f'𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱: {video_title}')
        
        # Optionally, delete the file after sending
        os.remove(file_path)
        
    except Exception as e:
        update.message.reply_text(
            f'Error: {str(e)}\n\n'
            "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗼𝗿 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗹𝗶𝗻𝗸 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱..."
        )

def main() -> None:
    updater = Updater("7373160480:AAEg-hW3KrPGxmp7yYroHccHezvsfAQmr1c")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(ChatMemberHandler(leave_group, chat_type='group'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()

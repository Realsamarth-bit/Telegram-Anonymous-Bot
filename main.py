from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from text_handler import handle_text
from media_handler import handle_photo, handle_video, handle_document, handle_sticker, handle_voice, handle_audio, handle_animation, handle_album
from telegram.ext import CallbackContext
from telegram import Update

TOKEN = "YOUR_BOT_TOKEN"

users = {}  # chat_id 
nick_counter = 1000  # for unique nicknames in telegram

def get_nickname(chat_id):
    global nick_counter
    if chat_id not in users:
        nick_counter += 1
        users[chat_id] = f"User{nick_counter}"
    return users[chat_id]

def start(update: Update, context: CallbackContext):
    nickname = get_nickname(update.effective_chat.id)
    update.message.reply_text(f"👋 Welcome {nickname}! Anything you send will be shared anonymously with others.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))

    # Text handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Media handlers
    dp.add_handler(MessageHandler(Filters.photo & Filters.media_group, handle_album))
    dp.add_handler(MessageHandler(Filters.video & Filters.media_group, handle_album))
    dp.add_handler(MessageHandler(Filters.photo & ~Filters.media_group, handle_photo))
    dp.add_handler(MessageHandler(Filters.video & ~Filters.media_group, handle_video))
    dp.add_handler(MessageHandler(Filters.document, handle_document))
    dp.add_handler(MessageHandler(Filters.sticker, handle_sticker))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))
    dp.add_handler(MessageHandler(Filters.audio, handle_audio))
    dp.add_handler(MessageHandler(Filters.animation, handle_animation))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

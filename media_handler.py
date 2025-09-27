from telegram import InputMediaPhoto, InputMediaVideo
from main import users, get_nickname

def broadcast(update, context, msg_type):
    sender_id = update.effective_chat.id
    nickname = get_nickname(sender_id)

    for uid in users:
        if uid != sender_id:
            try:
                if msg_type == "photo":
                    context.bot.send_photo(uid, photo=update.message.photo[-1].file_id,
                                           caption=f"{nickname}: {update.message.caption or ''}")
                elif msg_type == "video":
                    context.bot.send_video(uid, video=update.message.video.file_id,
                                           caption=f"{nickname}: {update.message.caption or ''}")
                elif msg_type == "document":
                    context.bot.send_document(uid, document=update.message.document.file_id,
                                              caption=f"{nickname}: {update.message.caption or ''}")
                elif msg_type == "sticker":
                    context.bot.send_sticker(uid, sticker=update.message.sticker.file_id)
                elif msg_type == "voice":
                    context.bot.send_voice(uid, voice=update.message.voice.file_id,
                                           caption=f"{nickname} sent a voice 🎙")
                elif msg_type == "audio":
                    context.bot.send_audio(uid, audio=update.message.audio.file_id,
                                           caption=f"{nickname}: {update.message.caption or ''}")
                elif msg_type == "animation":
                    context.bot.send_animation(uid, animation=update.message.animation.file_id,
                                               caption=f"{nickname}: {update.message.caption or ''}")
            except Exception as e:
                print(f"Error sending to {uid}: {e}")

# Individual handlers
def handle_photo(update, context): broadcast(update, context, "photo")
def handle_video(update, context): broadcast(update, context, "video")
def handle_document(update, context): broadcast(update, context, "document")
def handle_sticker(update, context): broadcast(update, context, "sticker")
def handle_voice(update, context): broadcast(update, context, "voice")
def handle_audio(update, context): broadcast(update, context, "audio")
def handle_animation(update, context): broadcast(update, context, "animation")

# Media album handler
def handle_album(update, context):
    sender_id = update.effective_chat.id
    nickname = get_nickname(sender_id)

    if not hasattr(context.chat_data, "albums"):
        context.chat_data["albums"] = {}

    media_group = update.message.media_group_id
    if media_group not in context.chat_data["albums"]:
        context.chat_data["albums"][media_group] = []

    if update.message.photo:
        context.chat_data["albums"][media_group].append(
            InputMediaPhoto(update.message.photo[-1].file_id, caption=f"{nickname}: {update.message.caption or ''}")
        )
    elif update.message.video:
        context.chat_data["albums"][media_group].append(
            InputMediaVideo(update.message.video.file_id, caption=f"{nickname}: {update.message.caption or ''}")
        )

    # If at least 2 files, broadcast
    if len(context.chat_data["albums"][media_group]) >= 2:
        for uid in users:
            if uid != sender_id:
                try:
                    context.bot.send_media_group(uid, context.chat_data["albums"][media_group])
                except Exception as e:
                    print(f"Error sending album to {uid}: {e}")
        del context.chat_data["albums"][media_group]


        #FROM THE CREATOR
        #THIS IS DEDICATED PY FOR HANDLING THE MEDIA.

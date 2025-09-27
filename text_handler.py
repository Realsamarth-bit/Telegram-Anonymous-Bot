from main import users, get_nickname

def broadcast(update, context, msg_type="text"):
    sender_id = update.effective_chat.id
    nickname = get_nickname(sender_id)

    for uid in users:
        if uid != sender_id:
            try:
                if msg_type == "text":
                    context.bot.send_message(uid, text=f"{nickname}: {update.message.text}")
            except Exception as e:
                print(f"Error sending to {uid}: {e}")

def handle_text(update, context):
    broadcast(update, context, "text")
# a dedicated text handler for the bot so that the bot can run smoothly if more users try to msg each other

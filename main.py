from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yagmail

# --- Setup Email ---
SENDER_EMAIL = "Ericxuiss@gmail.com"
APP_PASSWORD = "ASHU@8090"  # Use App Password (not your Gmail password)
yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)

# --- Command Handler ---
def send_mail(update, context):
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("Usage: /send target@example.com 'Subject' 'Message'")
            return
        
        target = args[0]
        subject = args[1]
        body = ' '.join(args[2:])
        
        yag.send(to=target, subject=subject, contents=body)
        update.message.reply_text(f"✅ Mail sent to {target}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

def start(update, context):
    update.message.reply_text("Bot ready. Use /send email@example.com 'Subject' 'Message'")

# --- Main ---
def main():
    TOKEN = "7460160224:AAGir3mTTNn0zZ6JnD8mcVnR6RA8mqsO2VI"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("send", send_mail))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()

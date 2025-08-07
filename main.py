import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email config (apna email aur password yahan dalein)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'Ericxuiss@gmail.com'        # sender email
EMAIL_PASSWORD = 'ASHU@8090'        # sender email ka app password ya normal password (gmail ke liye app password use karen)

# States for conversation handler
SUBJECT, SCRIPT, TARGET = range(3)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Hello! Main aapki madad karunga email bhejne mein.\n'
        'Sabse pehle email ka subject bhejein:'
    )
    return SUBJECT

def get_subject(update: Update, context: CallbackContext) -> int:
    context.user_data['subject'] = update.message.text
    update.message.reply_text('Ab email ka script (body) bhejein:')
    return SCRIPT

def get_script(update: Update, context: CallbackContext) -> int:
    context.user_data['script'] = update.message.text
    update.message.reply_text('Target email address bhejein jisko aap mail bhejna chahte hain:')
    return TARGET

def get_target(update: Update, context: CallbackContext) -> int:
    target_email = update.message.text
    subject = context.user_data['subject']
    script = context.user_data['script']

    # Email bhejne ka function call
    try:
        send_email(target_email, subject, script)
        update.message.reply_text(f"Email successfully bhej diya gaya {target_email} ko!")
    except Exception as e:
        update.message.reply_text(f"Kuch error aaya email bhejte waqt: {e}")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancel kar diya gaya. Agar phir se start karna hai to /start type karein.')
    return ConversationHandler.END

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # SMTP connection
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

def main():
    # Apna telegram token yahan dalein
    TOKEN = '7460160224:AAGir3mTTNn0zZ6JnD8mcVnR6RA8mqsO2VI'

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SUBJECT: [MessageHandler(Filters.text & ~Filters.command, get_subject)],
            SCRIPT: [MessageHandler(Filters.text & ~Filters.command, get_script)],
            TARGET: [MessageHandler(Filters.text & ~Filters.command, get_target)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    print("Bot chal raha hai...")
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()

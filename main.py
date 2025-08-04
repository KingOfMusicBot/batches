from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

NSFW_CONTENT = [
    "https://example.com/nsfw1.jpg",
    "https://example.com/nsfw2.jpg"
    # Replace with placeholder or blurred images
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔞 View NSFW Content", callback_data='show_nsfw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! This bot may contain 18+ content. Proceed at your own risk.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'show_nsfw':
        await query.message.reply_text("🔞 Are you 18+? This is sensitive content.")
        for content in NSFW_CONTENT:
            await query.message.reply_photo(content)

# --- Main App Setup ---
app = ApplicationBuilder().token("7833291072:AAG2DxST62b_x7DC9NqWFKc4JrB455kp5Y8").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()

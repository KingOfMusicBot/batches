from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# NSFW Content Placeholder (replace with actual links)
NSFW_CONTENT = [
    "https://example.com/nsfw1.jpg",
    "https://example.com/nsfw2.jpg"
]

# 🚀 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔞 View NSFW Content", callback_data='show_nsfw')],
        [InlineKeyboardButton("📜 Rules", callback_data='show_rules')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Hello *{update.effective_user.first_name}*,\n\n"
        "Welcome to *Rishant's NSFW Vault* 🔐\n\n"
        "⚠️ This bot contains 18+ adult content.\n"
        "Please proceed responsibly and confirm your age below.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 🎯 Button click handling
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'show_nsfw':
        confirm_keyboard = [
            [InlineKeyboardButton("✅ Yes, I'm 18+", callback_data='confirm_18')],
            [InlineKeyboardButton("❌ No, Take Me Back", callback_data='cancel')]
        ]
        await query.edit_message_text(
            "🔞 Are you at least *18 years old*?\nThis content is only for adults!",
            reply_markup=InlineKeyboardMarkup(confirm_keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'confirm_18':
        await query.edit_message_text("✅ Access granted. Enjoy responsibly!")
        for content in NSFW_CONTENT:
            await query.message.reply_photo(content)

    elif query.data == 'cancel':
        await query.edit_message_text("❌ Access denied. Returning to main menu.")
        await start(update, context)

    elif query.data == 'show_rules':
        await query.edit_message_text(
            "📜 *Rules & Guidelines*\n\n"
            "1️⃣ You must be 18+ to use this bot.\n"
            "2️⃣ Don't share sensitive content elsewhere.\n"
            "3️⃣ Use responsibly and avoid misuse.\n\n"
            "_— Rishant's Bot Team_",
            parse_mode="Markdown"
        )

# 🔧 Bot Setup
app = ApplicationBuilder().token("7833291072:AAG2DxST62b_x7DC9NqWFKc4JrB455kp5Y8").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()

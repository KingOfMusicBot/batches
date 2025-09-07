from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Config
API_ID = 28294093
API_HASH = "f24d982c45ab2f69a6cb8c0fee9630bd"
BOT_TOKEN = "8333618251:AAEHeHPBwoVG3BTWtQPHmPA4uvyhy895lk8"

# Group ID where all details will be sent
ADMIN_GROUP = -1002871095336   # <-- replace with your real group id

app = Client("nested_buttons_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Temporary user data store
user_data = {}


# Start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    first = message.from_user.first_name
    text = (
        f"👋 Hello {first}!\n\n"
        "📚 Welcome to *Smart Study Bot*\n\n"
        "✨ Here’s how it works:\n"
        "1️⃣ Select your Platform\n"
        "2️⃣ Choose your Class (8th – Dropper)\n"
        "3️⃣ Send your Batch Name\n"
        "4️⃣ You will receive your batch within 48 hours ✅\n\n"
        "🔔 Note: All your details will be securely shared with our Admin Group."
    )

    # Start Menu with single Platform button
    start_menu = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🌐 Select Platform", callback_data="choose_platform")]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=start_menu
    )


# Platform Menu (2 buttons per row)
def get_platform_menu():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Pw", callback_data="Pw"),
                InlineKeyboardButton("Next Topper", callback_data="Next Topper"),
            ],
            [
                InlineKeyboardButton("Kgs", callback_data="Kgs"),
                InlineKeyboardButton("Unacademy", callback_data="Unacademy"),
            ],
            [
                InlineKeyboardButton("Rwa", callback_data="Rwa"),
                InlineKeyboardButton("Khan Global Studio", callback_data="Khan Global Studio"),
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_to_start"),
            ]
        ]
    )


# Sub Menu (Classes - 2 buttons per row)
def get_sub_menu(platform):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("8th", callback_data=f"{platform}_8th"),
                InlineKeyboardButton("9th", callback_data=f"{platform}_9th"),
            ],
            [
                InlineKeyboardButton("10th", callback_data=f"{platform}_10th"),
                InlineKeyboardButton("11th", callback_data=f"{platform}_11th"),
            ],
            [
                InlineKeyboardButton("12th", callback_data=f"{platform}_12th"),
                InlineKeyboardButton("Dropper", callback_data=f"{platform}_Dropper"),
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="choose_platform")],
        ]
    )


# Callback Query Handler
@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id

    # Open Platform Menu
    if data == "choose_platform":
        await callback_query.message.edit_text(
            "🌐 *Choose Your Learning Platform*\n\n"
            "✨ Select the platform where you are studying.\n"
            "📚 After that, you can choose your class (8th – Dropper).\n\n"
            "👇 Tap on your platform below:",
            reply_markup=get_platform_menu()
        )

    # Platform selected
    elif data in ["Pw", "Next Topper", "Kgs", "Unacademy", "Rwa", "Khan Global Studio"]:
        user_data[user_id] = {"platform": data}
        await callback_query.message.edit_text(
            f"📚 You are now in the *{data}* section!\n\n"
            "✨ Please select your Class below:\n"
            "- Choose from 8th to Dropper.\n"
            "- This will help us assign the correct Batch to you.\n\n"
            "👇 Tap on your class:",
            reply_markup=get_sub_menu(data)
        )

    # Class selected
    elif "_" in data and not data.startswith("back"):
        platform, class_name = data.split("_", 1)
        user_data[user_id]["class"] = class_name

        await callback_query.message.reply_text(
            f"📝 You selected:\n\n"
            f"🏫 Platform: {platform}\n"
            f"📚 Class: {class_name}\n\n"
            f"👉 Please send your *Batch Name* now."
        )

    # Back to Start Menu
    elif data == "back_to_start":
        await callback_query.message.edit_text(
            "👋 Welcome back!\n\n"
            "Click below to select your Platform again:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🌐 Select Platform", callback_data="choose_platform")]]
            )
        )


# Batch Name Handler
@app.on_message(filters.text & ~filters.command("start"))
async def batch_handler(client, message):
    user_id = message.from_user.id

    if user_id in user_data and "class" in user_data[user_id]:
        batch_name = message.text
        platform = user_data[user_id]["platform"]
        class_name = user_data[user_id]["class"]

        # Reply to user with Website button
        await message.reply_text(
            f"✅ Thank you {message.from_user.first_name}!\n\n"
            f"Your batch **{batch_name}** will be provided within 48 hours.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🌐 Visit Our Website", url="https://Studymeta.in")]
                ]
            )
        )

        # Send to Admin Group
        text = (
            f"📢 *New Batch Request*\n\n"
            f"👤 Name: {message.from_user.first_name}\n"
            f"🔗 Username: @{message.from_user.username if message.from_user.username else 'N/A'}\n"
            f"🆔 ID: {message.from_user.id}\n\n"
            f"🏫 Platform: {platform}\n"
            f"📚 Class: {class_name}\n"
            f"📦 Batch: {batch_name}"
        )

        try:
            await app.send_message(ADMIN_GROUP, text)
        except Exception as e:
            print("Error sending to admin group:", e)

        # Clear user data
        user_data.pop(user_id, None)


print("🤖 Bot started...")
app.run()

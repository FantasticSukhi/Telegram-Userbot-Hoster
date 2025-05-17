import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN, ADMIN_IDS
from cloner import clone_userbot

logging.basicConfig(level=logging.INFO)

API_ID, API_HASH, PHONE, SESSION = range(4)
user_data_temp = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /clone to initialize a userbot session.")

async def clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Unauthorized access.")
        return ConversationHandler.END
    await update.message.reply_text("Enter your API_ID:")
    return API_ID

async def get_api_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id] = {'api_id': int(update.message.text)}
    await update.message.reply_text("Enter your API_HASH:")
    return API_HASH

async def get_api_hash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_temp[update.effective_chat.id]['api_hash'] = update.message.text
    await update.message.reply_text("Enter your phone number or session string:")
    return PHONE

async def get_phone_or_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = user_data_temp.get(update.effective_chat.id, {})
    input_val = update.message.text
    
    api_id = data['api_id']
    api_hash = data['api_hash']

    try:
        if len(input_val) > 50:  # Assume it's a session string
            await clone_userbot(api_id, api_hash, session_string=input_val)
        else:
            await clone_userbot(api_id, api_hash, phone=input_val)
        await update.message.reply_text("✅ Userbot cloned successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to initialize userbot: {str(e)}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

app = ApplicationBuilder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("clone", clone)],
    states={
        API_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_id)],
        API_HASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_hash)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_or_session)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)

app.run_polling()

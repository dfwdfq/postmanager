import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL', 'http://localhost:5000')
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Используйте /posts для просмотра постов')

async def posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'{API_URL}/posts')
    posts_data = response.json()
    
    if not posts_data:
        await update.message.reply_text('Постов нет')
        return
    
    keyboard = []
    for post in posts_data:
        keyboard.append([InlineKeyboardButton(post['title'], callback_data=str(post['id']))])
    
    await update.message.reply_text(
        'Выберите пост:',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def post_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    post_id = query.data
    response = requests.get(f'{API_URL}/posts/{post_id}')
    post = response.json()
    
    message = (
        f"{post['title']}\n\n"
        f"{post['created_at']}\n\n"
        f"{post['content']}"
    )
    
    await query.edit_message_text(message)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('posts', posts))
    app.add_handler(CallbackQueryHandler(post_detail))
    
    app.run_polling()

if __name__ == '__main__':
    main() 

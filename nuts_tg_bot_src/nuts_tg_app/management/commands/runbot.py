from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.conf import settings


class Command(BaseCommand):
    help = 'Бот работает вместе с параллельным запуском django сессии'
    
    def handle(self, *args, **options):
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text(f'Hello {update.effective_user.first_name}')
        
        app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot'))
        app.run_polling()
        
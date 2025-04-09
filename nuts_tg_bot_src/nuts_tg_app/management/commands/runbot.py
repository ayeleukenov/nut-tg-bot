import asyncio

from django.core.management.base import BaseCommand
from telegram import Bot
from django.conf import settings


class Command(BaseCommand):
    help = 'Устанавливает webhook на телеграм бот'
    
    def handle(self, *args, **options):
        bot = Bot(token=settings.TELEGRAM_TOKEN)
        
        async def set_webhook_async():
            webhook_url = f'https://{settings.NGROK_DOMAIN}/webhook/'
            success = await bot.set_webhook(webhook_url)
            
            if success:
                self.stdout.write(self.style.SUCCESS(f'Successfully set webhook to {webhook_url}'))
            else:
                self.stdout.write(self.style.ERROR('Failed to set webhook'))
        
        asyncio.run(set_webhook_async())
        
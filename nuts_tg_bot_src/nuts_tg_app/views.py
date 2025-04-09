import json
import asyncio

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from telegram import Update
from telegram.ext import Application, CommandHandler

from accounts_app.models import UserProfileModel 


application = Application.builder().token(settings.TELEGRAM_TOKEN).build()


async def start(update, context):
    await update.message.reply_text(f'Привет Мир')


application.add_handler(CommandHandler("start", start))


async def initialize_application():
    await application.initialize()


asyncio.run(initialize_application())


@csrf_exempt
def webhook_view(request):
    if request.method == 'POST':
        update_json = json.loads(request.body.decode('utf-8'))
        print('update_json is', update_json)
        update = Update.de_json(update_json, application.bot)
        first_name = last_name = username = ''
        if update.effective_user.first_name:
            first_name = update.effective_user.first_name 
        if update.effective_user.last_name:
            last_name = update.effective_user.last_name 
        if update.effective_user.username:
            username = update.effective_user.username
        profile, created = UserProfileModel.objects.get_or_create(
            # user_id=update.effective_user.id,
            username=username,
            defaults={
                'chat_id': update.effective_chat.id,
                'first_name': first_name,
                'last_name': last_name,
                'language_code': update.effective_user.language_code,
            }
        )

        print('command finished')
        return HttpResponse('OK')
    return HttpResponse('Accessed webhook with GET')

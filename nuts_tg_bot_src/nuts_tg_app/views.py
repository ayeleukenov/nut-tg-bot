import json
import asyncio

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from accounts_app.models import UserProfileModel 


application = Application.builder().token(settings.TELEGRAM_TOKEN).build()


async def start(update, context):
    keyboard = [
        [InlineKeyboardButton(
            "Открыть веб-апп", url=f"https://{settings.NGROK_DOMAIN}/chat_id/{update.effective_chat.id}"
            )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    print('this ran when?')
    await update.message.reply_text("Привет Мир", reply_markup=reply_markup)


async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "open_web_app":
        await query.message.reply_text("You selected open_web_app!")


application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_callback))


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
            username=username,
            defaults={
                'chat_id': update.effective_chat.id,
                'first_name': first_name,
                'last_name': last_name,
                'language_code': update.effective_user.language_code,
            }
        )
        asyncio.run(application.process_update(update))

        print('command finished')
        return HttpResponse('OK')
    return HttpResponse('Accessed webhook with GET')


def webapp_view(request):
    return HttpResponse('webapp OK')

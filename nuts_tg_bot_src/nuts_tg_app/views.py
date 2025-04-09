import json
import asyncio

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from accounts_app.models import UserProfileModel 
from nuts_tg_app.models import Category, CategoryItem


application = Application.builder().token(settings.TELEGRAM_TOKEN).build()


async def start(update, context):
    keyboard = [
        [InlineKeyboardButton(
            "Открыть веб-апп", 
            url=f"https://{settings.NGROK_DOMAIN}/chat_id/{
                update.effective_chat.id
                }"
            )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
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

        return HttpResponse('OK')
    return HttpResponse('Accessed webhook with GET')


class UserProfileView(DetailView):
    template_name = 'user_profile_view.html'
    model = get_user_model()
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_items'] = CategoryItem.objects.all()
        context['categories'] = Category.objects.all()
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        chat_id = self.kwargs.get('pk')
        return queryset.get(chat_id=chat_id)
    
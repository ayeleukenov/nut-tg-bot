from django.urls import path
from .views import webhook_view, webapp_view


urlpatterns = [
    path('webhook/', webhook_view, name='tg_webhook'),
    path('chat_id/<int:pk>/', webapp_view, name='webapp_view'),
]

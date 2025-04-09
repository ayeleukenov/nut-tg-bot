from django.urls import path
from .views import webhook_view, UserProfileView


urlpatterns = [
    path('webhook/', webhook_view, name='tg_webhook'),
    path('chat_id/<int:pk>/', UserProfileView.as_view(), name='webapp_view'),
]

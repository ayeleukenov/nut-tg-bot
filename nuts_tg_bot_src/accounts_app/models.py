from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfileModel(AbstractUser):
    chat_id = models.PositiveBigIntegerField(
        default=0,
        verbose_name="Chat ID",
        unique=True,
        null=True,
        blank=True,
    )
    
    is_bot = models.BooleanField(
        default=False,
        verbose_name='Is Bot?',
    )
    
    language_code = models.CharField(
        max_length=3,
        default='ru',
        verbose_name='Lang Code',
    )
    
    selected_items = models.ManyToManyField(
        'nuts_tg_app.CategoryItem',
        blank=True,
        related_name='users',
        verbose_name='Selected Items',
    )
    
    def __str__(self):
        return self.username
    
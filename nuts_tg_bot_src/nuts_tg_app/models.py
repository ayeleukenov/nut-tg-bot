from django.db import models


class Category(models.Model):
    CHOICES = {
        'fruits': 'Фрукты',
        'vegetables': 'Овощи',
        'nuts': 'Орехи',
    }

    name = models.CharField(
        max_length=32,
        choices=CHOICES,
        unique=True,
    )
    
    def __str__(self):
        return self.CHOICES.get(self.name, self.name)
    
    class Meta:
        verbose_name_plural = 'Categories'


class CategoryItem(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        verbose_name='Item Name',
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Category Items'

from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Color(models.Model):
    name = models.CharField('название', unique=True, max_length=50)
    color = ColorField(
        'Цвет в формате HEX',
        unique=True,
        max_length=7,
        help_text='Цветовой HEX-код например, #49B64E'
    )
    price = models.IntegerField('Стоймость цвета', default=0)

    class Meta:
        ordering = ('price', )
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self) -> str:
        return self.color


class User(AbstractUser):
    balance = models.IntegerField('Баланс монет', default=0)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='users')
    passed_tests = models.IntegerField('Пройденые тесты', default=0)

    class Meta:
        ordering = ('-passed_tests', 'username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class PurchasedColors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchased_colors")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='purchased_colors')

    class Meta:
        ordering = ('color', )
        verbose_name = "Купленный цвет"
        verbose_name_plural = "Купленные цвета"
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'color',),
                name='unique_usercolor'
            ),
        )


@receiver(pre_save, sender=User)
def item_discount(sender: User, instance: User, **kwargs: dict) -> User:
    try:
        instance.color
    except ObjectDoesNotExist:
        color = Color.objects.get_or_create(name='Зелёный', color='#008000')
        instance.color = color[0]
    return instance

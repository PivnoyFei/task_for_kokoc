from django.db import models
from users.models import User


class Test(models.Model):
    title = models.CharField("Название теста", max_length=50)
    coin = models.IntegerField("Начислить монет", default=0, help_text="За прохождение теста")
    points = models.IntegerField(
        "Очки",
        default=0,
        help_text="Количество правильных ответов для прохождения теста",
    )
    description = models.CharField(
        "Описание теста",
        max_length=500,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ("created_at", )

    def __str__(self) -> str:
        return self.title[:15]


class Question(models.Model):
    text = models.CharField("Вопрос", max_length=500)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return self.text[:15]


class Answer(models.Model):
    answer = models.CharField("Вариант ответа", max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(verbose_name="Ответ", default=False)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_answer")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="user_answer")
    test_passed = models.BooleanField(verbose_name="Тест пройден", default=False)

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'test',),
                name='unique_usertest'
            ),
        )

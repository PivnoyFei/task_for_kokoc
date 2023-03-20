from http import HTTPStatus as H

from app.models import Answer, Question, Test
from django.test import Client, TestCase
from django.urls import reverse
from users.models import Color, PurchasedColors, User


class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create(username='HasNoName')
        cls.test = Test.objects.create(title='HasNoNameTest', coin=30, points=1)
        cls.question = Question.objects.create(text='NoText', test=cls.test)
        cls.answer = Answer.objects.create(
            answer='NoAnswer', question=cls.question, is_correct=True
        )
        cls.color = Color.objects.create(name='Color_one', color='#749B64', price=10)

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_question(self) -> None:
        """Прохождение деста."""
        user = User.objects.filter(id=self.user.pk)
        assert user[0].passed_tests == 0
        assert user[0].balance == 0

        response = self.authorized_client.post(
            reverse('app:test', args=(self.test.pk, )),
            data={'csrfmiddlewaretoken': '', self.question.pk: [self.answer.pk]},
            follow=True,
        )
        user_after = User.objects.filter(id=self.user.pk)
        assert user[0].passed_tests == 1
        assert user[0].balance == 30

        self.assertEqual(user_after[0].passed_tests, user[0].passed_tests)
        self.assertEqual(user_after[0].balance, user[0].balance)
        self.assertEqual(response.status_code, H.OK)

    def _buy_color(self, num: int) -> None:
        """Вызыветься в < test_fail_buy_color > и < test_ok_buy_color >."""
        count_color = PurchasedColors.objects.filter(user_id=self.user.pk).count()
        assert count_color == 0
        response = self.authorized_client.post(
            reverse('users:buy'),
            data={'color': self.color.pk},
            follow=True,
        )
        count_color = PurchasedColors.objects.filter(user_id=self.user.pk).count()
        assert count_color == num
        self.assertEqual(response.status_code, H.OK)

    def test_fail_buy_color(self) -> None:
        """Неудачная покупка цвета."""
        user = User.objects.filter(id=self.user.pk)
        assert user[0].balance == 0
        self._buy_color(0)

    def test_ok_buy_color(self) -> None:
        """Успешная покупка цвета."""
        User.objects.filter(id=self.user.pk).update(balance=100)
        self._buy_color(1)

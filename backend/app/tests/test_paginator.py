from app.models import Answer, Question, Test
from django.test import Client, TestCase
from django.urls import reverse
from users.models import Color, PurchasedColors, User


class PaginatorViewsTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = [
            User.objects.create(username=f'HasNoName{i}')
            for i in range(13)
        ]
        cls.test = [
            Test.objects.create(title=f'HasNoNameTest{i}', coin=30, points=1)
            for i in range(13)
        ]
        cls.question = [
            Question.objects.create(text='NoText', test=cls.test[i])
            for i in range(13)
        ]
        cls.answer = [
            Answer.objects.create(answer='NoAnswer', question=cls.question[i], is_correct=True)
            for i in range(13)
        ]
        cls.color = [
            Color.objects.create(name=f'Color{i}', color=f'#{i}49B64', price=10)
            for i in range(12)
        ]

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user[0])

    def test_paginator_index_and_users_and_buy(self) -> None:
        """13 тестов, юзеров и цветов в магазине для пагинатора."""
        url_code = {
            reverse('app:index'),
            reverse('users:users'),
            reverse('users:buy')
        }
        for url in url_code:
            print('===', url)
            response = self.authorized_client.get(url)
            self.assertEqual(len(response.context['page_obj']), 5)

            response = self.authorized_client.get(url + '?page=2')
            self.assertEqual(len(response.context['page_obj']), 5)

            response = self.authorized_client.get(url + '?page=3')
            self.assertEqual(len(response.context['page_obj']), 3)

    def test_paginator_profile(self) -> None:
        """13 тестовых цветов в профиле для пагинатора."""
        [PurchasedColors.objects.create(user=self.user[0], color=i) for i in self.color]
        url = reverse('users:profile')

        response = self.authorized_client.get(url)
        self.assertEqual(len(response.context['page_obj']), 5)

        response = self.authorized_client.get(url + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

        response = self.authorized_client.get(url + '?page=3')
        self.assertEqual(len(response.context['page_obj']), 2)

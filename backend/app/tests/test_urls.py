from http import HTTPStatus as H

from app.models import Answer, Question, Test
from django.test import Client, TestCase
from django.urls import reverse
from users.models import User


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create(username='HasNoName')
        cls.test = Test.objects.create(title='HasNoNameTest', coin=30, points=1)
        cls.question = Question.objects.create(text='NoText', test=cls.test)
        cls.answer = Answer.objects.create(
            answer='NoAnswer',
            question=cls.question,
            is_correct=True,
        )

        cls.URL_LOGIN_NEXT = f'/auth/login/?next=/test/{cls.test.pk}/'
        cls.URL_TEST_DETAIL = reverse('app:test', args=(cls.test.pk, ))

        cls.url_status_code = {
            reverse('app:index'): [H.OK, 'app/index.html'],
            reverse('users:signup'): [H.OK, 'users/signup.html'],
            reverse('users:login'): [H.OK, 'users/login.html'],
            reverse('users:profile'): [H.FOUND, 'users/profile.html'],
            reverse('users:users'): [H.FOUND, 'users/user_list.html'],
            reverse('users:buy'): [H.FOUND, 'users/profile.html'],
            cls.URL_TEST_DETAIL: [H.FOUND, 'app/item.html'],
        }

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_guest_client(self) -> None:
        """Проверяем доступность для гостей."""
        for url, code in self.url_status_code.items():
            with self.subTest(code=code):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code, code[0],
                    f'''Страница {url} не найдена'''
                )

    def test_authorized_access(self) -> None:
        """Страница доступна авторизованному пользователю."""
        url_status_code = {
            reverse('users:profile'): H.OK,
            reverse('users:users'): H.OK,
            reverse('users:buy'): H.OK,
            self.URL_TEST_DETAIL: H.OK,
        }
        for url, code in url_status_code.items():
            with self.subTest(code=code):
                response = self.authorized_client.get(url)
                self.assertEqual(
                    response.status_code, code,
                    f'''Страница {url} не найдена'''
                )

    def test_redirect_anonymous(self) -> None:
        """Перенаправление незарегестрированого пользователя."""
        response = self.guest_client.get(self.URL_TEST_DETAIL)
        self.assertRedirects(response, self.URL_LOGIN_NEXT)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.url_status_code.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(
                    response, template[1],
                    f'''Страница {url} для шаблона {template} не найдена'''
                )

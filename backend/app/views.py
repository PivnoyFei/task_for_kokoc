from app.models import Answer, Question, Test, UserAnswer
from app.paginator import paginator_obj
from app.utils import checking_answers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from users.models import User


class TestListView(ListView):
    """Список тестов."""
    model = Test
    paginate_by = 5
    template_name = 'app/index.html'
    context_object_name = 'page_obj'

    def get_queryset(self) -> QuerySet:
        """Поиск по названию теста."""
        if title := self.request.GET.get('search'):
            object_list = self.model.objects.filter(title__icontains=title)
        else:
            object_list = self.model.objects.prefetch_related('questions').all()
        return object_list

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super(TestListView, self).get_context_data(**kwargs)
        context[self.context_object_name] = paginator_obj(self.request, context['object_list'])
        return context


class QuestionView(LoginRequiredMixin, View):
    """Начало теста. Пользователь получает список вопросов с вариантами ответов."""

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """Если тест уже пройден, уведомляет пользователи."""
        test = get_object_or_404(Test, pk=kwargs['pk'])
        user_answer = UserAnswer.objects.filter(user=request.user, test=test)
        if user_answer.exists():
            return render(request, 'app/result.html', context={'bool_answer': True})

        questions = Question.objects.prefetch_related('answers').filter(test=test)
        context = {'obj': questions, 'test': test}
        return render(request, 'app/item.html', context=context)

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """Если тест пройден, сохраняет статус и начисляет монеты пользователю."""
        answers = request.POST.copy()
        answers.pop('csrfmiddlewaretoken')

        questions = (
            Question.objects.filter(test_id=kwargs['pk'])
            .prefetch_related(
                Prefetch('answers', Answer.objects.filter(is_correct=True), 'correct_answer')
            )
        )
        bool_answer, count_answers, count_answers_user = checking_answers(questions, answers)
        if bool_answer:
            UserAnswer.objects.get_or_create(
                user=request.user,
                test=questions[0].test,
                test_passed=bool_answer,
            )
            User.objects.filter(id=request.user.id).update(
                balance=F('balance') + questions[0].test.coin,
                passed_tests=F('passed_tests') + 1,
            )
        context = {
            'count_correct_answers_user': count_answers_user,
            'count_correct_answers': count_answers,
            'bool_answer': bool_answer,
            'test_pk': kwargs['pk'],
        }
        return render(request, 'app/result.html', context=context)

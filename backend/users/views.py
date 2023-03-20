from app.paginator import paginator_obj
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from users.forms import CreationForm
from users.models import Color, PurchasedColors, User


class SignUp(CreateView):
    """Регистрация пользователя."""
    form_class = CreationForm
    success_url = reverse_lazy('pay:index')
    template_name = 'users/signup.html'


class UserListView(LoginRequiredMixin, ListView):
    """Показывать список пользователей и количество пройденных тестов."""
    model = User
    paginate_by = 5
    template_name = 'users/user_list.html'
    context_object_name = 'page_obj'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super(UserListView, self).get_context_data(**kwargs)
        context[self.context_object_name] = paginator_obj(self.request, context['object_list'])
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    model = Color
    paginate_by = 5
    template_name = 'users/profile.html'
    context_object_name = 'page_obj'

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """
        Проверяет наличие М2М связи, цвета и юзера.
        Если цвета нет, оформляет покупку цвета, если есть, просто меняет цвет профиля.
        """
        color_id = request.POST.get('color', None)
        color = get_object_or_404(Color, id=color_id)

        if self.request.path == '/profile/':
            purchased_colors = get_object_or_404(PurchasedColors, user=request.user, color=color)
            if purchased_colors and color != request.user.color:
                User.objects.filter(id=request.user.id).update(color=color)

        if self.request.path == '/buy/':
            if request.user.balance >= color.price:
                purchased_colors = PurchasedColors.objects.get_or_create(
                    user=request.user,
                    color=color,
                )

                if not purchased_colors[1] and color != request.user.color:
                    User.objects.filter(id=request.user.id).update(color=color)

                elif purchased_colors[1]:
                    User.objects.filter(id=request.user.id).update(
                        balance=request.user.balance - color.price,
                        color=color,
                    )
        return redirect("users:profile")

    def get_queryset(self) -> QuerySet:
        """
        /profile/ - Список приобретенных цветов.
        /buy/ - Список цветов к покупке которых нет у пользователя.
        """
        if self.request.path == '/profile/':
            return PurchasedColors.objects.select_related('color').filter(user=self.request.user)
        if self.request.path == '/buy/':
            return Color.objects.filter(
                ~Q(id__in=PurchasedColors.objects.filter(user=self.request.user)
                   .values_list('color_id'))
            )

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context[self.context_object_name] = paginator_obj(self.request, context['object_list'])
        return context

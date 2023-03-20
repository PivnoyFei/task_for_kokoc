from app.models import Answer, Question, Test
from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedTabularInline
from quiz.settings import VALUE_DISPLAY
from users.models import Color, User


class Answerline(NestedTabularInline):
    model = Answer
    min_num = 2
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'test', )
    search_fields = ('test', )
    inlines = (Answerline, )
    empty_value_display = VALUE_DISPLAY


class Questionline(NestedTabularInline):
    model = Question
    inlines = (Answerline,)
    min_num = 1
    extra = 1


@admin.register(Test)
class TestAdmin(NestedModelAdmin):
    list_display = ('id', 'title', 'description', 'coin', 'points', 'created_at', )
    readonly_fields = ('created_at', )
    search_fields = ('title', )
    inlines = (Questionline, )
    empty_value_display = VALUE_DISPLAY


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'price', )
    empty_value_display = VALUE_DISPLAY


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'last_login', 'is_staff', )
    readonly_fields = (
        'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name',
        'email', 'balance', 'color', 'passed_tests', 'date_joined', 'username',
    )
    empty_value_display = VALUE_DISPLAY

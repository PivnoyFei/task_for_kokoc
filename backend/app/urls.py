from app import views
from django.urls import path

app_name = 'pay'

urlpatterns = [
    path('', views.TestListView.as_view(), name='index'),
    path('test/<int:pk>/', views.QuestionView.as_view(), name='test'),
]

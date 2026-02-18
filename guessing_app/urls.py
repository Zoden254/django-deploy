from django.urls import path
from . import views

app_name = 'guessing_app'
urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name='home'),
    path('questions/', views.QuestionsList.as_view(), name='questions_list'),
    path('questions/<str:category>/', views.category_questions, name="category_questions"),
    path('questions/<str:category>/<int:id>/', views.question_detail, name='question_detail'),
    path('questions/<str:category>/game/', views.game, name='game'),
    path('questions/<str:category>/game/result/', views.submitted, name='result'),
    path('questions/<str:category>/game/result/complete/', views.complete, name='complete'),
    path('history/', views.HistoryListView.as_view(), name='history'),
]
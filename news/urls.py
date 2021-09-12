from django.urls import path
from .views import PostsList, PostDetail

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
]

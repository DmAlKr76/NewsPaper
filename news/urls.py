from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostAdd, PostEdit, PostDelete

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('add/', PostAdd.as_view(), name='news_add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

]

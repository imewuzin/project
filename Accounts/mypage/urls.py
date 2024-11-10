from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    # 
    path('', views.mypage, name='mypage'),
    path('favorite-users/', views.favorite_users_list, name='favorite_users_list'),
    path('liked-todos/', views.liked_todos_list, name='liked_todos_list'),
    path('toggle-favorite/<int:user_id>/', views.toggle_favorite_user, name='toggle_favorite_user'),
]
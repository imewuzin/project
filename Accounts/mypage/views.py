# from django.conf import settings
# from django.contrib.auth import logout
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from django.utils import timezone

# from accounts.models import User
# from todo.models import Todo   # 투두 모델 만들어야
# from .models import BookmarkUser

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Todo

# class MyPageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
        
#         try:
#             # 사용자 기본 정보
#             user_info = {
#                 'profile_image': user.profile_img,
#                 'nickname': user.nickname,
#                 'join_date': user.date_joined,
#                 'todo_count': Todo.objects.filter(user=user).count()
#             }
            
#             # 내가 작성한 투두 리스트
#             my_todos = Todo.objects.filter(user=user).order_by('-created_at')
#             my_todos_data = [{
#                 'id': todo.id,
#                 'content': todo.content,
#                 'created_at': todo.created_at,
#                 'is_completed': todo.is_completed if hasattr(todo, 'is_completed') else False
#             } for todo in my_todos]
            
#             # 좋아요한 투두 리스트
#             liked_todos = Todo.objects.filter(likes=user).order_by('-created_at')
#             liked_todos_data = [{
#                 'id': todo.id,
#                 'content': todo.content,
#                 'created_at': todo.created_at,
#                 'author': todo.user.nickname,
#                 'author_profile': todo.user.profile_img
#             } for todo in liked_todos]
            
#             # 즐겨찾기한 유저 정보
#             bookmarked_users = BookmarkUser.objects.filter(user=user)
#             bookmarked_users_data = []
            
#             for bookmark in bookmarked_users:
#                 bookmarked_user = bookmark.bookmarked_user
#                 latest_todo = Todo.objects.filter(user=bookmarked_user).order_by('-created_at').first()
                
#                 bookmarked_users_data.append({
#                     'id': bookmarked_user.id,
#                     'profile_image': bookmarked_user.profile_img,
#                     'nickname': bookmarked_user.nickname,
#                     'todo_count': Todo.objects.filter(user=bookmarked_user).count(),
#                     'latest_todo': {
#                         'id': latest_todo.id,
#                         'content': latest_todo.content,
#                         'created_at': latest_todo.created_at
#                     } if latest_todo else None
#                 })
            
#             return Response({
#                 'user_info': user_info,
#                 'my_todos': my_todos_data,
#                 'liked_todos': liked_todos_data,
#                 'bookmarked_users': bookmarked_users_data
#             }, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             return Response({
#                 'error': str(e)
#             }, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             logout(request)
#             return Response({
#                 'message': '로그아웃되었습니다.'
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({
#                 'error': str(e)
#             }, status=status.HTTP_400_BAD_REQUEST)

# class BookmarkUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         try:
#             target_user = get_object_or_404(User, id=user_id)
            
#             if request.user == target_user:
#                 return Response({
#                     'message': '자신을 즐겨찾기할 수 없습니다.'
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             bookmark, created = BookmarkUser.objects.get_or_create(
#                 user=request.user,
#                 bookmarked_user=target_user
#             )
            
#             if not created:
#                 bookmark.delete()
#                 return Response({
#                     'message': '즐겨찾기가 취소되었습니다.'
#                 }, status=status.HTTP_200_OK)
            
#             return Response({
#                 'message': '즐겨찾기에 추가되었습니다.'
#             }, status=status.HTTP_201_CREATED)
            
#         except Exception as e:
#             return Response({
#                 'error': str(e)
#             }, status=status.HTTP_400_BAD_REQUEST)



@login_required
def mypage(request):
    user = request.user
    todos = Todo.objects.filter(user=user)
    liked_todos = user.liked_todos.all()
    favorite_users = user.favorites.all()
    context = {
        'user': user,
        'todos': todos,
        'liked_todos': liked_todos,
        'favorite_users': favorite_users,
    }
    return render(request, 'mypage/mypage.html', context)

@login_required
def favorite_users_list(request):
    favorite_users = request.user.favorites.all()
    return render(request, 'mypage/favorite_users.html', {'favorite_users': favorite_users})

@login_required
def liked_todos_list(request):
    liked_todos = request.user.liked_todos.all()
    return render(request, 'mypage/liked_todos.html', {'liked_todos': liked_todos})

@login_required
def toggle_favorite_user(request, user_id):
    user_to_favorite = get_object_or_404(CustomUser, id=user_id)
    if user_to_favorite in request.user.favorites.all():
        request.user.favorites.remove(user_to_favorite)
        favorited = False
    else:
        request.user.favorites.add(user_to_favorite)
        favorited = True
    return JsonResponse({'status': 'success', 'favorited': favorited})
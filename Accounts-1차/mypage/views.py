# mypage/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import Ttodo, TtodoLike
from .serializers import TodoSerializer, LikedTodoSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage_view(request):
    user = request.user
    
    # 내 투두 리스트
    my_todos = Ttodo.objects.filter(user=user)
    
    # 내가 좋아요한 투두 리스트
    liked_todos = Ttodo.objects.filter(likes__user=user)
    
    data = {
        'profile': {
            'nickname': user.nickname,
            'profile_img': user.profile_img,
            'social_type': user.social,
            'created_date': user.created_date,
            'todo_count': my_todos.count(),
        },
        'my_todos': TodoSerializer(my_todos, many=True, context={'request': request}).data,
        'liked_todos': LikedTodoSerializer(liked_todos, many=True).data,
        'bookmarked_users': [
            {
                'id': friend.id,
                'nickname': friend.nickname,
                'profile_img': friend.profile_img,
                'todo_count': Ttodo.objects.filter(user=friend).count(),
                'latest_todo': TodoSerializer(
                    Ttodo.objects.filter(user=friend).first(),
                    context={'request': request}
                ).data if Ttodo.objects.filter(user=friend).exists() else None
            }
            for friend in user.friend_list.all()
        ]
    }
    
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, todo_id):
    todo = get_object_or_404(Ttodo, id=todo_id)
    like, created = TtodoLike.objects.get_or_create(user=request.user, ttodo=todo)
    
    if not created:
        like.delete()
        return Response({'message': '좋아요가 취소되었습니다.'})
    
    return Response({'message': '좋아요가 추가되었습니다.'})
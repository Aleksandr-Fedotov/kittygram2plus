from rest_framework import viewsets
from rest_framework.throttling import ScopedRateThrottle

from .models import Achievement, Cat, User
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .permissions import OwnerOrReadOnly  # , ReadOnly
from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    """
    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
    """
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (ScopedRateThrottle, WorkingHoursRateThrottle)
    # Для любых пользователей установим кастомный лимит 1 запрос в минуту
    throttle_scope = 'low_request'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

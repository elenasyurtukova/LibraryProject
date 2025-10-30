from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from users.models import User
from users.serializers import UserSerializer


class UserCreateApiView(CreateAPIView):
    """Класс контроллера для создания пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (
        AllowAny,
    )  # для этого контроллера доступ для всех неавторизованных пользователей

    def perform_create(self, serializer):
        """Функция хеширования пароля пользователя для безопасности"""
        user = serializer.save(is_active=True)
        user.set_password(
            user.password
        )
        user.save()


class UserListApiView(ListAPIView):
    """Класс контроллера для вывода списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserRetrieveApiView(RetrieveAPIView):
    """Класс контроллера для вывода экземпляра пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """метод отображения заданного пользователя"""
        return User.objects.filter(pk=self.request.user.pk)



class UserUpdateApiView(UpdateAPIView):
    """Класс контроллера для изменения экземпляра пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """метод отображения заданного пользователя"""
        return User.objects.filter(pk=self.request.user.pk)


class UserDestroyApiView(DestroyAPIView):
    """Класс контроллера для удаления экземпляра пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

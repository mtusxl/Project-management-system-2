from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from Project_Management_System.Users.models import User

from .models import Notification, NotificationSettings
from .serializer import NotificationSerializer, NotificationSettingsSerializer


#  GET /api/notifications/ - список уведомлений пользователя
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            user = get_list_or_404(Notification, recipient=user_id)
            return Notification.objects.filter(recipient=user)
        user = self.request.user
        return Notification.objects.filter(recipient=user)


# PUT /api/notifications/{id}/read/ - отметить уведомление прочитанным
class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = self.request.user
        return Notification.objects.filter(user=user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if not instance.is_read:
            instance.is_read = True
            instance.save()
        return Response(
            {"status": "Уведомление отмечено прочитанным"}, status=status.HTTP_200_OK
        )


#  DELETE /api/notifications/{id}/ - удалить уведомление
class NotificationDeleteView(generics.DestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]
    queryset = Notification.objects.all()


# GET /api/notifications/settings/ - настройки уведомлений пользователя
class AdminNotificationSettingsView(generics.ListAPIView):
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            return NotificationSettings.objects.filter(id=user_id)

        return NotificationSettings.objects.filter(user=user_id)


# PUT /api/notifications/settings/ - обновление настроек уведомлений
class AdminNotificationSettingsUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = self.request.user
        obj, created = NotificationSettings.objects.get_or_create(user=user)
        return obj


# GET /api/notification-preferences/ - получение настроек (только свои)
class ClientNotificationPreferencesView(generics.RetrieveAPIView):
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, created = NotificationSettings.objects.get_or_create(user=self.request.user)
        return obj


# PUT /api/notification-preferences/ - обновление настроек (только свои)
class ClientNotificationPreferencesUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, created = NotificationSettings.objects.get_or_create(user=self.request.user)
        return obj

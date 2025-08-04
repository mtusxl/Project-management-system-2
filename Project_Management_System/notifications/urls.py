from django.urls import path

from .views import (
    AdminNotificationSettingsUpdateView,
    AdminNotificationSettingsView,
    ClientNotificationPreferencesUpdateView,
    ClientNotificationPreferencesView,
    NotificationDeleteView,
    NotificationListView,
    NotificationMarkReadView,
)

urlpatterns = [
    # Админ-часть
    path("api/notifications/", NotificationListView.as_view(), name="notification-list"),
    path(
        "api/notifications/<int:pk>/read/",
        NotificationMarkReadView.as_view(),
        name="notification-mark-read",
    ),
    path(
        "api/notifications/<int:pk>/",
        NotificationDeleteView.as_view(),
        name="notification-delete",
    ),
    path(
        "api/notifications/settings/",
        AdminNotificationSettingsView.as_view(),
        name="admin-notification-settings-get",
    ),
    path(
        "api/notifications/settings/",
        AdminNotificationSettingsUpdateView.as_view(),
        name="admin-notification-settings-put",
    ),
    # Клиентская часть
    path(
        "api/notification-preferences/",
        ClientNotificationPreferencesView.as_view(),
        name="client-notification-preferences-get",
    ),
    path(
        "api/notification-preferences/",
        ClientNotificationPreferencesUpdateView.as_view(),
        name="client-notification-preferences-put",
    ),
]

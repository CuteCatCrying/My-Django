from django.urls import path
from .views import DashboardView, ProfileView, NotificationView, ListUserView, ListNotificationView, logoutView

app_name = 'dashboard'
urlpatterns = [
    path('notification/', NotificationView.as_view(), name='notification'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list-user/', ListUserView.as_view(), name='list-user'),
    path('list-notification/', ListNotificationView.as_view(), name='list-notification'),
    path('logout/', logoutView, name='logout'),
    path('', DashboardView.as_view(), name='index'),
]
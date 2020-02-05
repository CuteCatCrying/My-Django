from django.urls import path
from .views import IndexView, SignUpFormView, loginView

app_name = 'pendaftaran'

urlpatterns = [
    path('login/', loginView, name='login'),
    path('signup/', SignUpFormView.as_view(), name='signup'),
    path('', IndexView.as_view(), name='index'),
]
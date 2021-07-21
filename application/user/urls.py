from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create', views.CreateUserView.as_view(), name='create-user'),
    path('token', views.CreateAuthTokenView.as_view(), name='token'),
    path('profile', views.RudManagerUserView.as_view(), name='user-profile'),
]

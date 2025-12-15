from django.urls import path
from .views import UserRegisterAPIView, UserLoginAPIView, UserView, LogoutView, UserListsView

app_name='accounts'

urlpatterns = [

    path('register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('user/', UserView.as_view(), name='user_view'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('user_list/', UserListsView.as_view(), name='user_list'),

]

from django.urls import path

from .views import UserRegisterAPIView, UserLoginAPIView, UserAPIView, LogoutAPIView, UserListsAPIView, \
        CreateUserAPIView, UpdateUserAPIView, DetailUserAPIView  

app_name='accounts'

urlpatterns = [

    path('register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('user/', UserAPIView.as_view(), name='user_view'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
    path('user_list/', UserListsAPIView.as_view(), name='user_list'),

    path('create/user/', CreateUserAPIView.as_view(), name='create_user'),
    path('update/user/<int:user_id>/', UpdateUserAPIView.as_view(), name='update_user'),
    path('detail/user/<int:user_id>/', DetailUserAPIView.as_view(), name='detail_user'),

]

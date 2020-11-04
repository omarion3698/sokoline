<<<<<<< HEAD
from .views import RegisterAPI, UserProfileAPI
from knox import views as knox_views
=======
from .views import RegisterAPI, LoginAPI, UserAPI, ChangePasswordView
>>>>>>> 785504072747c02cb84bdca0cfb27bf61dd41302
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
<<<<<<< HEAD
    path('api/users/<user_id>/profile/', UserProfileAPI.as_view()),

=======
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
>>>>>>> 785504072747c02cb84bdca0cfb27bf61dd41302
]
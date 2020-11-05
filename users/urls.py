from .views import UserProfileAPI
from knox import views as knox_views
from django.urls import path, include
from . import views
from knox import views as knox_views


urlpatterns = [
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/users/<user_id>/profile/', UserProfileAPI.as_view()),
    re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
    path('<int:id>/details/', users_details, name="users_details"),
    path('<int:id>/edit/', users_edit, name="users_edit"),
    path('add/', users_add, name="users_add"),
    path('<int:id>/delete/', users_delete, name="users_delete"),

]

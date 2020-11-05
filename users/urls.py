from .views import RegisterAPI, UserProfileAPI, LoginAPI, UserAPI, ChangePasswordView
from knox import views as knox_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/users/<user_id>/profile/', UserProfileAPI.as_view()),
    re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
    path('<int:id>/details/', users_details, name="users_details"),
    path('<int:id>/edit/', users_edit, name="users_edit"),
    path('add/', users_add, name="users_add"),
    path('<int:id>/delete/', users_delete, name="users_delete"),
    
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
	# path('simple-checkout/', views.simpleCheckout, name="simple-checkout"),
    # path('', views.store, name="store"),
    # path('checkout/<int:pk>/', views.checkout, name="checkout"),
    # path('complete/', views.paymentComplete, name="complete"),
    # path('products/', views.products, name='products'),
    # path('customer/<str:pk_test>/', views.customer, name="customer"),
    # path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    # path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    # path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]

from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'uers', views.UserViewSet)

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'soko-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import views


router = DefaultRouter()
router.register(r'repositories', views.RepositoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import views


router = DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'products', views.ProductViewSet, 'product')
router.register(r'packages', views.PackageViewSet)
router.register(r'dependencies', views.DependencyViewSet)
router.register(r'builds', views.BuildViewSet)
router.register(r'deployments', views.DeploymentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

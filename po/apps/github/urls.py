from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import views


router = DefaultRouter()
router.register(r'repositories', views.RepositoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/add-repo-to-product/$',
        views.AddRepoToProductFormView.as_view(),
        name='add_repo_to_product'),
]

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.product_query_form, name='index'),
]

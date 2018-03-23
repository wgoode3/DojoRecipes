from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.index),
    url(r'^recipe$', views.recipe),
    url(r'^like/(?P<recipe_id>\d+)$', views.like)
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>", views.article, name="article"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("<str:query>/results", views.index, name="results")
]

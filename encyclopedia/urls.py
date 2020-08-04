from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name="article"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/<str:title>/editconfirm", views.editconfirm, name="editconfirm")
]

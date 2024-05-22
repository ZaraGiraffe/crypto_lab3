from django.urls import path

from . import views

urlpatterns = [
    path("test/", views.test),
    path("get/", views.get_message),
    path("send/", views.send_message)
]

from django.urls import path
from . import views

app_name = "video_rental"

urlpatterns = [
    path("", views.video_list, name="video_list"),
    path("create/", views.video_create, name="video_create"),
    path("update/<int:pk>/", views.video_update, name="video_update"),
    path("delete/<int:pk>/", views.video_delete, name="video_delete"),
]

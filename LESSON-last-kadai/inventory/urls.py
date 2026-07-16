from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/inventory/items/ に対応
    path("items/", views.item_list, name="item_list"),
]

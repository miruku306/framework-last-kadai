from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.staff_list, name="staff_list"),
    path("user/<int:user_id>/", views.staff_detail, name="staff_detail"),
    path("new/", views.employee_create, name="employee_create"),
    path("portal/edit/<int:user_id>/", views.employee_update, name="employee_update"),
    path("portal/delete/<int:user_id>/", views.employee_delete, name="employee_delete"),
]

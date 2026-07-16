from django.contrib import admin

# Register your models here.
from .models import Employee

# admin.site.register(Employee)  # Employeeモデルを管理サイトに登録


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "dept", "role", "joined_date")  # 表示したいフィールド


admin.site.register(Employee, EmployeeAdmin)

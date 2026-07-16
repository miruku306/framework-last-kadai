from .models import Employee
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from django.shortcuts import render, redirect, get_object_or_404


# 一覧ページ用
def staff_list(request):
    members = Employee.objects.all().order_by("-joined_date")
    return render(request, "staff/list.html", {"members": members})


# 詳細ページ用
def staff_detail(request, user_id):
    # user_idが一致する人を1人探す
    members = Employee.objects.all()
    user = next((s for s in members if s.id == user_id), None)
    return render(request, "staff/detail.html", {"user": user})


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff_list")  # urls.pyで決めた名前を指定
    else:
        form = EmployeeForm()

    return render(request, "staff/employee_form.html", {"form": form})


def employee_update(request, user_id):
    # 1. 編集したいデータをDBから1件取り出す
    user = get_object_or_404(Employee, id=user_id)

    if request.method == "POST":
        # 2. 既存データ(instance)をベースに、送られてきたデータで上書き
        form = EmployeeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("staff_list")
    else:
        # 3. 最初は既存データが入った状態のフォームを表示
        form = EmployeeForm(instance=user)

    return render(request, "staff/employee_form.html", {"form": form})


def employee_delete(request, user_id):
    user = get_object_or_404(Employee, id=user_id)
    if request.method == "POST":
        user.delete()  # データを削除
        return redirect("staff_list")

    # GETの時は確認画面を表示
    return render(request, "staff/employee_confirm_delete.html", {"user": user})

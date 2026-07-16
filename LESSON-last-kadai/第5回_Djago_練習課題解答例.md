
# 第5回 練習課題 解答例：社員名簿システム

## 1. フォームの定義 (`staff/forms.py`)
`ModelForm` を使って、モデルから入力を自動生成します。

```python
# staff/forms.py
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # 全ての項目を入力対象にする
        fields = ['name', 'dept', 'role', 'email', 'joined_date']

        # 【発展】入社日の入力欄をカレンダーにするための設定
        widgets = {
            'joined_date': forms.DateInput(attrs={'type': 'date'}),
        }
```

---

## 2. ビューの実装 (`staff/views.py`)
「画面を表示する(GET)」と「保存する(POST)」を1つの関数で切り分けます。

```python
# staff/views.py
from django.shortcuts import render, redirect
from .forms import EmployeeForm

def employee_create(request):
    # 1. ユーザーが「登録」ボタンを押してデータが送られてきた場合（POST）
    if request.method == 'POST':
        # 送られてきたデータ(request.POST)をフォームに詰め込む
        form = EmployeeForm(request.POST)

        # データが正しいかチェック（バリデーション）
        if form.is_valid():
            form.save()         # データベースへ保存！
            return redirect('staff_list') # 保存後は一覧ページへ転送

    # 2. 最初にページを開いた場合（GET）
    else:
        # 中身が空のフォームを用意する
        form = EmployeeForm()

    # どちらの場合も同じHTMLを表示（エラーがある場合はエラー付きのformが表示される）
    return render(request, 'staff/employee_form.html', {'form': form})
```

---

## 3. URLの設定 (`staff/urls.py`)
新しいURL `/portal/new/` を追加します。

```python
# staff/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.staff_list, name='staff_list'),
    path('user/<int:user_id>/', views.staff_detail, name='staff_detail'),
    # 新規登録のURL
    path('new/', views.employee_create, name='staff_create'),
]
```

---

## 4. テンプレートの実装 (`templates/staff/employee_form.html`)
CSRF対策（お守り）を忘れずに記述します。

```html
{% extends 'base.html' %}

{% block content %}
<h2>新規社員登録</h2>

<!-- データを送る(POST)ための設定 -->
<form method="POST">
    {% csrf_token %} <!-- セキュリティの合言葉（必須！） -->

    {{ form.as_p }} <!-- フォームをPタグ形式で自動表示 -->

    <button type="submit">この内容で登録する</button>
</form>

<hr>
<p><a href="{% url 'staff_list' %}">キャンセルして一覧に戻る</a></p>
{% endblock %}
```

---

## 5. 一覧ページにボタンを追加 (`templates/staff/list.html`)
ユーザーがわざわざURLを打たなくても登録画面へ飛べるようにします。

```html
{% extends 'base.html' %}
{% block content %}
<h1>社員名簿一覧</h1>

<!-- 登録画面へのリンクボタン -->
<p><a href="{% url 'staff_create' %}">＋新規社員登録</a></p>

<table>
    <!-- テーブルの中身は前回と同じ... -->
</table>
{% endblock %}
```

---

## 解説

1.  **`redirect` の使い道** :
    保存が成功した後、そのまま `render` で同じページを出すのではなく、`redirect` で別のページに飛ばすのがWebのルールです。これによって、ブラウザで「再読み込み」した時に二重にデータが登録されるのを防ぎます。
2.  **`is_valid()` の活用** :
    `forms.py` で `joined_date` を設定しているので、日付以外の文字を入力して送信すると、Djangoが自動的に検知して「有効な日付を入力してください」というエラーを出してくれます。
3.  **CSRFトークン** :
    もしこれがないと、Djangoは「悪いサイトからの攻撃かもしれない」と判断してデータを拒否します。必ず書きましょう。

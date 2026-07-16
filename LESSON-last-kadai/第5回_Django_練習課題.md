

---

# 第5回 実習指示書：社員名簿システム
**新規社員登録フォームの実装**

## 1. 開発ミッション
前回データベース化した「社員名簿システム」に、ブラウザから新しい社員を登録できる　**新規登録機能（Create）**　を追加してください。

> [!IMPORTANT]
> **環境の確認：** 実習用のプロジェクト（コンテナ）に切り替えて作業してください。
>
> この課題は第４回の練習課題完成後が必要です。
>
> 第４回は提出前なのでコードを保存するか新たにコンテナを作って作業しましょう。
>
> この課題は成績対象ではありませんが、今後の課題で必要になることがあります。
---

## 2. 要件定義（仕様書）

### ① フォームの定義
*   `staff/forms.py` を新規作成し、`Employee` モデルに基づいた **`EmployeeForm`** を作成すること。
*   入力項目には、`name`, `dept`, `role`, `email`, `joined_date` の全てを含めること。

### ② 新規登録機能（View & URL）
*   **URL**: `/portal/new/` で登録画面が表示されるようにすること。
*   **View**: `EmployeeForm` を使い、以下の挙動を実装すること。
    *   **GET時**: 空のフォームを表示する。
    *   **POST時**: 送信されたデータをバリデーション（入力チェック）し、問題がなければ保存する。
    *   **保存後**: 社員一覧ページ（`/portal/list/`）に自動的にリダイレクト（転送）させること。

### ③ テンプレートの実装
*   `templates/staff/employee_form.html` を作成し、`base.html` を継承すること。
*   フォームを表示する際、セキュリティ対策の **`{% csrf_token %}`** を必ず記述すること。
*   「登録する」ボタンと「キャンセル（一覧に戻る）」リンクを設置すること。

### ④ リンクの追加
*   社員一覧ページ（`list.html`）のタイトル付近に、**「＋新規社員登録」** というリンクを作成し、スムーズに登録画面へ移動できるようにすること。

---

## 3. 実装のヒント

### Viewの基本構造
保存処理を書くときは、`if request.method == 'POST':` を使って、「画面を表示したいだけなのか」「データが送られてきたのか」を判別します。

```python
from django.shortcuts import render, redirect
from .forms import EmployeeForm

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list') # urls.pyで決めた名前を指定
    else:
        form = EmployeeForm()

    return render(request, 'staff/employee_form.html', {'form': form})
```

### CSRFトークンの書き忘れに注意！
これがないと、データを送信した瞬間に **「403 Forbidden」** エラーが発生します。

```html
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">登録する</button>
</form>
```

---

## 4. 発展課題（時間が余った人へ）

1.  **カレンダー入力の導入**　: `joined_date`（入社日）の入力欄を、クリックするとカレンダーが出るように工夫してみよう。（`forms.py` で `widgets` を設定）
2.  **成功メッセージ**　: 登録が完了した際、一覧ページの上部に「〇〇さんを登録しました」と表示されるようにしてみよう（Djangoの `messages` フレームワークを調査）。
3.  **入力エラーの表示**　: フォームのバリデーションに失敗した際（メールアドレスの形式が変など）、どこが間違っているか赤文字で表示されるようにしてみよう。

---

## 5. 成果物チェックリスト
提出前に以下の項目を確認してください。

- [ ] ブラウザの `/portal/new/` からデータを入力して保存できるか？
- [ ] 保存した後、自動的に一覧ページに戻るか？
- [ ] 保存したデータが、一覧ページの一番下（または上）に表示されているか？
- [ ] 管理画面（`/admin/`）を開いたとき、登録したデータが正しく保存されているか？

---

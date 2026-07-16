実習（個人制作：社員名簿システム）を完成させるための**最短操作手順書**です。
迷ったらこの手順通りに進めてください。

---

# 実習：社員名簿システムの実装手順

### STEP 1：アプリの作成と登録
まず、社員名簿専用の「部屋（アプリ）」を作ります。

1.  **ターミナル**（VS Code下部）で以下のコマンドを実行。
    ```bash
    python manage.py startapp staff
    ```
2.  `myproject/settings.py` を開き、`INSTALLED_APPS` のリストに `'staff',` を追記する。
    ```python
    INSTALLED_APPS = [
        ...
        'inventory',
        'staff',  # ← 追加！
    ]
    ```

---

### STEP 2：データと命令を作る（View）
社員のデータを用意し、画面に渡す命令を書きます。

1.  `staff/views.py` を開き、中身を以下のように書き換える。
    ```python
    from django.shortcuts import render

    # 実習用データ
    STAFF_MEMBERS = [
        {'id': 1, 'name': '山田 太郎', 'dept': '営業部', 'role': 'マネージャー', 'email': 'yamada@example.com'},
        {'id': 2, 'name': '佐藤 華子', 'dept': '開発部', 'role': 'エンジニア', 'email': 'sato@example.com'},
        {'id': 3, 'name': '伊藤 健太', 'dept': '開発部', 'role': '一般', 'email': 'ito@example.com'},
        {'id': 4, 'name': '鈴木 一郎', 'dept': '人事部', 'role': '一般', 'email': 'suzuki@example.com'},
    ]

    # 一覧ページ用
    def staff_list(request):
        return render(request, 'staff/list.html', {'members': STAFF_MEMBERS})

    # 詳細ページ用
    def staff_detail(request, user_id):
        # user_idが一致する人を1人探す
        user = next((s for s in STAFF_MEMBERS if s['id'] == user_id), None)
        return render(request, 'staff/detail.html', {'user': user})
    ```

---

### STEP 3：URLを繋ぐ（ルーティング）
「どの住所にアクセスしたら、どのViewを呼ぶか」を設定します。

1.  **アプリ側**：`staff/` フォルダの中に、**`urls.py` というファイルを新規作成**し、以下を入力。
    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('list/', views.staff_list, name='staff_list'),
        path('user/<int:user_id>/', views.staff_detail, name='staff_detail'),
    ]
    ```
2.  **プロジェクト全体**：`myproject/urls.py` を開き、`staff` アプリのURLを読み込む。
    ```python
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('inventory/', include('inventory.urls')),
        path('portal/', include('staff.urls')), # ← 追加！
    ]
    ```

---

### STEP 4：見た目を作る（Template）
データを表示するためのHTMLを作成します。

1.  `templates/` フォルダの中に、さらに **`staff`** という名前のフォルダを作る。
2.  `templates/staff/list.html` を作成し、以下を入力。
    ```html
    {% extends 'base.html' %}
    {% block content %}
    <h1>社員名簿一覧</h1>
    <table border="1">
        <tr><th>氏名</th><th>部署</th><th>詳細</th></tr>
        {% for m in members %}
        <tr>
            <td>
                {% if m.role == 'マネージャー' %} 👑 <strong>{{ m.name }}</strong> {% else %} {{ m.name }} {% endif %}
            </td>
            <td>{{ m.dept }}</td>
            <td><a href="{% url 'staff_detail' m.id %}">詳細を見る</a></td>
        </tr>
        {% endfor %}
    </table>
    {% endblock %}
    ```
3.  `templates/staff/detail.html` を作成し、以下を入力。
    ```html
    {% extends 'base.html' %}
    {% block content %}
    <h1>社員詳細情報</h1>
    {% if user %}
        <ul>
            <li>氏名：{{ user.name }}</li>
            <li>部署：{{ user.dept }}</li>
            <li>役職：{{ user.role }}</li>
            <li>メール：{{ user.email }}</li>
        </ul>
    {% else %}
        <p>該当する社員は見つかりません。</p>
    {% endif %}
    <a href="{% url 'staff_list' %}">一覧に戻る</a>
    {% endblock %}
    ```

---

### STEP 5：動作確認
最後にブラウザで正しく動くかチェックします。

1.  ブラウザを開き `http://127.0.0.1:8000/portal/list/` にアクセス。
2.  名簿が表示され、マネージャーの山田さんに「👑」がついていれば成功！
3.  「詳細を見る」をクリックして、個人の情報が表示されるか確認。

---

### 💡 うまくいかない時のヒント
*   **ファイル保存**：全てのファイルを `Ctrl + S` で保存しましたか？
*   **フォルダ名**：`templates/staff/` のスペルは合っていますか？
*   **エラー画面**：ブラウザに赤い画面が出たら、一番上のメッセージを読みましょう。URLの打ち間違い（`/portal/list/`）がないかも確認！
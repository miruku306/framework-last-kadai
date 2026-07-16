第6回の授業案を作成しました。
今回のテーマは **「CRUDの完成（更新・削除）」** です。これで、データの登録・表示・変更・消去というWebアプリの基本操作ができます。

---

# 第6回：フォームとCRUD ②
**データの更新（Update）と削除（Delete）**

---

## 0. 本日のロードマップ

本日は、CRUDの残り2つ、**Update（更新）** と **Delete（削除）** を学びます。

1.  **【説明】更新と削除の仕組み**
    *   新規登録と更新の違い（instanceの概念）
    *   削除時の注意点（確認画面の必要性）
2.  **【学習：在庫管理】編集・削除機能の実装**
    *   既存データの読み込み → 保存 → 削除
3.  **【実習：社員名簿】CRUD機能の全完成**
    *   ※実習用コンテナに切り替えて実施

---
## おさらい　ModelFormとは
* 「Model（データの設計図）」を読み取って、「HTMLの入力画面」を自動で作ってくれる機能のことです。
* 普通のHTMLフォームとの違い<br>
普通のHTML: ```<input type="text" name="name">``` などを1つずつ自分で書く必要があります。<br>
ModelForm: 「Itemモデルの項目を全部出して！」と1行書くだけで、Djangoが適切なタグを生成してくれます。
---
## おさらい　ModelFormのメリット
- ①開発スピードが速い<br>
  モデル（models.py）ですでに「名前は100文字まで」「価格は数字」と決めています。ModelFormはそれを再利用するので、同じことを二度書かずに済みます。
- ②自動でバリテーション（入力チェック）をしてくれる<br>
  例えば、数字を入れる場所に「あいうえお」と打って送信した場合、ModelFormは自動的に 「数字を入力してください」というエラーメッセージ を出してくれます。この「チェック機能」を自分でプログラミングする必要はありません。
- ③データベースへの保存が簡単<br>
  送られてきたデータを一つずつ取り出してDBに入れる作業（name = request.POST['name'] など）が不要です。form.save() と書くだけで、自動的にデータベースへ保存されます。
---
## おさらい ModelFormの書き方
- アプリフォルダの中に forms.py というファイルを作って定義します。
```python
# inventory/forms.py
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    # 「Metaクラス」の中に設定を書くルール
    class Meta:
        model = Item               # どのモデルをベースにするか
        fields = ['name', 'price']  # どの項目を画面に出すか
```
### ModelForm Metaクラスとは
「クラスの中の設定用クラス」です。「このフォームは、このモデル専用ですよ」という設定情報をこの中に書くのがDjangoの決まりです。

### ModelForm View での使い方
- Viewでは、 **「画面を出す時（GET）」と「データが届いた時（POST）」** で動きを分けます。
```python
def item_create(request):
    if request.method == 'POST':
        # --- データが送られてきた時 ---
        form = ItemForm(request.POST) # 届いたデータをフォームに詰める
        if form.is_valid():           # 自動チェック（バリデーション）
            form.save()               # 合格なら保存！
            return redirect('list')
    else:
        # --- 最初に関数を呼び出した時 ---
        form = ItemForm()             # 空のフォームを用意する

    return render(request, 'form.html', {'form': form})
```
### ModelForm テンプレートでの表示方法
* ``{{ form.as_p }}``: 各入力項目を ``<p>`` タグで囲って表示
* ``{{ form.as_table }}``: 各入力項目を ``<tr>`` タグで囲って表示
* ``{{ form.as_ul }}``: 各入力項目を ``<li>`` タグで囲って表示

```python
<form method="POST">
    {% csrf_token %} <!-- セキュリティ必須　これがないと403エラー -->
    {{ form.as_p }} <!-- これだけでinputタグが全部出る！ -->
    <button type="submit">送信</button>
</form>
```

---
## 1. 【講義】更新（Update）と削除（Delete）の考え方

### 1-1. 新規登録(Create) と 更新(Update) の違い
Djangoの `ModelForm` を使う場合、コードはほとんど同じですが、たった一つ大きな違いがあります。

*   **新規登録**: 真新しい「空のフォーム」を作る。
*   **更新**: DBから取り出した **「既存のデータ（instance）」を詰め込んだフォーム** を作る。

DjangoのModelFormにおいて、新規(Create)と更新(Update)を分けるのは、 **「そのフォームが特定のデータ（実物）と紐付いているかどうか」** です。これをDjangoでは instance（インスタンス） と呼びます。

### 1-2. なぜ削除（Delete）には確認画面が必要か
削除はやり直しがききません。「削除ボタン」を押した瞬間に消える設定にすると、誤操作で大切なデータを失うリスクがあります。
プロの現場では、必ず **「本当に消しますか？」という確認画面（またはポップアップ）** を挟むのが鉄則です。
データの用途によっては削除ではなく新たなデータを追加したり、表示するか状態を管理するなどの運用がいい場合もあります。

---

## 2. 【学習フェーズ】在庫管理システムを完成させる

授業用コンテナ（学習用）で実施します。

### 2-1. 編集機能の作成 (`inventory/views.py`)
既存のデータをフォームに渡すために `instance` 引数を使います。

```python
# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm

def item_update(request, item_id):
    # 1. 編集したいデータをDBから1件取り出す
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        # 2. 既存データ(instance)をベースに、送られてきたデータで上書き
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        # 3. 最初は既存データが入った状態のフォームを表示
        form = ItemForm(instance=item)

    return render(request, 'inventory/item_form.html', {'form': form})
```
> **Point:** 新規登録で使った `item_form.html` をそのまま使い回せるので、効率的です。

### 2-2. 削除機能の作成 (`inventory/views.py`)
安全のため、POSTメソッドが送られてきた時だけ削除を実行するようにします。

```python
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete() # データを削除
        return redirect('item_list')

    # GETの時は確認画面を表示
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})
```

### 2-3. URLの設定 (`inventory/urls.py`)
```python
path('edit/<int:item_id>/', views.item_update, name='item_update'),
path('delete/<int:item_id>/', views.item_delete, name='item_delete'),
```

### 2-4. テンプレートの作成
**① 削除確認画面 (`templates/inventory/item_confirm_delete.html`)**
```html
{% extends 'base.html' %}
{% block content %}
<h1>データを削除しますか？</h1>
<p>「{{ item.name }}」を削除しようとしています。この操作は取り消せません。</p>

<form method="POST">
    {% csrf_token %}
    <button type="submit" style="background-color: red; color: white;">本当に削除する</button>
    <a href="{% url 'item_list' %}">キャンセル</a>
</form>
{% endblock %}
```

**② 一覧画面にリンクを追加 (`templates/inventory/item_list.html`)**
```html
<table border="1">
    <tr>
        <th>商品名</th><th>価格</th><th>在庫</th><th>編集</th><th>削除</th>
    </tr>
    {% for item in items %}
    <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.price }}円</td>
        <td>
            {% if item.stock == 0 %}
                <span style="color:red;">在庫なし</span>
            {% else %}
                {{ item.stock }}
            {% endif %}
        </td>
        <td>
            <a href="{% url 'item_update' item.id %}">編集</a>
        </td>
        <td>
            <a href="{% url 'item_delete' item.id %}" style="color: red;">削除</a>
        </td>

    </tr>
    {% endfor %}
</table>
```

---


---

## 4.  なぜ `instance=` が必要なのか？

よくやるミスは、更新の時に `instance=item` を書き忘れることです。

*   **もし `instance=item` がなかったら？**
    *   Djangoはそれが「更新」だと気づけません。
    *   保存ボタンを押したとき、既存のデータが書き換わるのではなく、**「全く同じ内容の新しいデータ」がもう1つ増えてしまいます。**
* ModelFormはinstanceを渡されると「書き換えればいいんだな」と解釈しますが、渡さないと「新しく作れ」と解釈してしまいます。

---

## 5.よくあるエラー

*   **`GenericDetailView` などのエラー**
    *   URLの `item_id` と Viewの引数名が一致しているか確認しましょう。
*   **削除しても一覧から消えない**
    *   `item.delete()` を書き忘れていないか、保存（Ctrl+S）したか確認しましょう。
*   **404 Not Found**
    *   存在しないIDのURLを直打ちしていないか確認しましょう。

---

### 今日のポイント
1.  既存データの編集ができ、DBの内容が書き換わっている。
2.  削除確認画面を経て、安全にデータが削除できる。
3.  一覧 ➔ 登録 ➔ 詳細 ➔ 編集 ➔ 削除 の一連の動線が繋がっている。

---
**次回予告：**
第7回は、これら全ての操作を「ログインしたスタッフだけ」ができるようにする **「認証機能（Login）」** を学びます！


今回のテーマは **「フォーム（Form）とデータの登録」** です。

前回までは管理画面（Admin）からデータを入力していましたが、今回は**一般のユーザーがブラウザ上の画面からデータを入力・送信できる機能**を実装します。

---

# 第5回：フォームとデータの登録
**〜 ユーザーからの入力を受け付け、DBへ保存する 〜**

---

## 本日のロードマップ

本日は、CRUD（データの基本操作）のうち、 **Create（作成）** を学びます。

1.  **【講義】CRUDとフォームの役割**
    *   なぜ管理画面以外にフォームが必要なのか
    *   CSRF対策（セキュリティ）について
2.  **【学習：在庫管理】新規登録機能の実装**
    *   ModelFormの活用 → ビューでのPOST処理 → 画面遷移
3.  **【練習課題：社員名簿】新規メンバー追加機能の実**
    *   ※実習用コンテナに切り替えて実施
4.  **課題実施時間など**

---

## 事前知識：POSTとGET通信について

POST通信とGET通信の違いについて確認しましょう。

1. **【 GET通信 】**
   *  **「中身が外から丸見え」** の送り方です。URLの後ろに ?name=yamada&price=1000 のようにデータがくっつきます。
   *  主な利用場面として、検索やページ番号などに利用される。

2. **【 POST通信 】**
   *  **「中身を隠して送る」** 送り方です。URLにはデータが表示されず、通信の「中身（ボディ）」に隠されます。
   *  主な利用場面として、認証画面（ログイン）などに利用される。


---

## 1.　CRUDとフォーム

### 1-1. CRUD（クラッド）とは
Webシステムの基本となる4つの機能の頭文字です。
*   **C**reate（作成）：データを新しく作る ← **今日の内容**
*   **R**ead（参照）：データを表示する（前回やった一覧・詳細）
*   **U**pdate（更新）：データを書き換える（次回）
*   **D**elete（削除）：データを消す（次回）

### 1-2. Djangoのフォーム機能
HTMLで `<input>` タグを並べてフォームを作るのは大変ですが、Djangoには **ModelForm（モデルフォーム）** という便利な機能があります。これを使うと、**「モデル（設計図）」から自動的に入力画面を生成**してくれます。

---

## 2. 在庫管理システムに登録機能を追加

授業用コンテナ（学習用）で実施します。

### 2-1. フォームの定義 (`inventory/forms.py`)
アプリフォルダの中に `forms.py` というファイルを新規作成します。

```python
# inventory/forms.py
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'stock'] # 入力させたい項目
```

### 2-2. ビューの作成 (`inventory/views.py`)
データを「表示する時（GET）」と「保存する時（POST）」の2通りの動きを書きます。

```python
# inventory/views.py
from django.shortcuts import render, redirect # redirectを追加
from .forms import ItemForm

def item_create(request):
    if request.method == 'POST':
        # 2. 送信されたデータを受け取って保存する処理
        form = ItemForm(request.POST)
        if form.is_valid(): # 入力チェック（バリデーション）
            form.save()     # DBへ保存
            return redirect('item_list') # 保存後は一覧へ戻る
    else:
        # 1. 最初に入力画面を表示する処理
        form = ItemForm()

    return render(request, 'inventory/item_form.html', {'form': form})
```
* `インポート .forms を解決できませんでしたPylancereportMissingImports`　と出ることがありますがVSCodeが読み込めてないだけで、プログラムとしては問題ありません。このまま起動できます。気になる場合はVSCodeの再起動などで警告は消えます。

### 2-3. URLの設定 (`inventory/urls.py`)
```python
path('add/', views.item_create, name='item_create'),
```

### 2-4. テンプレートの作成 (`templates/inventory/item_form.html`)
```html
{% extends 'base.html' %}
{% block content %}
<h1>商品の新規登録</h1>

<form method="POST">
    {% csrf_token %} <!-- セキュリティのため -->
    {{ form.as_p }} <!-- フォームをPタグ形式で自動表示 -->
    <button type="submit">登録する</button>
</form>

<hr>
<a href="{% url 'item_list' %}">キャンセルして戻る</a>
{% endblock %}
```

---

## 3. 【解説】CSRF（クロスサイトリクエストフォージェリ）対策について

テンプレートに書いた `{% csrf_token %}` は非常に重要です。

*   **役割**：自分のサイト以外の「偽物の画面」から勝手にデータを送信されるのを防ぐ（クロスサイトリクエストフォージェリ攻撃の対策）。
*   **仕組み**：Djangoが画面を表示する時に「内緒の合言葉（トークン）」を発行し、送信された時にその合言葉が合っているかチェックします。
*   **注意**：これを書き忘れると、Djangoはセキュリティ保護のために **「403 Forbidden」** エラーを出し、データの保存を拒否します。

---

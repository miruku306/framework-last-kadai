
---

# 第3回：Django　URL設計・View・テンプレートの連携

---
## 第３回準備

- 授業は学習と実習で内容を分けていきます。コンテナを分けて作業をしてください。

- lesson-02のフォルダ(Djangoの開発環境を構築したフォルダ)を複製して適切な名前に変更して作業しましょう。

- 複製したフォルダにある**docker-compose.yml**のコンテナ名を任意の名称に変更します。

```
services:
  web:
    build: .
    container_name: ここのコンテナ名をかぶらない名前に変更
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    tty: true
    stdin_open: true
```

保存後、コンテナを開いてください。

---

## 1. Djangoの仕組み「MTVモデル」

Djangoは、Webサイトを**「3つの役割」**に分けて管理します。これを**MTVパターン**と呼びます。

### 役割分担のイメージ：レストラン
Webサイトをレストランに例えると、役割が非常に分かりやすくなります。

| 要素 | 正式名称 | レストランでの例え | 役割 |
| :--- | :--- | :--- | :--- |
| **M** | **Model**（モデル） | **食材・倉庫** | データの保存・取り出しを担当（次回詳しく実施） |
| **T** | **Template**（テンプレート） | **お皿・盛り付け** | 画面の見た目（HTML）を担当 |
| **V** | **View**（ビュー） | **料理人（シェフ）** | 食材を加工し、お皿に盛り付ける「命令」を担当 |
| **URL** | **URLconf**（URL設定） | **注文票・メニュー** | どの料理（View）を作るか決定する入り口 |

---

### 💻 ブラウザに画面が出るまでの「4ステップ」

混乱しやすい「処理の順番」

1.  **リクエスト (注文)**
    ユーザーがURL（例: `/items/`）にアクセスする。
2.  **URLconf (注文の振り分け)**
    `urls.py` が「このURLなら、このView（料理人）を呼ぼう」と決める。
3.  **View (調理・加工)**
    `views.py` がデータを準備する（今回はリスト形式のデータ）。
    それをテンプレート（お皿）へ送る。
4.  **Template (完成品)**
    `html` ファイルがデータを受け取り、最終的な見た目を作ってブラウザに返す。

> **なぜ分けるのか？**：
> デザイン（T）を変えたい時に、データ処理（V）のコードを触らなくて済むからです。チーム開発（デザイナーとエンジニアの分業）がしやすくなります。

---

## 2. 【学習フェーズ】ハンズオン：在庫管理システムの構築

ここからは、実際に手を動かして「URL → View → Template」を繋いでいきます。

前回の **django-admin startproject myproject .** を実行した後を想定しています。

### STEP 1：アプリの作成とDjangoへの登録
プロジェクトの中に「在庫管理（inventory）」という名前のアプリを作ります。

```bash
# ターミナルで実行
python manage.py startapp inventory
```

次に、プロジェクト全体に「新しいアプリとテンプレートの場所」を教えます。

```python
# myproject/settings.py


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0'] # ← 開発中は、自分のPC（localhost）からのアクセスを許可する

INSTALLED_APPS = [
    ...
    'inventory',  # ← 1. アプリを登録
]

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],  # ← 2. テンプレートの共通置き場を指定
        ...
    },
]
```

---

### STEP 2：URLの設計（注文票の作成）

URLは「プロジェクト用」と「アプリ用」の2段階で設定していきます。

**① アプリ側のURL設定 (`inventory/urls.py` を新規作成)**
```python
from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/inventory/items/ に対応
    path('items/', views.item_list, name='item_list'),
]
```
### 補足
**Module has no attribute "item_list"Mypyattr-defined**がviews.item_listに対して発生する場合、これはまだ定義されていないためです。次の項目で追加後、タブを開きなおすと解決する場合があります。


**② プロジェクト全体のURL設定 (`myproject/urls.py`)**
```python
from django.urls import path, include # includeを追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')), # inventoryアプリのURL設定を読み込む
]
```

### 補足　
**urls.pyのimportで警告（注意）が出る場合**

myptなど型チェックツールは強力にコードを確認してくれます。

フレームワークのような独自の書き方がある場合、警告が発生することがあります。

今回の場合は、requirements.txtに下記のモジュールを追加することで解決します。

```
# requirements.txt
django-stubs==6.0.5 # 追加
```
requirements.txtを保存します。

コンテナを開いている状態であれば左下のコンテナ名をクリックして、**コンテナーのリビルド**をクリックします。

---

### STEP 3：Viewの実装（料理人の命令）

Viewの仕事は、**「データを用意し、テンプレートに渡すこと」**です。

```python
# inventory/views.py
from django.shortcuts import render

# 今回は「Model」がまだ無いので、ここに直接データを用意します
ITEMS = [
    {'id': 1, 'name': 'ノートPC', 'price': 120000, 'stock': 5},
    {'id': 2, 'name': '無線マウス', 'price': 3500, 'stock': 0},
    {'id': 3, 'name': '27インチモニター', 'price': 45000, 'stock': 2},
]

def item_list(request):
    # テンプレートで使うための「辞書」を作る（contextと呼びます）
    context = {
        'items': ITEMS,
        'message': '本日の在庫状況です'
    }
    # render関数：(リクエスト, 使うテンプレート, 渡すデータ)
    return render(request, 'inventory/item_list.html', context)
```

---

### STEP 4：テンプレートの実装（盛り付け）

Django特有の書き方を使って、HTMLの中にデータを埋め込みます。

**準備　フォルダ作成**
templatesフォルダを以下の場所に作成
```text
lesson-03/
├── manage.py
├── myproject/
│   ├── settings.py
│   └── ...
├── inventory/
│   └── ...
└── templates/  ← 右クリックして「新しいフォルダー」で作る
    ├── base.html
    └── inventory/
        └── item_list.html
```

**① 共通レイアウト (`templates/base.html`)**
全ページで使い回す「外枠」を作ります。
```html
<!DOCTYPE html>
<html>
<head>
    <title>在庫管理システム</title>
</head>
<body>
    <nav> <strong>在庫管理APP</strong> | <a href="/inventory/items/">ホーム</a> </nav>
    <hr>
    {% block content %}
    <!-- ここに各ページの中身が入る -->
    {% endblock %}
</body>
</html>
```

**② 一覧画面 (`templates/inventory/item_list.html`)**
```html
{% extends 'base.html' %} <!-- base.htmlを土台にする -->

{% block content %}
<h2>{{ message }}</h2> <!-- 変数の表示 -->

<table border="1">
    <tr>
        <th>商品名</th><th>価格</th><th>在庫</th>
    </tr>
    {% for item in items %} <!-- ループ処理 -->
    <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.price }}円</td>
        <td>
            {% if item.stock == 0 %} <!-- 条件分岐 -->
                <span style="color:red;">在庫なし</span>
            {% else %}
                {{ item.stock }}
            {% endif %}
        </td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
```
---
# 実行方法
ターミナルで以下のコマンドを入力します。
```
python manage.py runserver 0.0.0.0:8000
```

ブラウザなどで、http://127.0.0.1:8000/inventory/items/ にアクセスする。

起動中に変更したものは自動的に反映されます。

---


## 💡 よくあるトラブル

1.  **URLの設定を忘れたら？**
    → ブラウザに「404 Not Found」が出て、Viewまで注文が届きません。
2.  **Viewで `context` にデータを入れ忘れたら？**
    → テンプレート（お皿）に中身が届かず、画面に何も表示されません。
3.  **Templateのタグ（`{% %}`）を書き間違えたら？**
    → Djangoが「どう表示すればいいか分からない！」とエラー（TemplateSyntaxError）を出します。

---


# Djangoテンプレートの書き方ガイド
---

## 1. Djangoテンプレートの「2大ルール」

HTMLファイルの中で、Django専用の命令を書くときは、必ず以下の記号を使います。

### ① `{{ 変数名 }}` ：データの表示（二重カッコ）
Viewから渡されたデータ（変数）を画面に出したいときに使います。
- **例**：`{{ item.name }}` ➔ 「ノートPC」と表示される。
- **覚え方**：**「二重のカッコは、データを見るためのメガネ」**

### ② `{% 命令 %}` ：ロジックの実行（カッコとパーセント）
繰り返し（for）や条件分岐（if）、ページの継承（extends）など、**「動き」**をつけたいときに使います。
- **例**：`{% if ... %}` ➔ もし〜なら実行せよ。
- **覚え方**：**「パーセントは、プログラムを動かす歯車」**

---

## 2. テンプレート継承（extends と block）

すべてのページに共通のヘッダーやメニューを何度も書くのは、プロの仕事ではありません。
Djangoでは**「親（共通枠）」**を作って、**「子（中身）」**がそれを借りる仕組みを使います。

### 🏠 親テンプレート：`base.html`
家でいうところの「外枠（壁や屋根）」です。中身を入れ替えたい場所に **`{% block %}`** という名前の穴を開けておきます。

```html
<!-- templates/base.html -->
<html>
<body>
    <nav>共通メニュー</nav>

    <hr>

    <!-- ここに名前（今回はcontent）をつけた「穴」を開ける -->
    {% block content %}
    {% endblock %}

    <hr>
    <footer>共通フッター</footer>
</body>
</html>
```

### 📄 子テンプレート：`item_list.html`
家でいうところの「家具や内装」です。親を呼び出し、親が開けた穴（block）の中に自分のコードを流し込みます。

```html
<!-- templates/inventory/item_list.html -->

<!-- 1. まず「親を借ります」と宣言する（1行目に書くこと！） -->
{% extends 'base.html' %}

<!-- 2. 親が作った「content」という穴を埋める -->
{% block content %}
    <h1>商品一覧ページ</h1>
    <p>ここが親の穴の中に表示されます。</p>
{% endblock %}
```

---

## 3. よく使う「制御構文」

### 🔄 繰り返し処理（for）
データのリストを順番に表示します。**最後に必ず `{% endfor %}` が必要**です。

```html
<ul>
    {% for item in items %}
        <li>{{ item.name }}：{{ item.price }}円</li>
    {% empty %}
        <li>データがありません。</li> <!-- リストが空だった時の処理（任意） -->
    {% endfor %}
</ul>
```

### ❓ 条件分岐（if）
値によって表示を変えます。**最後に必ず `{% endif %}` が必要**です。

```html
{% if item.stock == 0 %}
    <p style="color: red;">売り切れです</p>
{% elif item.stock <= 5 %}
    <p>残りわずか（{{ item.stock }}個）</p>
{% else %}
    <p>在庫あり</p>
{% endif %}
```

---

## 4. 便利なタグ：URLの生成

リンクを貼るときに、`/inventory/items/` と直接書くと、後でURLを変えたくなった時に大変です。Djangoでは**「URLの名前」**を使ってリンクを作ります。

```html
<!-- urls.py で name='item_detail' と付けたURLを呼び出す -->
<a href="{% url 'item_detail' item.id %}">詳細を見る</a>
```

---

## ⚠️ よくあるミス

1.  **タグの閉じ忘れ**
    `{% for %}` を書いたら、必ず `{% endfor %}` を書く。これを忘れるとエラーで画面が真っ白になります。
2.  **`extends` の位置**
    `{% extends 'base.html' %}` は、必ず**ファイルの1行目**に書いてください。その上にコメントや空行があってもいけません。
3.  **ブロック名の不一致**
    親で `{% block main %}` としたなら、子でも `{% block main %}` と書く必要があります。名前が違うと穴が埋まりません。

---

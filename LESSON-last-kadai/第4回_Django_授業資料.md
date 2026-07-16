
---

# 第4回：モデルとデータベース（授業資料）

## 0. 本日のロードマップ

本日は、MTVモデルの **「M（Model）」** を学びます。
前回までは「料理人（View）」が自分の手元にある材料（リストデータ）で料理を作っていましたが、今日からは**「倉庫（データベース）」**から食材を取り出す仕組みを作ります。

1.  **【学習：在庫管理】DB環境の構築**
    *   PostgreSQLコンテナの追加と接続設定
2.  **【学習：在庫管理】モデルの定義と取得**
    *   Model作成 → マイグレーション → ORMでのデータ取得
3.  **【練習課題（成績対象）：社員名簿】仕様書に基づき自力でDB化**
    *   ※実習用コンテナに切り替えて実施

> [!CAUTION]
> **注意：** ここからの内容は授業用のコンテナ（学習用）を使用してください。練習課題用とはコンテナを分けて作業してください。

---

## 1. 【学習】DB環境の構築

### 1-1. データベース（PostgreSQL）の追加
学習用プロジェクトの `docker-compose.yml` を書き換えて、DB専用のコンテナを追加します。

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=django_db
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=django_pass

  web:
    # ...既存の設定はそのまま...
    depends_on:
      - db

volumes:
  postgres_data:
```

### 💡 `volumes: postgres_data:` はなぜ必要なのか？
結論から言うと、 **「コンテナを消しても、入力したデータ（社員や商品）を消さないため」** に絶対必要です。

#### ① コンテナは「使い捨て」の部屋
Dockerコンテナは、例えるなら **「中身をいつでもリセットできるホテルの客室」** のようなものです。
*   あなたが管理画面からデータを100件入力しても、それは「客室の机の引き出し」に置いただけの状態です。
*   `docker compose down`（コンテナの削除）をすると、客室ごと壊されて新しい部屋に変わるため、**引き出しの中身（データ）はすべて消えてしまいます。**

#### ② ボリュームは「外にある貸し倉庫」
ここで `volumes` の設定が登場します。`postgres_data` というのは、コンテナの外（あなたのPC上）に作る**「専用の貸し倉庫」**の名前です。

*   **設定の意味：** `postgres_data:/var/lib/postgresql/data`
    ➔ 「コンテナ内のデータベース保存場所」を、「外にある倉庫（postgres_data）」に繋ぎなさい、という命令です。

こうすることで、コンテナを壊したり作り直したりしても、**大切なデータは倉庫に保管されている**ため、次にコンテナを立ち上げたときに続きから作業ができます。

#### 🛠 2箇所の書き方のポイント
1.  **services内のdb項目**: 「このコンテナはこの倉庫を使ってね」という紐付け
2.  **最下部のvolumes項目**: 「このプロジェクトでこの名前の倉庫を作るよ」という宣言

> **鉄則：** プログラム（コード）とデータ（中身）を切り離して考える。
> *   **プログラム** ➔ コンテナに入れる。
> *   **データ** ➔ ボリューム（外のストレージ）で守る。

#### 🛠 トラブル時の対応（リセット）
「設定を間違えて一度完全にリセットしたい」という場合は、以下のコマンドを実行します。
```bash
# ボリューム（倉庫）ごと削除してリセットする
docker compose down -v
```
`-v` をつけるとボリュームも消えるので、真っさらな状態からやり直せます。

---

### 1-2. requirements.txtにモジュールを追加
`requirements.txt`に以下のモジュールを追加します。
```text
psycopg2-binary==2.9.12
```
*   `psycopg2-binary` は、PostgreSQLデータベースアダプタです。
*   DjangoがPostgreSQLと通信するために必要です。

### 1-3. コンテナーのリビルドを行う
設定を反映させるため、VS Codeの左下の青い部分（Dev Container）をクリックし、**「コンテナーのリビルド (Rebuild Container)」**を実行してください。

### 1-4. Djangoとの接続設定
`myproject/settings.py` を開き、DBの接続先を「内部メモリ（sqlite）」から「PostgreSQLコンテナ」へ変更します。

```python
# myproject/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': 'django_pass',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

---

## 2. 【学習】モデルの定義と操作

### 2-1. モデル（設計図）の作成
`inventory/models.py` でデータの形を定義します。

```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100) # 商品名
    price = models.IntegerField()            # 価格
    stock = models.IntegerField()            # 在庫数

    def __str__(self):
        return self.name
```

#### 💡 `def __str__(self):` の役割
**「そのデータが何という名前なのか、人間に分かりやすく表示するための設定」**です。

1.  **これがないとどうなるか？（デフォルト状態）**
    管理画面などで `Item object (1)` と表示され、中身が何か判別できません。
2.  **これがあるとどうなるか？**
    管理画面に `ノートPC` `無線マウス` と表示され、一目で分かるようになります。

*   **`self`**: 「今扱っているその1件の商品データ」を指します。
*   **`return self.name`**: 自分の `name` 項目を名前として返します。
*   **注意**: 必ず**文字列**を返す必要があります。数値などを返す場合は `str(self.price)` のように変換が必要です。

### 2-2. マイグレーション（工事の実行）
設計図を基に、データベースの中にテーブル（表）を作ります。

```bash
# 1. 設計図を作成
python manage.py makemigrations inventory

# 2. データベースに適用（工事の実施）
python manage.py migrate
```

### 2-3. 管理画面からデータを登録する
1.  **管理画面にモデルを出す**: `inventory/admin.py` に追記。
    ```python
    from .models import Item
    admin.site.register(Item)
    ```
2.  **管理者を作る**: ターミナルで `python manage.py createsuperuser` を実行。
IDとパスワードを決める。推奨８桁以上ですが、短いパスワードでも大丈夫です。(大丈夫か聞かれるのでy応答する)
3.  **ログイン**: http://127.0.0.1:8000/admin/ から商品データを3件以上登録。

### 2-4. Viewを「DB取得」に書き換える
前回のリスト（ITEMS）を消し、DBから取得するように変更します。

```python
# inventory/views.py
from .models import Item

def item_list(request):
    # DBからすべてのデータを取得
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})
```
* 前回同様、ブラウザなどで動作確認しましょう。　http://127.0.0.1:8000/inventory/items/

*   **なぜ `makemigrations` と `migrate` の2段階なの？**
    *   `makemigrations` は「設計図（指示書）」を作る作業。
    *   `migrate` はその指示書を見て、実際に「工事（DB操作）」をする作業です。
    *   設計図を一度確認することで、安全に工事を行うためです。
*   **`Item.objects.all()` って何？**
    *   これは「Django ORM」という機能です。本来は `SELECT * FROM inventory_item;` という難しいSQL文を書く必要がありますが、DjangoがPythonの言葉に翻訳してくれています。

---

## 補足解説：Django管理画面（Admin）とは？

### 1. 役割：サイトの「楽屋（バックステージ）」
運営者がデータを管理するための**「裏側の管理画面」**です。通常はイチから作る必要がありますが、Djangoは「モデル」を読み取って自動生成してくれます。

*   **データのCRUD操作**: 登録・参照・更新・削除がマウスで可能。
*   **ユーザー管理**: スタッフのID作成やパスワード変更。
*   **権限設定**: 「閲覧のみ」などの制限が可能。
*   **検索・絞り込み**: 大量データから即座に検索。

### 2. なぜ使うのか？
*   **圧倒的な開発スピード**: `admin.py` に数行書くだけで完成します。
*   **本物のデータでテスト**: 「名前が長いと表示が崩れるか？」などの確認が容易。

---

## 補足資料：Django ORMとは？
**SQLを書かずにデータベースを操る「翻訳機」**

### 1. ORMは「翻訳機」
**「Pythonの言葉」を「SQL」に自動で翻訳する機能**です。（Object-Relational Mapping）

### 2. なぜORMを使うのか？
*   **SQL（ORMなし）**: `SELECT * FROM inventory_item WHERE price >= 1000;`
*   **Django ORM**: `Item.objects.filter(price__gte=1000)`
➔ Pythonの文法で書けるため、ミスが減り、コードが読みやすくなります。

### 3. ORMのメリット
1.  **SQLを覚えなくても操作可能**: Pythonの知識だけでDBを扱えます。
2.  **セキュリティが強い**: 「SQLインジェクション」などの攻撃から自動で守ってくれます。
3.  **DBの種類を選ばない**: PostgreSQLでもSQLiteでも、Pythonコードを書き換える必要がありません。

### 🛠 ORMの代表例
*   `Item.objects.all()`：全件取得
*   `Item.objects.get(id=1)`：1件取得
*   `item.save()`：保存

> [!NOTE]
> 複雑な参照ではSQLより遅くなる場合もありますが、通常の開発ではORMの利便性が勝ります。状況に応じて使い分けましょう。

---
## mypy.iniの警告を止める
---
* `manage.py`と同じ階層に`mypy.ini`ファイルを作成し以下の内容にし保存します。
```
# mypy.ini

[mypy]
# Djangoプラグインを有効にする（すでに django-stubs が入っているため）
plugins =
    mypy_django_plugin.main

# インポートエラーを無視する設定
ignore_missing_imports = True

# django-environ 固有の型エラーを無視
[mypy-environ.*]
ignore_missing_imports = True

[mypy.plugins.django-stubs]
django_settings_module = "config.settings"
```

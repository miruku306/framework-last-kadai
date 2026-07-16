# Django 開発環境構築 手順書

**第2回 — Docker × Django**
docker-compose → コンテナ起動 → デモページ表示まで

> 対象：Windows / VS Code / Docker Desktop

> 全体所要時間：5-15分程度

---

## 🎯 本日のゴール

ブラウザで Django のデモページ（ロケット画面）を表示できる

```
http://127.0.0.1:8000
```

---

## 完成形のフォルダ構成

```
lesson-02/
├── .devcontainer/
│   └── devcontainer.json   ← STEP 2 で作成
├── Dockerfile              ← STEP 3 で作成
├── docker-compose.yml      ← STEP 4 で作成
├── requirements.txt        ← STEP 5 で更新
└── myproject/              ← STEP 6 で自動生成される
    ├── manage.py
    └── myproject/
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

---

## 準備

1. DockerDesktopを起動する

---

## STEP 1 — プロジェクトフォルダを作成する

1. エクスプローラーで作業場所（例：デスクトップ）を開く
2. 新しいフォルダ **`lesson-02`** を作成する
3. VS Code で「ファイル → フォルダを開く」→ `lesson-02` を選択
4. ターミナルを開く（`Ctrl + @`）

> ⚠️ フォルダ名にスペースや日本語は使わないこと
---
## STEP 2 — devcontainer.jsonの作成
1. **.devcontainer** フォルダを作成する
2. **devcontainer.json** ファイルを作成する
3. 作成したファイルの内容に以下のコードを入力する
```
{
  "name": "Django_Framework",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "web",
  "workspaceFolder": "/app",
  "postCreateCommand": "pip install --no-cache-dir -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.mypy-type-checker",
        "batisteo.vscode-django",
        "oderwat.indent-rainbow",
        "mikestead.dotenv"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "mypy-type-checker.importStrategy": "fromEnvironment",
        "editor.tabSize": 4,
        "editor.insertSpaces": true,
        "files.trimTrailingWhitespace": true,
        "files.insertFinalNewline": true,
        "files.associations": {
          "**/*.html": "django-html",
          "**/templates/**/*.html": "django-html"
        },
        "emmet.includeLanguages": {
          "django-html": "html"
        }
      }
    }
  }
}

```
### 拡張機能

無くても問題ありませんが便利な拡張機能なので入れてみてください

その他、必要な拡張機能があれば入れて構いません

| 拡張機能名 | 役割 |
| --- | --- |
| **ms-python.python** | Python 実行・デバッグをサポート |
| **ms-python.black-formatter** | Python コードを自動整形（Black） |
| **ms-python.mypy-type-checker** | 型チェック（mypy）でバグを防ぐ |
| **batisteo.vscode-django** | Django 用の補完・テンプレートサポート |
| **oderwat.indent-rainbow** | インデントを色分けして見やすくする |
| **mikestead.dotenv** | ``.env`` ファイルの構文ハイライト |

---

## STEP 3 — Dockerfile を作成する

VS Code で **`Dockerfile`** という名前のファイルを作成する（拡張子なし）

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
```

| 命令 | 意味 |
|------|------|
| `FROM python:3.12-slim` | 公式のPython 3.12軽量イメージをベースにする |
| `WORKDIR /app` | コンテナ内の作業フォルダを `/app` に設定 |
| `apt-get install` | git・curl などの便利ツールをインストール |
| `COPY requirements.txt` | 先にこれだけコピーしてpipを実行（キャッシュ最適化） |
| `COPY . .` | 残りのソースコードをコンテナにコピー |

---

## STEP 4 — docker-compose.yml を作成する

**`docker-compose.yml`** を作成して以下を入力する

```yaml
services:
  web:
    build: .
    container_name: lesson-django
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    tty: true
    stdin_open: true
```

| 設定 | 意味 |
|------|------|
| `build: .` | このフォルダの Dockerfile でイメージをビルド |
| `volumes: .:/app` | ホストのフォルダとコンテナを同期（ファイル保存が即反映） |
| `ports: 8000:8000` | ホストの 8000 番ポートをコンテナに繋ぐ |
| `tty / stdin_open` | Dev Containers から接続するために必要 |

---

## STEP 5 — requirements.txt を更新する

**`requirements.txt`** に Django を追加する

```text
# Django本体（★今回追加）
Django==6.0.5

# 整形ツール
black==26.5.1

# 型チェックツール
mypy==2.1.0
```

> **なぜ requirements.txt を使うのか？**
> `pip install Django` だけでもインストールできるが、ファイルに書いておくことで
> ① チームメンバーが同じバージョンを使える
> ② Docker ビルド時に自動インストールされる
> ③ バージョン管理できて「どこで動いていたか」がわかる

> **Django6.0系の動作環境について**
> 動作サポートされているバージョンについて　Python 3.12～3.14が必要

---

## STEP 6 — イメージをビルドする

### コンテナーを再度開くからビルドする
「コンテナを再度開く」からイメージをビルドすることが可能です。
画面左下のリモート接続をクリックして「コンテナを再度開く」をクリックするか、画面右下に「コンテナを再度開く」が出ている場合はそこからもイメージをビルドすることが可能です。

「キーを押して終了」がでたら何かキーを押すと通常のターミナルに移動します。

> ⚠️ **ビルドができない場合**
> devcontainerを使用する場合 .devcontainerフォルダと設定が読み込めないとビルドできないことがあります。
> ファイル名や設定内容に誤字がないか確認します。
> 最後にVSCodeの再起動を試してみてください。


> ⚠️ **初回は数分かかることがあります**
> エラーが出た場合はネット接続を確認してください。

---

## STEP 7 — Django プロジェクトを作成する

コンテナ内のターミナルで実行する

```bash
django-admin startproject myproject .
```

実行後、`myproject/` フォルダが自動生成される。

---

## STEP 8 — サーバーを起動する
### ターミナルで以下を実行
```bash
python manage.py runserver 0.0.0.0:8000
```

- ✅ `Starting development server at http://0.0.0.0:8000/` が表示されれば起動成功
- 🛑 サーバーを止めるときは `Ctrl + C`
- 🔄 ファイルを保存すると自動でリロードされる（StatReloader）

---

## STEP 9 — ブラウザでデモページを確認する

- ブラウザのアドレスバーに入力する
- 学内のインターネット環境やファイアウォールの設定によってhttp://0.0.0.0:8000/ でアクセスできない可能性があります

```
http://127.0.0.1:8000
```

### ✅ 確認ポイント

- [ ] ロケットの絵文字（🚀）が表示されている
- [ ] 「The install worked successfully!」の文字がある
- [ ] Django のバージョンが表示されている

### ❌ うまくいかない場合

「Error」や赤い画面が出ている → STEP 5 に戻ってビルドし直す

---

## よくあるエラーと対処法

### `port is already allocated`

**原因**：8000 番ポートが他のプロセスに使われている

**対処**：
```bash
docker compose down
docker compose up
```

---

### `ModuleNotFoundError: No module named 'django'`

**原因**：requirements.txt に Django が書かれていない、またはビルドし直していない

**対処**：
1. `requirements.txt` に `Django==6.0.5` を追記
2. `docker compose build` を実行
3. `docker compose up` を実行

---

### `django-admin: command not found`

**原因**：コンテナがビルドされていない、または volumes の同期がされていない

**対処**：
```bash
docker compose build
docker compose run --rm web django-admin startproject myproject .
```

---

### ブラウザで「接続できません」が出る

**原因**：サーバーがまだ起動していない、またはポート番号が違う

**対処**：ターミナルに `Starting development server...` が表示されているか確認。URL は `http://localhost:8000`

---

## よく使う Docker コマンド一覧

| コマンド | 意味 |
|---------|------|
| `docker compose build` | Dockerfile からイメージをビルド（requirements.txt 変更後は必ず実行） |
| `docker compose up` | コンテナを起動（Django 開発サーバーも同時に立ち上がる） |
| `docker compose up -d` | バックグラウンドで起動（ターミナルが塞がれない） |
| `docker compose down` | コンテナを停止・削除する |
| `docker compose run --rm web <コマンド>` | コンテナ内でコマンドを 1 回だけ実行する |
| `docker compose exec web python manage.py ...` | 起動中のコンテナ内で manage.py を実行する |
| `docker ps` | 起動中のコンテナ一覧を表示する |
| `docker compose logs` | コンテナのログを表示する（エラー調査に使う） |

---

## まとめ 

1. **Dockerfile** と **docker-compose.yml** の書き方
2. **requirements.txt** で Python パッケージを管理
3. `docker compose build → up` で Django を起動
4. ブラウザでデモページ（ロケット画面）を確認

時間に余裕があれば、Djangoの公式HPのチュートリアルやってみましょう

---


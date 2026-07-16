from django.db import models


class Video(models.Model):
    """
    レンタルビデオ情報
    """

    GENRE_CHOICES = [
        ("洋画", "洋画"),
        ("邦画", "邦画"),
        ("アニメ", "アニメ"),
        ("ドラマ", "ドラマ"),
        ("ホラー", "ホラー"),
        ("SF", "SF"),
        ("コメディ", "コメディ"),
        ("ドキュメンタリー", "ドキュメンタリー"),
        ("その他", "その他"),
    ]

    # 商品コード
    product_code = models.CharField(
        "商品コード",
        max_length=10,
        unique=True,
    )

    # タイトル
    title = models.CharField(
        "タイトル",
        max_length=100,
    )

    # ジャンル
    genre = models.CharField(
        "ジャンル",
        max_length=30,
        choices=GENRE_CHOICES,
    )

    # 説明
    description = models.TextField(
        "作品説明",
        blank=True,
    )

    # 総在庫数
    stock = models.PositiveIntegerField(
        "総在庫数",
        default=0,
    )

    # 貸出中
    rented = models.PositiveIntegerField(
        "貸出中",
        default=0,
    )

    # ジャケット画像
    image = models.ImageField(
        "ジャケット画像",
        upload_to="videos/",
        blank=True,
        null=True,
    )

    # 発売日
    release_date = models.DateField(
        "発売日",
        blank=True,
        null=True,
    )

    # 登録日時
    created_at = models.DateTimeField(
        "登録日時",
        auto_now_add=True,
    )

    # 更新日時
    updated_at = models.DateTimeField(
        "更新日時",
        auto_now=True,
    )

    @property
    def available_stock(self):
        """貸出可能数"""
        return self.stock - self.rented

    @property
    def stock_status(self):
        """在庫状態"""

        if self.available_stock == 0:
            return "在庫切れ"

        if self.available_stock <= 4:
            return "残りわずか"

        return "在庫あり"

    def __str__(self):
        return f"{self.product_code} : {self.title}"

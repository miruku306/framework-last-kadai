from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)  # 氏名
    dept = models.CharField(max_length=100)  # 部署名
    role = models.CharField(max_length=100)  # 役職
    email = models.EmailField()  # メールアドレス
    joined_date = models.DateField()  # 入社日

    def __str__(self):
        return self.name

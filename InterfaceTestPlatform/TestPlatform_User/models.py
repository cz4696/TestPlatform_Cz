from django.db import models


# Create your models here.

# 创建表 需要注册表：python3 manage.py makemigrations   同步：migrate
class Project_Date(models.Model):
    id = models.AutoField(primary_key=True)
    pj_id = models.IntegerField()
    pj_name = models.CharField(max_length=8)
    pj_pname = models.CharField(max_length=8)
    pj_tname = models.CharField(max_length=8)
    pj_state = models.CharField(max_length=6)

# def __unicode__(self):
#     return self.pj_id

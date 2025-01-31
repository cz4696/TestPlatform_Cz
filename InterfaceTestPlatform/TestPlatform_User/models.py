from django.db import models


# Create your models here.

# 创建表 需要注册表：python3 manage.py makemigrations   同步：migrate
class Project_Data(models.Model):
    id = models.AutoField(primary_key=True)
    pj_id = models.IntegerField()
    pj_name = models.CharField(max_length=10)
    pj_pname = models.CharField(max_length=10)
    pj_pn = models.CharField(max_length=10)
    pj_tname = models.CharField(max_length=10)
    pj_state = models.CharField(max_length=6)


class Interface_Data(models.Model):
    id = models.AutoField(primary_key=True)
    in_id = models.IntegerField()
    in_mname = models.CharField(max_length=10)
    in_type = models.CharField(max_length=8)
    in_url = models.CharField(max_length=100)
    in_data_type = models.CharField(max_length=8)
    in_data = models.CharField(max_length=50)
    in_tname = models.CharField(max_length=10)
    in_expected_result = models.IntegerField()
    in_actual_result = models.CharField(max_length=20)
    status = models.IntegerField()

# def __unicode__(self):
#     return self.pj_id

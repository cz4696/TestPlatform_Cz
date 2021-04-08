from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from . import *
# Create your views here.
from TestPlatform_User import models
import json


def get_pj_data(request):
    pj_data = models.Project_Data.objects.all().values()
    data_list = list(pj_data)
    data_list = {"code": 200, "msg": "ok", "count": len(data_list), "data": data_list}
    return HttpResponse(json.dumps(data_list))


def get_inter_data(request):
    inter_data = models.Interface_Data.objects.all().values()
    data_list = list(inter_data)
    data_list = {"code": 200, "msg": "ok", "count": len(data_list), "data": data_list}
    return HttpResponse(json.dumps(data_list))


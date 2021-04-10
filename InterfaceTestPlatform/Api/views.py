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
    pj_id = request.GET.get('id')
    if pj_id == None:
        return HttpResponse(json.dumps(data_list))
    else:
        data = data_list['data']
        search_data = []
        for i in data:  # 获得列表中的每个字典
            for key, value in i.items():
                if key == 'pj_id' and value == int(pj_id):
                    search_data.append(i)
        if search_data != []:
            data_list = {"code": 200, "msg": "ok", "count": len(search_data), "data": search_data}
            return HttpResponse(json.dumps(data_list))
        else:
            data_list = {"msg": "没有查询到该条数据！", "count": 0, "data": ''}
            return HttpResponse(json.dumps(data_list))


def get_inter_data(request):
    inter_data = models.Interface_Data.objects.all().values()
    data_list = list(inter_data)
    data_list = {"code": 200, "msg": "ok", "count": len(data_list), "data": data_list}
    in_id = request.GET.get('id')
    if in_id == None:
        return HttpResponse(json.dumps(data_list))
    else:
        data = data_list['data']
        search_data = []
        for i in data:  # 获得列表中的每个字典
            for key, value in i.items():
                if key == 'in_id' and value == int(in_id):
                    search_data.append(i)
        if search_data != []:
            data_list = {"code": 200, "msg": "ok", "count": len(search_data), "data": search_data}
            return HttpResponse(json.dumps(data_list))
        else:
            data_list = {"msg": "没有查询到该条数据！", "count": 0, "data": ''}
            return HttpResponse(json.dumps(data_list))


def project_data(request):
    inter_data = models.Interface_Data.objects.all().values()
    data_list = list(inter_data)
    status_arr = []  # 创建一个列表存放解析出来的status
    data_id = request.POST.get('data_id')
    if data_id != None:
        global new_data_id
        new_data_id = data_id
    for i in data_list:  # 获得列表中的每个字典
        for key, value in i.items():  # 获取字典中的每个字段及value
            if key == 'status' and str(value) == new_data_id and value is not None:  # 只把status存入status_arr列表中
                status_arr.append(i)
            else:
                continue
    data_list = {"code": 200, "msg": "ok", "count": len(status_arr), "data": status_arr}
    return HttpResponse(json.dumps(data_list))

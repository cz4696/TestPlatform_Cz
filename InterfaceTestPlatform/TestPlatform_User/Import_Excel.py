# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import xlrd, xlwt, json, sys
import requests


class cls_api:
    def post(self, url, para):
        a_url = url
        a_par = para
        res = requests.post(a_url, a_par)
        return res

    def get(self, url, para):
        a_url = url
        a_par = para
        res = requests.get(a_url, a_par)
        return res

    def put(self, url, para):
        a_url = url
        a_par = para
        res = requests.put(a_url, a_par)
        return res

    def delete(self, url):
        a_url = url
        res = requests.delete(a_url)
        return res


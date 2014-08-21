# -*- coding:utf-8 -*-
from dmu import json_response


def home(request):
    data = {
        'Hello': 'World!'
    }
    return json_response(data)

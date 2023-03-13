#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/13 15:12
# FileName:

import json

import requests

import conf


def base_request(api_path, method, params=None, data=None, headers=None):
    resp = requests.request(method, url=f'http://localhost:{conf.port}/{api_path}',
                            params=params, json=data,
                            headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        try:
            print(json.dumps(data, indent=4, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(data, indent=4))
    else:
        print(f'{api_path} 请求失败')


def chart():
    api_path = 'dashboard/chart'
    method = 'get'
    params = {

    }
    data = None
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def add():
    api_path = 'dashboard/add'
    method = 'post'
    params = None
    data = {
        'title': '测试',
        'content': '测试文本'
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def update():
    api_path = 'dashboard/update'
    method = 'put'
    params = None
    data = {}
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def remove():
    api_path = 'dashboard/remove'
    method = 'delete'
    params = None
    data = {}
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


if __name__ == '__main__':
    # chart()
    # add()
    # update()
    # remove()

    ...

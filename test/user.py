#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 14:43
# FileName:

import json

import requests

from test import conf


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


def register():
    api_path = 'user/register'
    method = 'post'
    params = None
    data = {
        'name': 'test06',
        'email': 'test06@fq.com',
        'password': 'test06',
        # 'role_id': 'd81054451179d2efae4aa0e56efe4e3c',
        'depart_id': '1852a3143c234e8b2a1f4b64aef2b3cd',
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


# 登录
def login():
    api_path = 'user/login'
    method = 'post'
    params = None
    data = {
        'email': 'default@fq.com',
        'password': 'default',
    }
    headers = None
    return base_request(api_path, method, params=params, data=data, headers=headers)


# 更新
def update():
    api_path = 'user/update'
    method = 'put'
    params = None
    data = {
        'data': {
            'remark': '超管',
        },
        # 'uid': '1e41e116-7ba1-46a8-b9cd-95443897cc4d',
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


# 查询
def info():
    api_path = 'user/info'
    method = 'get'
    params = {
        # 'uids': [],
        # 'emails': ['test01@fq.com', ],
    }
    data = None
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


# 封禁
def ban():
    api_path = 'user/ban'
    method = 'put'
    params = None
    data = {
        'uids': ['af59ccbf-4045-4e80-916c-a40783363b55'],
        'is_ban': 1,
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


if __name__ == '__main__':
    # register()
    # login()
    # update()
    # info()
    # ban()

    ...

#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/11 20:30
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


# 注册
def register():
    api_path = 'user/register'
    method = 'post'
    params = None
    data = {
        'name': 'root',
        'email': 'root@fq.com',
        'password': 'root',
    }
    headers = None
    return base_request(api_path, method, params=params, data=data, headers=headers)


# 登录
def login():
    api_path = 'user/login'
    method = 'post'
    params = None
    data = {
        'email': 'test01@fq.com',
        'password': 'test01',
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
            'remark': '测试用户',
        },
        'uid': '1e41e116-7ba1-46a8-b9cd-95443897cc4d',
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
        'uids': ['1e41e116-7ba1-46a8-b9cd-95443897cc4d'],
        'is_ban': 0,
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

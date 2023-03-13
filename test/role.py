#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/11 22:14
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


def add_role():
    api_path = 'role/add'
    method = 'post'
    params = None
    data = {
        'name': '研发',
        # 'remark': '',
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def remove_role():
    api_path = 'role/remove'
    method = 'delete'
    params = None
    data = {
        'role_ids': ['0c2c49255266ce1c1ecb437274538471', '3363153a98cc9a23042514c5edcc2089'],
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def update_role():
    api_path = 'role/update'
    method = 'put'
    params = None
    data = {
        'data': {
            'remark': '不可更改',
            'parent': ['37f6e32d06c693b98fadaa527441b3b6', 'd4b99354449728c7e6bc4d6709cfe522'],
        },
        'role_id': '9e94b771f74524d058e150f2704294e3'
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def info():
    api_path = 'role/info'
    method = 'get'
    params = {
        # 'role_id': '9e94b771f74524d058e150f2704294e3',
        # 'role_name': '测试',
    }
    data = None
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


if __name__ == '__main__':
    # add_role()
    # remove_role()
    # update_role()
    # info()

    ...

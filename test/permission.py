#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/12 20:09
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


def role_add_user():
    api_path = 'permission/role_add_user'
    method = 'post'
    params = None
    data = {
        'role_id': '9e94b771f74524d058e150f2704294e3',
        'uids': ['1e41e116-7ba1-46a8-b9cd-95443897cc4d'],
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def role_remove_user():
    api_path = 'permission/role_remove_user'
    method = 'DELETE'
    params = None
    data = {
        'data': {
            'role_id': 'a2fee1741f8baa0886cad3160d6a50ff',
            'uids': ['417cb395-2f5a-4d86-9d12-2dcc029477b4'],
        }
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def permission_tree():
    api_path = 'permission/permission_tree'
    method = 'GET'
    params = None
    data = None
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def role_permission():
    api_path = 'permission/role_permission'
    method = 'POST'
    params = None
    data = {
        'role_id': '37f6e32d06c693b98fadaa527441b3b6',
        'data': [
            'demo02.chart:table01', 'demo02.chart:table02', 'demo02.filter:filter01', 'demo02.filter:filter02',
            'demo02.func:demo02/add', 'demo02.func:demo02/update',
        ]
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


if __name__ == '__main__':
    # role_add_user()
    # role_remove_user()
    # permission_tree()
    # role_permission()

    ...

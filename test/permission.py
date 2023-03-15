#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/12 20:09
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


def role_add_user():
    api_path = 'permission/role_add_user'
    method = 'post'
    params = None
    data = {
        'role_id': '080363a4cdd968c5d13998eff79edfcb',
        'uids': ['1d1d36f4-00bc-43f5-99cc-6ebcef490ed2'],
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
            'role_id': '080363a4cdd968c5d13998eff79edfcb',
            'uids': ['1d1d36f4-00bc-43f5-99cc-6ebcef490ed2'],
        }
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def user_roles():
    api_path = 'permission/user_roles'
    method = 'put'
    params = None
    data = {
        'uid': '1d1d36f4-00bc-43f5-99cc-6ebcef490ed2',
        'data': [
            {'role_id': '484db34d5130b75e7d90d586c1ad1d5d'},
            {'role_id': '080363a4cdd968c5d13998eff79edfcb'},
        ]
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def user_depart():
    api_path = 'permission/user_depart'
    method = 'put'
    params = None
    data = {
        'depart_id': 'b3a695fb9b9b3988d198df9f1b9afaae',
        'data': [
            {'uid': '21e3f738-eb9c-4265-9503-e94dd035cd54'},
        ]
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
        'role_id': '34943c5d7b10b5cf65c43a2971c8253c',
        'data': [
            'demo02.chart:table01', 'demo02.chart:table02', 'demo02.filter:filter01', 'demo02.filter:filter02',
            'demo02.func:demo02/add', 'demo02.func:demo02/update',
        ]
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def depart_add_project():
    api_path = 'permission/depart_add_pj'
    method = 'post'
    params = None
    data = {
        'depart_id': '5e86d5d983576d9810de7e8a1f588231',
        'projects': ['pig', 'chicken']
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def depart_remove_project():
    api_path = 'permission/depart_remove_pj'
    method = 'delete'
    params = None
    data = {
        'depart_id': '5e86d5d983576d9810de7e8a1f588231',
        'projects': ['chicken']
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


if __name__ == '__main__':
    # role_add_user()
    # role_remove_user()
    # user_roles()
    # user_depart()
    # permission_tree()
    # role_permission()
    # depart_add_project()
    # depart_remove_project()

    ...

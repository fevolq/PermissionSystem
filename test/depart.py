#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 17:48
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


def add_depart():
    api_path = 'depart/add'
    method = 'post'
    params = None
    data = {
        'name': '服务器',
        # 'parent_id': 'bcd13561e3681fd8027e06d90c1e6ddf'
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def remove_depart():
    api_path = 'depart/remove'
    method = 'delete'
    params = None
    data = {
        'depart_ids': ['9a1d798f1faeb3b95495eda7c0bed565'],
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def update_depart():
    api_path = 'depart/update'
    method = 'put'
    params = None
    data = {
        'depart_id': '89644c18c4e086ac2f9561e191edd4ee',
        'data': {
            # 'remark': '数据仓库',
            'parent_id': 'f9bb9ab827b75a21a623a76ab4c52c89',
        }
    }
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


def info():
    api_path = 'depart/info'
    method = 'get'
    params = {

    }
    data = None
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


if __name__ == '__main__':
    # add_depart()
    # remove_depart()
    # update_depart()
    # info()

    ...

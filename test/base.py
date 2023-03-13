#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/11 20:26
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


def template():
    api_path = 'template/template'
    method = 'get'
    params = None
    data = None
    headers = {
        'token': conf.token,
    }
    return base_request(api_path, method, params=params, data=data, headers=headers)


if __name__ == '__main__':
    template()

    ...

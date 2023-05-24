#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/11 20:16
# FileName:

from flask import Blueprint, request, jsonify

from logic import user_logic
from module.bean import user_util
from utils import util

user_route = Blueprint('user', __name__)


@user_route.route('register', methods=['POST'])
def register():
    query = request.json
    res = user_logic.register(query)
    return jsonify(res)


@user_route.route('login', methods=['POST'])
def login():
    query = request.json
    res = user_logic.login(query)
    return jsonify(res)


# 临时用户
@user_route.route('temp', methods=['POST'])
def temp():
    data = {
        'user-agent': str(request.user_agent),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr)
    }
    md5_value = util.md5(":".join(data.values()))
    res = user_logic.temp_account(md5_value)
    return jsonify(res)


# 更新用户信息
@user_route.route('update', methods=['PUT'])
@user_util.is_login
def update():
    query = request.json
    res = user_logic.update(query)
    return jsonify(res)


# 查询用户
@user_route.route('info', methods=['GET'])
@user_util.is_admin
def info():
    query = request.args
    res = user_logic.info(query)
    return jsonify(res)


# 封禁
@user_route.route('ban', methods=['PUT'])
@user_util.is_admin
def ban():
    query = request.json
    res = user_logic.ban(query)
    return jsonify(res)

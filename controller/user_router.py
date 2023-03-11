#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/11 20:16
# FileName:

from flask import Blueprint, request, jsonify

from logic import user_logic

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


@user_route.route('update', methods=['PUT'])
def update():
    query = request.json
    res = user_logic.update(query)
    return jsonify(res)


@user_route.route('info', methods=['GET'])
# TODO：权限校验——管理员
def info():
    query = request.args
    res = user_logic.info(query)
    return jsonify(res)


# 封禁
@user_route.route('ban', methods=['PUT'])
# TODO：权限校验——管理员
def ban():
    query = request.json
    res = user_logic.ban(query)
    return jsonify(res)

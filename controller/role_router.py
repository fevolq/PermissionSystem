#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/11 21:40
# FileName:

from flask import Blueprint, request, jsonify

from logic import role_logic

role_route = Blueprint('role', __name__)
# TODO：权限校验——管理员


@role_route.route('add', methods=['POST'])
def add_role():
    query = request.json
    res = role_logic.add_role(query)
    return jsonify(res)


@role_route.route('remove', methods=['DELETE'])
def remove_role():
    query = request.json
    res = role_logic.remove_role(query)
    return jsonify(res)


@role_route.route('update', methods=['PUT'])
def update_role():
    query = request.json
    res = role_logic.update_role(query)
    return jsonify(res)


@role_route.route('info', methods=['GET'])
def info():
    query = request.args
    res = role_logic.info(query)
    return jsonify(res)

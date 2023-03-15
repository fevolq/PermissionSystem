#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 17:37
# FileName:

from flask import Blueprint, request, jsonify

from logic import depart_logic
from module.bean import user_util

depart_route = Blueprint('depart', __name__)


# 增加
@depart_route.route('add', methods=['POST'])
@user_util.is_admin
def add_depart():
    query = request.json
    res = depart_logic.add_depart(query)
    return jsonify(res)


# 删除
@depart_route.route('remove', methods=['DELETE'])
@user_util.is_admin
def remove_depart():
    query = request.json
    res = depart_logic.remove_depart(query)
    return jsonify(res)


# 更改
@depart_route.route('update', methods=['PUT'])
@user_util.is_admin
def update_depart():
    query = request.json
    res = depart_logic.update_depart(query)
    return jsonify(res)


# 查询
@depart_route.route('info', methods=['GET'])
@user_util.is_admin
def info():
    query = request.args
    res = depart_logic.info(query)
    return jsonify(res)

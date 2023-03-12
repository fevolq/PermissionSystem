#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/12 17:36
# FileName:

from flask import Blueprint, request, jsonify

from logic import permission_logic
from module.bean import user_util

permission_route = Blueprint('permission', __name__)


@permission_route.route('role_add_user', methods=['POST'])
@user_util.is_admin
def role_add_users():
    query = request.json
    res = permission_logic.role_add_users(query)
    return jsonify(res)


@permission_route.route('role_remove_user', methods=['DELETE'])
@user_util.is_admin
def role_remove_users():
    query = request.json
    res = permission_logic.role_remove_users(query)
    return jsonify(res)

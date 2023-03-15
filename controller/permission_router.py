#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 15:36
# FileName:

from flask import Blueprint, request, jsonify

from logic import permission_logic
from module.bean import user_util

permission_route = Blueprint('permission', __name__)


# 角色添加用户
@permission_route.route('role_add_user', methods=['POST'])
@user_util.is_admin
def role_add_users():
    query = request.json
    res = permission_logic.role_add_users(query)
    return jsonify(res)


# 角色移除用户
@permission_route.route('role_remove_user', methods=['DELETE'])
@user_util.is_admin
def role_remove_users():
    query = request.json
    res = permission_logic.role_remove_users(query)
    return jsonify(res)


# 用户更换角色
@permission_route.route('user_roles', methods=['PUT'])
@user_util.is_admin
def user_roles():
    query = request.json
    res = permission_logic.user_roles(query)
    return jsonify(res)


# 用户部门
@permission_route.route('user_depart', methods=['PUT'])
@user_util.is_admin
def user_depart():
    query = request.json
    res = permission_logic.user_depart(query)
    return jsonify(res)


# 权限树
@permission_route.route('permission_tree', methods=['GET'])
@user_util.is_admin
def permission_tree():
    res = permission_logic.permission_tree()
    return jsonify(res)


# 角色权限赋予
@permission_route.route('role_permission', methods=['POST'])
@user_util.is_admin
def role_permission():
    query = request.json
    res = permission_logic.role_permission(query)
    return jsonify(res)


# 部门中添加项目
@permission_route.route('depart_add_pj', methods=['POST'])
@user_util.is_admin
def depart_add_project():
    query = request.json
    res = permission_logic.depart_add_project(query)
    return jsonify(res)


# 部门中移除项目
@permission_route.route('depart_remove_pj', methods=['DELETE'])
@user_util.is_admin
def depart_remove_project():
    query = request.json
    res = permission_logic.depart_remove_project(query)
    return jsonify(res)

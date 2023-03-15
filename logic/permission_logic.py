#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 15:44
# FileName:

import json

from flask import request

import constant
from dao import sql_builder, mysqlDB
from module.role import Role
from status_code import StatusCode
from utils import util


def role_add_users(query):
    current_user = request.environ['metadata.user']
    role_id = query['role_id']
    users_id = query['uids']
    assert role_id in [role_data['role_id'] for role_data in Role.get_all_data()]
    if role_id in [constant.SuperAdminRoleID, constant.AdminRoleID] and not current_user.is_super_admin():
        # 更改管理员人员，需超管权限
        return {'code': StatusCode.forbidden, 'msg': 'Access Denied'}

    # TODO：冲突校验

    rows = [{
        'role_id': role_id,
        'uid': uid,
        'update_at': util.asia_local_time(),
        'update_by': current_user.email,
    } for uid in users_id]
    sql, args = sql_builder.gen_insert_sqls(constant.UserRoleTable, rows, update_cols=['update_at'])
    res = mysqlDB.execute(sql, args)
    return {'code': StatusCode.success}


def role_remove_users(query):
    current_user = request.environ['metadata.user']
    data = query['data']
    role_id = data['role_id']
    users_id = data['uids']

    assert role_id in [role_data['role_id'] for role_data in Role.get_all_data()]
    if role_id in [constant.SuperAdminRoleID, constant.AdminRoleID] and not current_user.is_super_admin():
        # 更改管理员人员，需超管权限
        return {'code': StatusCode.forbidden, 'msg': 'Access Denied'}

    # TODO：冲突校验

    conditions = {'role_id': {'=': role_id}, 'uid': {'IN': users_id}}
    sql, args = sql_builder.gen_delete_sql(constant.UserRoleTable, conditions=conditions)
    res = mysqlDB.execute(sql, args)
    return {'code': StatusCode.success}


def permission_tree():
    with open('permission_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    permission_data = {}
    for dashboard in data:
        if dashboard.startswith('#'):
            continue

        dashboard_value = {}
        for item, values in data[dashboard].items():
            if item.startswith('#'):
                continue
            values = [f'{dashboard}.{item}:{value}' for value in values]
            dashboard_value[item] = values
        permission_data[dashboard] = dashboard_value
    return {'code': StatusCode.success, 'data': permission_data}


def role_permission(query):
    # 权限更新时，传输该角色所有的权限
    current_user = request.environ['metadata.user']
    role_id = query['role_id']
    data = query['data']
    assert role_id in [role_data['role_id'] for role_data in Role.get_all_data()]\
           and role_id not in [constant.SuperAdminRoleID, constant.AdminRoleID, constant.DefaultRoleID]

    # TODO：权限校验

    # 一个角色的所有权限只占一行
    row = {
        'role_id': role_id,
        'permission': json.dumps(data, indent=4),
        'update_at': util.asia_local_time(),
        'update_by': current_user.email,
    }
    sql, args = sql_builder.gen_insert_sql(constant.RolePermissionTable, row, update_cols=['permission', 'update_at'])
    res = mysqlDB.execute(sql, args)

    return {'code': StatusCode.success}

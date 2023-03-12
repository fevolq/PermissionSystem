#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/12 17:37
# FileName:

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
    return {'code': 200}

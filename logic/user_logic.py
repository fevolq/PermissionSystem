#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 14:27
# FileName:
from flask import request

import constant
from dao import sql_builder, mysqlDB
from module.bean import user_util
from module.depart import Depart
from module.user import User
from status_code import StatusCode
from utils import util, pools


def register(query):
    """
    注册用户，需管理员权限，且需指定部门，角色可指定（存在默认角色）。
    :param query:
    :return:
    """
    current_user: User = request.environ['metadata.user']
    name = query['name']
    email = query['email']
    password = query['password']
    role_id = query.get('role_id', constant.DefaultRoleID)
    depart_id = query['depart_id']
    assert depart_id in [depart_data['depart_id'] for depart_data in Depart.get_all_data()] + [Depart.root_depart_id]
    if User.has_register(email):
        return {'code': StatusCode.is_conflict, 'msg': 'Email address has registered'}
    if role_id in (constant.SuperAdminRoleID, constant.AdminRoleID) and not current_user.is_super_admin():
        return {'code': StatusCode.forbidden, 'msg': 'Access Denied'}

    salt = user_util.gen_salt()
    bcrypt_str = user_util.gen_bcrypt_str(password, salt)
    current_time = util.asia_local_time()
    uid = user_util.gen_uid()
    row = {
        'uid': uid,
        'name': name,
        'email': email,
        'salt': salt,
        'bcrypt_str': bcrypt_str,
        'remark': query.get('remark', None),
        'create_at': current_time,
        'create_by': current_user.email,
        'update_at': current_time,
        'update_by': '',
    }
    sql, args = sql_builder.gen_insert_sql(constant.UserTable, row)
    user_role_row = {
        'uid': uid,
        'role_id': role_id,
        'update_at': current_time,
        'update_by': current_user.email,
    }
    role_sql, role_args = sql_builder.gen_insert_sql(constant.UserRoleTable, user_role_row)
    user_depart_row = {
        'uid': uid,
        'depart_id': depart_id,
        'update_at': current_time,
        'update_by': current_user.email,
    }
    depart_sql, depart_args = sql_builder.gen_insert_sql(constant.UserDepartTable, user_depart_row)
    res = mysqlDB.execute_many([
        {'sql': sql, 'args': args},
        {'sql': role_sql, 'args': role_args},
        {'sql': depart_sql, 'args': depart_args},
    ])
    return {'code': StatusCode.success}


def login(query):
    email = query['email']
    password = query['password']

    record_user = User(email=email)
    if record_user.uid is None:
        return {'code': StatusCode.is_conflict, 'msg': 'error password'}
    if not user_util.check_pwd(password, record_user.salt, record_user.bcrypt_str):
        return {'code': StatusCode.is_conflict, 'msg': 'error password'}
    if record_user.is_ban:
        return {'code': StatusCode.forbidden, 'msg': 'forbidden'}

    token = user_util.gen_token(email)
    user_info = record_user.ui_info()
    user_util.insert_token(token, user_info)

    return {'code': StatusCode.success, 'token': token, 'info': user_info}


def update(query):
    current_user: User = request.environ['metadata.user']
    data = query['data']
    uid = query.get('uid', current_user.uid)
    if uid != current_user.uid:
        if not current_user.is_admin():  # 改他人信息，需管理员权限
            return {'code': StatusCode.forbidden, 'msg': 'Access Denied'}
        if User.user_is_admin(uid) and not current_user.is_super_admin():  # 改其他管理员，需超管权限
            return {'code': StatusCode.forbidden, 'msg': 'Access Denied'}

    # TODO：冲突校验

    can_change_fields = ['name', 'password', 'remark']
    change_fields = {}
    for field, value in data.items():
        if field not in can_change_fields:
            continue
        if field == 'password':
            if uid != current_user.uid:  # 只有自己可更改密码
                continue
            field = 'bcrypt_str'
            value = user_util.gen_bcrypt_str(value, current_user.salt)
        change_fields[field] = value

    if not change_fields:
        return {'code': StatusCode.success}
    change_fields['update_at'] = util.asia_local_time()
    change_fields['update_by'] = current_user.email

    sql, args = sql_builder.gen_update_sql(constant.UserTable, change_fields, conditions={'uid': {'=': uid}})
    res = mysqlDB.execute(sql, args)
    return {'code': StatusCode.success}


def info(query):
    uid_arr = query.getlist('uids')
    uname_arr = query.getlist('unames')
    email_arr = query.getlist('emails')
    page = int(query.get('page', 1))
    page_size = int(query.get('page_size', 20))

    conditions = {}
    if uid_arr:
        conditions['uid'] = {'IN': uid_arr}
    if uname_arr:
        conditions['name'] = {'IN': uname_arr}
    if email_arr:
        conditions['email'] = {'IN': email_arr}
    sql, args = sql_builder.gen_select_sql(constant.UserTable, ['uid'], condition=conditions,
                                           order_by=[('id', 'asc')], limit=page_size, offset=(page - 1) * page_size)
    res = mysqlDB.execute(sql, args)['result']

    args_list = [[{'uid': row['uid']}] for row in res]
    result = pools.execute_event(lambda uid: User(uid), args_list, pools=20, force_pool=True)
    return {'code': StatusCode.success, 'total': len(res), 'data': [user.info() for user in result]}


def ban(query):
    current_user: User = request.environ['metadata.user']
    current_time = util.asia_local_time()

    uid_arr = query['uids']
    is_ban = query.get('is_ban', True)
    is_ban = 1 if is_ban else 0
    if current_user.is_admin(only_admin=True) and User.user_is_admin(uid_arr):  # 管理员不能更改其他管理员
        return {'code': StatusCode.forbidden, 'msg': 'insufficient privileges'}

    # TODO：冲突校验

    update_cols = {'is_ban': is_ban, 'update_at': current_time, 'update_by': current_user.email}
    sql, args = sql_builder.gen_update_sql(constant.UserTable, update_cols, conditions={'uid': {'IN': uid_arr}})
    res = mysqlDB.execute(sql, args)
    return {'code': StatusCode.success}

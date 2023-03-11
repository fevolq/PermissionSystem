#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/11 20:19
# FileName:

import constant
from dao import mysqlDB, sql_builder
from utils import dict_to_obj


class User:

    def __init__(self, uid=None, email=None):
        self.uid = uid
        self.name = None
        self.email = email
        self.salt = None
        self.bcrypt_str = None
        self.is_ban = 0

        self.create_at = None
        self.update_at = None
        self.update_by = None
        self.remark = None

        self.login = False
        self._init()

    def _init(self):
        cols = ['uid', 'name', 'email', 'salt', 'bcrypt_str', 'is_ban', 'create_at', 'update_at', 'update_by', 'remark']
        condition = {}
        if self.uid is not None:
            condition['uid'] = {'=': self.uid}
        if self.email is not None:  # 登录校验
            condition['email'] = {'=': self.email}
        if not condition:
            condition = {'id': {'=': -1}}

        info_sql, info_args = sql_builder.gen_select_sql(constant.UserTable, cols, condition=condition, limit=1)
        res = mysqlDB.execute(info_sql, info_args)['result']
        if not res:
            return

        dict_to_obj.set_obj_attr(self, res[0])
        self.login = True

    @classmethod
    def has_register(cls, email):
        sql = f'SELECT uid FROM {constant.UserTable} WHERE email = %s LIMIT 1'
        res = mysqlDB.execute(sql, [email])['result']
        return res

    # 用户自己可查看的信息
    def ui_info(self):
        return {
            'uid': self.uid,
            'uname': self.name,
            'email': self.email,
        }

    # 管理员可查看的用户信息
    def info(self):
        return {
            'uid': self.uid,
            'uname': self.name,
            'email': self.email,
            'is_ban': self.is_ban,
            'update_at': self.update_at,
            'update_by': self.update_by,
            'remark': self.remark,
        }

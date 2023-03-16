#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/16 20:38
# FileName:

import getopt
import sys

sys.path.append('..')
from dao import sql_builder, mysqlDB
import constant
from module.bean import user_util
from utils import util


class InitData:

    def __init__(self, root_name='root', root_email='root', root_password='root', root_remark='超管'):
        self.root_uid = user_util.gen_uid()
        self.root_name = root_name
        self.root_email = root_email
        self.root_password = root_password
        self.root_remark = root_remark

        self.super_admin_role_id = None
        self.root_depart_id = None

    @staticmethod
    def truncate_table(table):
        sql_list = [
            f'TRUNCATE TABLE {table};',
            f'ALTER TABLE {table} AUTO_INCREMENT = 1;',
        ]
        for sql in sql_list:
            mysqlDB.execute(sql)

    def create_root_user(self):
        self.truncate_table(constant.UserTable)

        salt = user_util.gen_salt()
        bcrypt_str = user_util.gen_bcrypt_str(self.root_password, salt)
        current_time = util.asia_local_time()
        data = {
            'uid': self.root_uid,
            'name': self.root_name,
            'email': self.root_email,
            'salt': salt,
            'bcrypt_str': bcrypt_str,
            'remark': self.root_remark,
            'create_at': current_time,
            'update_at': current_time,
            'create_by': '',
        }
        sql, args = sql_builder.gen_insert_sql(constant.UserTable, data)
        mysqlDB.execute(sql, args)

    def create_init_roles(self):
        """
        创建初始角色：超管、管理员、默认角色
        :return:
        """
        self.truncate_table(constant.RoleTable)

        def gen_role_data(role_name):
            current_time = util.asia_local_time()
            return {
                'role_id': util.gen_unique_str(role_name),
                'name': role_name,
                'parent': None,
                'remark': role_name,
                'create_at': current_time,
                'update_at': current_time,
                'create_by': self.root_email,
            }

        result = {}
        for role in ('超管', '管理员', '默认'):
            data = gen_role_data(role)
            role_id = data['role_id']
            sql, args = sql_builder.gen_insert_sql(constant.RoleTable, data)
            mysqlDB.execute(sql, args)
            result[role] = role_id
        # TODO: 重写入constant文件

        self.super_admin_role_id = result['超管']
        for role, role_id in result.items():
            print(f'【{role}】: {role_id}')

    def create_root_depart(self):
        self.truncate_table(constant.DepartTable)

        current_time = util.asia_local_time()
        depart_name = '企业'
        depart_id = util.gen_unique_str(depart_name)
        data = {
            'depart_id': depart_id,
            'name': depart_name,
            'parent_id': '',
            'remark': '企业',
            'create_at': current_time,
            'update_at': current_time,
            'create_by': self.root_email,
        }
        sql, args = sql_builder.gen_insert_sql(constant.DepartTable, data)
        mysqlDB.execute(sql, args)
        print(f'根部门ID: {depart_id}')
        self.root_depart_id = depart_id

    def associate_root_user_role(self):
        """
        关联root用户的超管权限
        :return:
        """
        self.truncate_table(constant.UserRoleTable)

        data = {
            'uid': self.root_uid,
            'role_id': self.super_admin_role_id,
            'update_at': util.asia_local_time(),
            'update_by': self.root_email,
        }
        sql, args = sql_builder.gen_insert_sql(constant.UserRoleTable, data)
        mysqlDB.execute(sql, args)

    def associate_root_user_depart(self):
        """
        关联root用户的部门
        :return:
        """
        self.truncate_table(constant.UserDepartTable)

        data = {
            'uid': self.root_uid,
            'depart_id': self.root_depart_id,
            'update_at': util.asia_local_time(),
            'update_by': self.root_email,
        }
        sql, args = sql_builder.gen_insert_sql(constant.UserDepartTable, data)
        mysqlDB.execute(sql, args)

    def main(self):
        self.create_root_user()
        self.create_init_roles()
        self.create_root_depart()
        self.associate_root_user_role()
        self.associate_root_user_depart()


if __name__ == '__main__':
    name = 'root'
    email = 'root'
    password = 'root'
    remark = '超管'

    opts, _ = getopt.getopt(sys.argv[1:], 'n:e:p:r:', ['name=', 'email=', 'password=', 'remark='])
    opts = dict(opts)
    if opts.get("-n"):
        name = str(opts.get("-n"))
    elif opts.get("--name"):
        name = str(opts.get("--name"))
    if opts.get("-e"):
        email = str(opts.get("-e"))
    elif opts.get("--email"):
        email = str(opts.get("--email"))
    if opts.get("-p"):
        password = str(opts.get("-p"))
    elif opts.get("--password"):
        password = str(opts.get("--password"))
    if opts.get("-r"):
        remark = str(opts.get("-r"))
    elif opts.get("--remark"):
        remark = str(opts.get("--remark"))

    assert all([name, email, password])

    InitData(root_name=name, root_email=email, root_password=password, root_remark=remark).main()

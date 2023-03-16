#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 17:45
# FileName:

import threading
from typing import List

import constant
from dao import sql_builder, mysqlDB
from utils import dict_to_obj, pools


class Depart:

    all_data = None             # 仅包含基础元素
    __lock = threading.RLock()

    def __init__(self, depart_id):
        # 基础元素
        self.depart_id = depart_id
        self.name = None
        self.remark = None
        self.create_at = None
        self.update_at = None
        self.create_by = None
        self.update_by = None

        # 衍生元素
        self.children: List[Depart] = []

        # 权限元素
        self.users: List[dict] = []
        self.projects = []

        self._init()

    @classmethod
    def get_all_data(cls):
        if cls.all_data is None:
            with cls.__lock:
                if cls.all_data:
                    return cls.all_data

                cols = ['depart_id', 'name', 'remark', 'parent_id', 'create_at', 'update_at', 'create_by', 'update_by']
                sql, args = sql_builder.gen_select_sql(constant.DepartTable, cols)
                res = mysqlDB.execute(sql, args)['result']
                cls.all_data = res
        return cls.all_data

    @classmethod
    def clear_all_data(cls):
        cls.all_data = None

    def _init(self):
        all_depart_data = {depart_data['depart_id']: depart_data for depart_data in self.get_all_data()}

        # 填充属性
        dict_to_obj.set_obj_attr(self, all_depart_data.get(self.depart_id, {}))

        parent_departs = {}  # {parent_id: [depart, ]}
        for row in all_depart_data.values():
            departs = parent_departs.setdefault(row['parent_id'], [])
            departs.append(row)

        children = parent_departs.get(self.depart_id)
        if children:
            args_list = [[(depart_data['depart_id'],)] for depart_data in children]
            self.children = pools.execute_event(lambda depart_id: Depart(depart_id), args_list)

        user_sql = f'SELECT {constant.UserTable}.uid AS uid, {constant.UserTable}.name AS uname ' \
                   f'FROM {constant.UserTable}' \
                   f' LEFT JOIN {constant.UserDepartTable} ON {constant.UserDepartTable}.uid = {constant.UserTable}.uid ' \
                   f'WHERE {constant.UserDepartTable}.depart_id = %s ' \
                   f'ORDER BY {constant.UserTable}.id ASC'
        self.users = mysqlDB.execute(user_sql, [self.depart_id])['result']

        project_sql, project_args = sql_builder.gen_select_sql(constant.DepartProjectTable, ['project'],
                                                               condition={'depart_id': {'=': self.depart_id}},
                                                               order_by=[('id', 'asc')])
        project_res = mysqlDB.execute(project_sql, project_args)['result']
        self.projects = [row['project'] for row in project_res]

    def ui_info(self):
        return {
            'depart_id': self.depart_id,
            'name': self.name,
            'remark': self.remark,
        }

    def info(self):
        return {
            'depart_id': self.depart_id,
            'name': self.name,
            'remark': self.remark,
            'create_at': self.create_at,
            'update_at': self.update_at,
            'create_by': self.create_by,
            'update_by': self.update_by,
            'children': [child.info() for child in self.children],

            'users': self.users,
            'projects': self.projects,
        }

    @classmethod
    def in_tree_node(cls, depart_id, depart_node_id=None):
        """
        depart是否为depart_node延申的某个节点
        :param depart_id:
        :param depart_node_id: 指定的节点
        :return:
        """
        depart_id_set = set()

        def get_children(depart):
            depart_id_set.add(depart.depart_id)
            if depart.children and depart_id not in depart_id_set:      # 已存在，则终止延申
                for child in depart.children:
                    get_children(child)

        get_children(Depart(depart_node_id))

        return depart_id in depart_id_set

    def get_all_projects(self):
        """
        获取所有有权限的项目
        """
        projects = []
        projects.extend(self.projects)

        if self.children:
            for child in self.children:
                chile_projects = child.get_all_projects()
                projects.extend(chile_projects)

        return list(set(projects))

    def has_project(self, project):
        """
        是否有指定项目的权限
        """
        if project in self.projects:
            return True

        if self.children:
            for child in self.children:
                result = child.has_project(project)
                if result:
                    return result
        return False

        # projects = []
        #
        # def get_projects(depart):
        #     projects.extend(depart.projects)
        #     if project not in projects and depart.children:     # 已存在，则终止延申
        #         for child in depart.children:
        #             get_projects(child)
        #
        # get_projects(self)
        # return project in projects

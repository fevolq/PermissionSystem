#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/15 17:44
# FileName:

from flask import request

import constant
from dao import sql_builder, mysqlDB
from module.depart import Depart
from status_code import StatusCode
from utils import util


def add_depart(query):
    current_user = request.environ['metadata.user']

    name = query['name']
    remark = query.get('remark')
    parent_id = query.get('parent_id', constant.RootDepartID)
    all_depart_ids = [depart_data['depart_id'] for depart_data in Depart.get_all_data()]
    if all_depart_ids:
        assert parent_id in all_depart_ids

    current_time = util.asia_local_time()
    row = {
        'depart_id': util.gen_unique_str(name),
        'name': name,
        'parent_id': parent_id,
        'remark': remark,
        'create_at': current_time,
        'update_at': current_time,
        'create_by': current_user.email,
    }
    sql, args = sql_builder.gen_insert_sql(constant.DepartTable, row)
    res = mysqlDB.execute(sql, args)
    Depart.clear_all_data()
    return {'code': StatusCode.success}


def remove_depart(query):
    depart_id_arr = query['depart_ids']     # 可批量

    # TODO：冲突校验

    del_depart_ids = set()
    for depart_id in depart_id_arr:
        del_depart_ids.add(depart_id)

        depart = Depart(depart_id)
        children = depart.children
        while children:
            child = children.pop(0)
            del_depart_ids.add(child.depart_id)
            children.extend(child.children)

    assert constant.RootDepartID not in del_depart_ids

    record_sql, record_args = sql_builder.gen_select_sql(constant.UserDepartTable, ['uid'], condition={'depart_id': {'IN': del_depart_ids}})
    record_res = mysqlDB.execute(record_sql, record_args)['result']
    assert not record_res       # 删除的部门中存在用户，则不能删除，避免用户处于无部门状态

    sql, args = sql_builder.gen_delete_sql(constant.DepartTable, conditions={'depart_id': {'IN': del_depart_ids}})
    res = mysqlDB.execute(sql, args)
    Depart.clear_all_data()
    return {'code': StatusCode.success}


def update_depart(query):
    current_user = request.environ['metadata.user']
    data = query['data']
    depart_id = query['depart_id']

    # TODO：冲突校验

    can_change_fields = ['name', 'parent_id', 'remark']
    change_fields = {field: data[field] for field in can_change_fields if field in data}
    if not change_fields:
        return {'code': StatusCode.success}
    elif 'parent_id' in change_fields:
        all_depart_ids = [depart_data['depart_id'] for depart_data in Depart.get_all_data()]
        assert change_fields['parent_id'] in all_depart_ids

    change_fields['update_at'] = util.asia_local_time()
    change_fields['update_by'] = current_user.email

    sql, args = sql_builder.gen_update_sql(constant.DepartTable, change_fields, conditions={'depart_id': {'=': depart_id}})
    res = mysqlDB.execute(sql, args)
    Depart.clear_all_data()
    return {'code': StatusCode.success}


def info(query):
    depart_id = query.get('depart_id', None)
    depart_name = query.get('depart_name', None)

    conditions = {}
    if depart_name is not None:
        conditions['name'] = {'LIKE': depart_name}
    if depart_id is None:
        conditions['parent_id'] = {'=': ''}
    else:
        conditions['depart_id'] = {'=': depart_id}

    sql, args = sql_builder.gen_select_sql(constant.DepartTable, ['depart_id'], condition=conditions,
                                           order_by=[('id', 'asc')])
    res = mysqlDB.execute(sql, args)['result']
    depart_ids = [row['depart_id'] for row in res]

    departs = (Depart(depart_id_) for depart_id_ in depart_ids)
    return {'code': 200, 'data': [depart.info() for depart in departs]}

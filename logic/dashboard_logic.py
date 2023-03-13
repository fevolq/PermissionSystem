#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/13 13:20
# FileName:

from flask import request

from status_code import StatusCode


def chart(query):
    current_user = request.environ['metadata.user']
    return {'code': StatusCode.success}


def test_add(query):
    return {'code': StatusCode.success}


def test_update(query):
    return {'code': StatusCode.success}


def test_remove(query):
    return {'code': StatusCode.success}

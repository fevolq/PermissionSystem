#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 10:57
# FileName:

from controller import (
    template_router,
    user_router,
    role_router,
)

blueprint = {
    # url_prefix: blueprint
    'template': template_router.template_route,
    'user': user_router.user_route,
    'role': role_router.role_route,
}

#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 10:54
# FileName:

import logging
import time

from flask import Flask, request, jsonify
from gevent import monkey

from config import conf
from middleware import Middleware
from utils import log_init, util
from status_code import StatusCode
from controller import control

if conf.LOAD_PATCH and util.is_linux():
    monkey.patch_all()


# 日志初始化
log_init.init_logging(conf.app_log_path, datefmt='%Y-%m-%d %H:%M:%S')


app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app)
# 跨域
# from flask_cors import CORS
# CORS(
#     app,
#     resources='*',
#     origins='*',
#     methods=['GET', 'POST'],
#     expose_headers='*',
#     allow_headers='*',
#     supports_credentials=True,
# )

for url_prefix, blueprint in control.blueprint.items():
    app.register_blueprint(blueprint, url_prefix=f'/{url_prefix}')
    logging.info(f'register blueprint: {url_prefix}')


@app.before_request
def before_call():
    ...
    # 若不为注册登录接口，则校验用户
    current_user = request.environ['metadata.user']
    if request.path not in ('/user/register', '/user/login',):
        if (not current_user.login) or current_user.is_ban:
            return {'code': StatusCode.forbidden, 'msg': 'token invalidation, please login again'}
    pass


@app.after_request
def after_call(response):
    ...
    response.headers['metadata.spent'] = f'{time.time() - request.environ["metadata.start_time"]} ms'
    response.headers['metadata.require_id'] = request.environ['metadata.require_id']
    return response


@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获
    :param e:
    :return:
    """
    logging.error(e)
    data = {
        'code': StatusCode.failure,
        'msg': '出现未知情况',
    }
    if not conf.catch_error:
        raise e
    return jsonify(data)


@app.route('/', methods=['GET'])
def hello():
    return 'HELLO WORLD!'


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=conf.app_port,
        debug=False,
        threaded=conf.use_thread,
    )

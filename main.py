import os
import time
import argparse
import logging
import pathlib

from internal.server import new_grpc_server
from internal.service.service import new_service
from internal.biz import new_account_use_case, new_company_use_case
from internal.data import new_account_repo, new_company_repo
from internal.data import orm
from internal.data import cache
from internal.modules import logx
from internal.modules import redisx
from internal.modules import lockx
from config import Config


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def _configure_logger():
    logx.Logger(
        pathlib.Path(os.path.join(os.path.dirname(__file__), 'logs')).as_posix(),
        'admin_app.log'
    ).init()


def _register_server(svc_port: int):
    # -----------repo------------
    account_use_case = new_account_use_case(new_account_repo())
    company_use_case = new_company_use_case(new_company_repo())

    # -----------biz------------
    api_svc = new_service(account_use_case, company_use_case)

    with open('./secret-key/server.key', 'rb') as f:
        private_key = f.read()

    with open('./secret-key/server.crt', 'rb') as f:
        certificate = f.read()

    rpc = new_grpc_server(
        svc_port,
        api_svc,
        workers=10,
        options=[
            ('grpc.max_send_message_length', 100 * 1024 * 1024),
            ('grpc.max_receive_message_length', 100 * 1024 * 1024)
        ],
        private_key=private_key,
        certificate=certificate
    )

    rpc.serve()

    logging.info(f'grpc server start successful, port: {svc_port}')

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        rpc.server.stop(0)


def _init_redis():
    conf = Config.REDIS()
    redisx.redis = redisx.new_client(**conf.dict())


def _init_cache():
    cache.sess = cache.new_cache_session(redisx.redis)


def _init_distributed_lock(pool: int = 10):
    lockx.lock_pool = lockx.LockPool(pool)
    for _ in range(pool):
        lockx.lock_pool.put(lockx.Lock(redisx.Lock(client=redisx.redis)))


def init_new_modules():
    """modules init factory function"""
    _init_redis()
    _init_distributed_lock()
    _init_cache()


def main():
    """main func"""
    parse = argparse.ArgumentParser()
    parse.add_argument('--svc_port', type=int, default=30003)
    parse.add_argument('--db_ep', type=str, default='127.0.0.1:3306')
    parse.add_argument('--db_auth', type=str, default='root:123456')
    parse.add_argument('--db_name', type=str, default='admin_application_db')

    args = parse.parse_args()

    # ============log=============
    _configure_logger()

    # =============db=============
    orm.db = orm.new_database_handler(
        db_ep=args.db_ep,
        db_auth=args.db_auth,
        db_name=args.db_name,
        charset='utf8mb4'
    )

    # ============grpc server================
    _register_server(args.svc_port)

    # ============factory func===============
    init_new_modules()


if __name__ == '__main__':
    main()

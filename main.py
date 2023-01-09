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
from internal.modules.logx import Logger


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def _register_server(svc_ep: str):
    # -----------repo------------
    account_use_case = new_account_use_case(new_account_repo())
    company_use_case = new_company_use_case(new_company_repo())

    # -----------biz------------
    api_svc = new_service(account_use_case, company_use_case)

    rpc = new_grpc_server(
        svc_ep,
        api_svc,
        workers=10,
        options=[('grpc.max_receive_message_length', 30 * 1024 * 1024)]
    )

    rpc.serve()

    logging.info(f'grpc server register successful, endpoint: {svc_ep}')

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        rpc.server.stop(0)


def main():
    """main func"""
    parse = argparse.ArgumentParser()
    parse.add_argument('--svc_ep', type=str, default='127.0.0.1:30003')
    parse.add_argument('--db_ep', type=str, default='127.0.0.1:3306')
    parse.add_argument('--db_auth', type=str, default='root:123456')
    parse.add_argument('--db_name', type=str, default='admin_application_db')

    args = parse.parse_args()

    # ============log=============
    Logger(
        pathlib.Path(os.path.join(os.path.dirname(__file__), 'logs')).as_posix(),
        'admin_app.log'
    ).init()

    # =============db=============
    orm.db = orm.new_database_handler(
        db_ep=args.db_ep,
        db_auth=args.db_auth,
        db_name=args.db_name,
        charset='utf8mb4'
    )

    # ============grpc server================
    _register_server(args.svc_ep)


if __name__ == '__main__':
    main()

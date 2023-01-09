import typing as t
from concurrent import futures
import logging

import grpc


class ErrEndpointIsNullException(Exception):
    """endpoint is null"""


class GRPCServer:
    """gRPC server"""

    def __init__(
            self,
            svc_port: int,
            api_svc: object,
            workers: int,
            options: t.Optional[t.List[t.Tuple]],
            register_func: t.Callable,
            private_key: t.Optional[t.AnyStr] = None,
            certificate: t.Optional[t.AnyStr] = None
    ):
        """

        :param svc_port: port
        :param api_svc: api 服务
        :param workers: 工作线程数
        :param options: grpc options
        :param register_func: grpc api 注册函数
        :param private_key: 秘钥, 为空使用非安全模式
        :param certificate: 证书, 为空使用非安全模式
        """
        self._svc_port = svc_port
        self._options = options if options else [('grpc.max_receive_message_length', 30 * 1024 * 1024)]
        self._workers = workers
        self._api_svc = api_svc
        self.server = None
        self._register_func = register_func
        self._private_key = private_key
        self._certificate = certificate

    def serve(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._workers), options=self._options)
        self._register_func(self._api_svc, self.server)

        if not self._svc_port:
            raise ErrEndpointIsNullException

        if not self._private_key or not self._certificate:
            logging.info('insecure mode')
            self.server.add_insecure_port(f'[::]:{self._svc_port}')
        else:
            logging.info('TSL/SSL mode')
            server_credentials = grpc.ssl_server_credentials(
                ((self._private_key, self._certificate),)
            )
            self.server.add_secure_port(f'[::]:{self._svc_port}', server_credentials)

        self.server.start()

        logging.info('start grpc server...')

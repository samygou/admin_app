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
            svc_ep: str,
            api_svc: object,
            workers: int,
            options: t.Optional[t.List[t.Tuple]],
            register_func: t.Callable,
            private_key: str = None,
            certificate: str = None
    ):
        """

        :param svc_ep: endpoint
        :param api_svc: api 服务
        :param workers: 工作线程数
        :param options: grpc options
        :param register_func: grpc api 注册函数
        :param private_key: 秘钥, 为空使用非安全模式
        :param certificate: 证书, 为空使用非安全模式
        """
        self._svc_ep = svc_ep
        self._options = options if options else [('grpc.max_receive_message_length', 30 * 1024 * 1024)]
        self._workers = workers
        self._api_svc = api_svc
        self.server = None
        self._register_func = register_func
        self._private_key = private_key
        self._certificate = certificate

    def serve(self):
        # TODO: 目前只实现非安全模式, 安全模式待实现
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._workers), options=self._options)
        self._register_func(self._api_svc, self.server)

        if not self._svc_ep:
            raise ErrEndpointIsNullException

        self.server.add_insecure_port(self._svc_ep)
        self.server.start()

        logging.info('start grpc server...')

from functools import wraps
import typing as t
import logging
import traceback


from api.app.v1 import admin_pb2 as api_admin_pb2
from internal.biz import BIZException


class APIExceptionHandler:
    """处理api exception"""
    def __init__(self, resp_func: t.Callable):
        """

        :param resp_func: 响应函数
        """
        self._resp_func = resp_func

    def __call__(self, func) -> t.Callable:
        @wraps(func)
        def wrappers(*args, **kwargs) -> t.Callable:
            try:
                return func(*args, **kwargs)
            except BIZException.ErrInternalServer:
                return self._resp_func(err=api_admin_pb2.SERVER_FAULT)
            except BIZException.ErrAccountNotFound:
                return self._resp_func(err=api_admin_pb2.ACCOUNT_NOT_EXIST)
            except Exception as e:
                logging.error(e)
                traceback.print_exc()
                return self._resp_func(err=api_admin_pb2.SERVER_FAULT)

        return wrappers

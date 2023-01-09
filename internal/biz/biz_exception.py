class BIZException:
    """biz level exception"""

    class ErrInternalServer(Exception):
        """服务内部错误异常"""

    class ErrAccountNotFound(Exception):
        """账户不存在异常"""

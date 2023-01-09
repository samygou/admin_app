import typing as t

from api.app.v1 import admin_pb2_grpc as api_admin_pb2_grpc
from internal.service.service import AdminServicer
from internal.modules.grpcx import GRPCServer


# 设置只能从包中导出, 不允许从包文件导出
__all__ = []


def new_grpc_server(
        svc_port: int,
        api_svc: AdminServicer,
        workers: int = 10,
        options: t.List[t.Tuple] = None,
        private_key: t.Optional[t.AnyStr] = None,
        certificate: t.Optional[t.AnyStr] = None
) -> GRPCServer:
    # 运行服务, 并把服务句柄保存到类属性
    return GRPCServer(
        svc_port,
        api_svc,
        workers,
        options,
        api_admin_pb2_grpc.add_AdminServicer_to_server,
        private_key=private_key,
        certificate=certificate
    )

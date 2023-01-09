import typing as t

from api.app.v1 import admin_pb2_grpc as api_admin_pb2_grpc
from internal.service.service import AdminService
from internal.modules.grpcx import GRPCServer


# 设置只能从包中导出, 不允许从包文件导出
__all__ = []


def new_grpc_server(
        svc_ep: str,
        api_svc: AdminService,
        workers: int = 10,
        options: t.List[t.Tuple] = None) -> GRPCServer:
    # 运行服务, 并把服务句柄保存到类属性
    return GRPCServer(
        svc_ep,
        api_svc,
        workers,
        options,
        api_admin_pb2_grpc.add_AdminServicer_to_server
    )

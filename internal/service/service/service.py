import logging

from api.app.v1 import admin_pb2_grpc as api_admin_pb2_grpc
from api.app.v1 import admin_pb2 as api_admin_pb2
from internal.biz import AccountUseCase, CompanyUseCase
from internal.modules.limitx import PageLimit
from internal.service.exception import APIExceptionHandler


# 设置只能从包中导出, 不允许从包文件导出
__all__ = []


class AdminServicer(api_admin_pb2_grpc.AdminServicer):
    """service 实例, grpc服务"""

    __slots__ = ('_accountUseCase', '_companyUseCase')

    def __init__(
            self,
            accountUseCase: AccountUseCase,
            companyUseCase: CompanyUseCase
    ):
        self._accountUseCase = accountUseCase
        self._companyUseCase = companyUseCase

    @APIExceptionHandler(api_admin_pb2.GetAccountByPhoneReply)
    def GetAccountByPhone(self, request, context):
        logging.info('GetAccountByPhone api')

        account = self._accountUseCase.get_account_by_phone(request.phone)

        account = None if not account else \
            api_admin_pb2.Account(
                uid=account.uid,
                name=account.username,
                phone=account.phone,
                remark=account.remark
            )

        return api_admin_pb2.GetAccountByUIDReply(account=account, err=api_admin_pb2.OK)

    @APIExceptionHandler(api_admin_pb2.GetAccountByUIDReply)
    def GetAccountByUID(self, request, context):
        logging.info('GetAccountByUID api')

        account = self._accountUseCase.get_account_by_uid(request.uid)

        account = None if not account else \
            api_admin_pb2.Account(
                uid=account.uid,
                name=account.username,
                phone=account.phone,
                remark=account.remark
            )

        return api_admin_pb2.GetAccountByUIDReply(account=account, err=api_admin_pb2.OK)

    @APIExceptionHandler(api_admin_pb2.ListCompaniesReply)
    def ListCompanies(self, request, context):
        logging.info('ListCompanies api')

        companies = self._companyUseCase.list_companies(page_limit=None)
        out = []
        for company in companies:
            tmp_com = api_admin_pb2.Company(
                uid=company.uid,
                name=company.name,
                modules=company.modules,
                expired=company.expired,
            )
            tmp_com.config.algConfig.inventory = company.config
            out.append(tmp_com)

        return api_admin_pb2.ListCompaniesReply(companies=out, err=api_admin_pb2.OK)

    @APIExceptionHandler(api_admin_pb2.ListCompaniesReply)
    def ListCompaniesByUIDs(self, request, context):
        logging.info('ListCompaniesByUIDs api')

        companies = self._companyUseCase.list_companies_by_uids(request.uid, page_limit=None)
        out = []
        for company in companies:
            tmp_com = api_admin_pb2.Company(
                uid=company.uid,
                name=company.name,
                modules=company.modules,
                expired=company.expired,
            )
            tmp_com.config.algConfig.inventory = company.config
            out.append(tmp_com)

        return api_admin_pb2.ListCompaniesReply(companies=out, err=api_admin_pb2.OK)


def new_service(
        account_use_case: AccountUseCase,
        company_use_case: CompanyUseCase,
) -> AdminServicer:
    return AdminServicer(account_use_case, company_use_case)

import typing as t

from pydantic import BaseModel
from zope.interface import Interface

from internal.modules.limitx import PageLimit
from .biz_exception import BIZException


# 设置只能从包中导出, 不允许从包文件导出
__all__ = []


class AuthSendSmsReq(BaseModel):
    phone: str
    type: str


class AuthLoginReq(BaseModel):
    phone: str
    sms_token: str
    code: str


class Account(BaseModel):
    uid: str
    username: str
    phone: str
    remark: str


class IAccountRepo(Interface):
    """account data level interface"""

    def exist_account_by_phone(self, phone: str) -> bool:
        """
        判断账户是否存在
        :param phone: phone number
        :return: bool, is exist or not
        """""

    def get_account_by_phone(self, phone: str) -> t.Optional[Account]:
        """

        :param phone:
        :return:
        """

    def exist_account_by_uid(self, uid: str) -> bool:
        """

        :param uid: unique id
        :return:
        """

    def get_account_by_uid(self, uid: str) -> t.Optional[Account]:
        """

        :param uid: unique id
        :return:
        """


class AccountUseCase:
    """account biz use case"""

    __slots__ = ('_repo', )

    def __init__(self, repo: IAccountRepo):
        self._repo = repo

    def get_account_by_phone(self, phone: str) -> t.Optional[Account]:
        """

        :param phone: phone number
        :return:
        """
        if not self._repo.exist_account_by_phone(phone):
            raise BIZException.ErrAccountNotFound('account not found')

        account = self._repo.get_account_by_phone(phone)

        return account

    def get_account_by_uid(self, uid: str) -> t.Optional[Account]:
        """
        通过 uid 获取账号
        :param uid: unique id
        :return:
        """
        if not self._repo.get_account_by_uid(uid):
            raise BIZException.ErrAccountNotFound('account not found')

        account = self._repo.get_account_by_uid(uid)

        return account


def new_account_use_case(repo: IAccountRepo) -> AccountUseCase:
    return AccountUseCase(repo)

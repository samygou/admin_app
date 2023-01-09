import typing as t

from zope.interface.declarations import implementer

from internal.biz import IAccountRepo, Account, BIZException
from . import orm


# 设置只能从包中导出, 不允许从包文件导出
__all__ = []


@implementer(IAccountRepo)
class AccountRepo:
    """account data level"""

    def __init__(self):
        """"""

    def exist_account_by_phone(self, phone: str) -> bool:
        """

        :param phone: phone number
        :return:
        """
        sql = f"""SELECT 1 FROM accounts WHERE phone = {phone} LIMIT 1"""

        with orm.DBSession(orm.db) as sess:
            result = sess.execute(sql)
            if not result:
                raise BIZException.ErrAccountNotFound('account not found')

        return True

    def get_account_by_phone(self, phone: str) -> t.Optional[Account]:
        """

        :param phone: phone number
        :return:
        """
        sql = f"""SELECT uid, username, phone, remark FROM accounts WHERE phone = {phone} LIMIT 1"""
        with orm.DBSession(orm.db) as sess:
            account = sess.execute_fetchall(sql)
            account = Account(**account[0]) if account else None

        return account

    def exist_account_by_uid(self, uid: str) -> bool:
        """

        :param uid:
        :return:
        """
        sql = f"""SELECT 1 FROM accounts WHERE uid = {uid} LIMIT 1"""

        with orm.DBSession(orm.db) as sess:
            result = sess.execute(sql)
            if not result:
                raise BIZException.ErrAccountNotFound('account not found')

        return True

    def get_account_by_uid(self, uid: str) -> t.Optional[Account]:
        """

        :param uid:
        :return:
        """
        sql = f"""SELECT uid, username, phone, remark FROM accounts WHERE uid = {uid} LIMIT 1"""
        with orm.DBSession(orm.db) as sess:
            account = sess.execute_fetchall(sql)
            account = Account(**account[0]) if account else None

        return account


def new_account_repo() -> AccountRepo:
    return AccountRepo()

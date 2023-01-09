import typing as t
import json

from zope.interface.declarations import implementer

from internal.biz import ICompanyRepo, Company
from internal.modules.limitx import PageLimit
from . import orm


# 设置只能从包中导出, 不允许从包文件导出
__all__ = []


@implementer(ICompanyRepo)
class CompanyRepo:
    """company repo level"""

    def __init__(self):
        """初始化"""

    def list_companies(self, page_limit: t.Optional[PageLimit]) -> t.List:
        """
        获取公司列表
        :param page_limit: 分页信息, 可为None, None表示获取全部数据
        :return:
        """
        with orm.DBSession(orm.db) as sess:
            out = []

            sql = f"""SELECT uid, name, modules, expired, config FROM company"""
            if page_limit:
                sql = f"""{sql} LIMIT {page_limit.offset}, {page_limit.size}"""

            results = sess.execute_fetchall(sql)
            for result in results:
                result['modules'] = json.loads(result['modules'])
                company = Company(**result)
                out.append(company)

        return out

    def list_companies_by_uids(self, uids: t.List[str], page_limit: t.Optional[PageLimit]) -> t.List:
        """
        根据uids获取公司列表
        :param uids: unique ids
        :param page_limit: 分页信息, 可为None, 为None表示获取全部数据
        :return:
        """
        with orm.DBSession(orm.db) as sess:
            out = []

            uids = ','.join(uids)
            sql = f"""SELECT uid, name, modules, expired, config FROM company WHERE uid IN({uids})"""
            if page_limit:
                sql = f"""{sql} LIMIT {page_limit.offset}, {page_limit.size}"""

            results = sess.execute_fetchall(sql)
            for result in results:
                result['modules'] = json.loads(result['modules'])
                company = Company(**result)
                out.append(company)

        return out


def new_company_repo() -> CompanyRepo:
    return CompanyRepo()

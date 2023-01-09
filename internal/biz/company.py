import typing as t

from zope.interface import Interface
from pydantic import BaseModel


from internal.modules.limitx import PageLimit


# 设置只能从包中导出, 不允许从包文件导出
__all__ = []


class Company(BaseModel):
    uid: str = ''
    name: str = ''
    modules: t.List = []
    expired: int = 0
    config: str = ''


class ICompanyRepo(Interface):
    """company repo interface"""
    def list_companies(self, page_limit: t.Optional[PageLimit]) -> t.List[Company]:
        """
        获取公司列表
        :param page_limit: 分页信息, 可为None, None表示获取全部数据
        :return:
        """

    def list_companies_by_uids(
            self,
            uids: t.List[str],
            page_limit: t.Optional[PageLimit]
    ) -> t.List[Company]:
        """
        根据unique ids获取公司列表
        :param uids: list unique id
        :param page_limit: page limit parameter
        :return:
        """


class CompanyUseCase:
    """company use case"""

    __slots__ = ('_repo', )

    def __init__(
            self,
            repo: ICompanyRepo,
    ):
        self._repo = repo

    def list_companies(self, page_limit: t.Optional[PageLimit]) -> t.List[Company]:
        """
        获取公司列表
        :param page_limit: 分页信息, 可为None, None表示获取全部数据
        :return:
        """

        return self._repo.list_companies(page_limit)

    def list_companies_by_uids(
            self,
            uids: t.List[str],
            page_limit: t.Optional[PageLimit]
    ) -> t.List[Company]:
        """
        根据unique ids获取公司列表
        :param uids: list unique id
        :param page_limit: page limit parameter
        :return:
        """

        return self._repo.list_companies_by_uids(uids, page_limit)


def new_company_use_case(repo: ICompanyRepo) -> CompanyUseCase:
    return CompanyUseCase(repo)

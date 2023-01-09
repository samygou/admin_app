import typing as t
import logging

import pymysql
from dbutils.pooled_db import PooledDB

from internal.modules.utils import Singleton
from config import Config


class DatabaseHandle(Singleton):
    """db handle"""
    __slots__ = ["__pool"]

    def __init__(self, conf: t.Union[Config.DB, t.Dict[str, t.Union[str, int]]] = None):
        if isinstance(conf, dict):
            db_conf = Config.DB(**conf)
        else:
            db_conf = Config.DB()

        self.__pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=200,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=20,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=0,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，
            # 所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：
            # 0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created,
            # 4 = when a query is executed, 7 = always
            host=db_conf.host,
            port=db_conf.port,
            user=db_conf.user,
            password=db_conf.password,
            database=db_conf.db,
            charset=db_conf.charset,
        )

        self._conn = self.__pool.connection()
        self._cursor = None

    def open(self):
        self._cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
        return self

    def close_cursor(self):
        self._cursor.close()

    def close(self):
        self.close_cursor()
        self._conn.close()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def execute(self, sql: str, args: t.Union[t.List, t.Tuple, t.Dict] = None) -> int:
        return self._cursor.execute(sql, args)

    def execute_fetchall(self, sql: str, args: t.Union[t.Tuple, t.List, t.Dict] = None) -> t.Tuple:
        self._cursor.execute(sql, args)
        results = self._cursor.fetchall()

        return tuple(results)


class DBSession:
    """db content manager"""
    def __init__(self, sess: DatabaseHandle):
        self._sess = sess.open()

    def __enter__(self):
        return self._sess

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._sess.commit()
            self._sess.close_cursor()
        except Exception as e:
            logging.error(f'db session commit failed: {e}')
            self._sess.rollback()


def new_database_handler(
        db_ep: str = None,
        db_auth: str = None,
        db_name: str = None,
        charset: str = None
) -> DatabaseHandle:
    """

    :param db_ep: database endpoint, 格式: host:port
    :param db_auth: database auth: 格式: user:password
    :param db_name: database name
    :param charset: charset
    :return: database handler
    """
    logging.info('start connection db...')

    conf = Config.DB()
    if db_ep:
        conf.host, conf.port = db_ep.split(':', 1)
    if db_auth:
        conf.user, conf.password = db_auth.split(':', 1)
    if db_name:
        conf.db = db_name
    if charset:
        conf.charset = charset

    return DatabaseHandle(conf)


db: t.Optional[DatabaseHandle] = None

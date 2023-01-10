import typing as t

from . import session


__all__ = [
    'DBSession',
    'db',
    'new_database_handler'
]

DBSession = session.DBSession
DatabaseHandle = session.DatabaseHandle
db: t.Optional[DatabaseHandle] = None
new_database_handler = session.new_database_handler

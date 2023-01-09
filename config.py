from pydantic import BaseModel


class Config:

    class DB(BaseModel):
        host: str = '127.0.0.1'
        port: int = 3306
        user: str = 'root'
        password: str = '123456'
        db: str = 'admin_application_db'
        charset: str = 'utf8mb4'

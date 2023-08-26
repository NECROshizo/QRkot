from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Представляет пользователя в базе данных.
    #### Attributes:
        - id (int): ID пользователя в базе данных. PrimaryKey
        - email (str): Электронная почта пользователя.
        - hashed_password (str): Зашифрованный пароль пользователя.
        - is_active (bool): Указывает, активен ли пользователь.
        - is_superuser (bool): Указывает, является ли пользователь суперпользователем.
        - is_verified (bool): Указывает, подтверждена ли электронная почта пользователя.
    """
    pass

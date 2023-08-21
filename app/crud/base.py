from typing import (
    Dict, Generic, List, Optional, Type, TypeVar, Union)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(
            self,
            model: Type[ModelType]
    ):
        self.model = model

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        """
        Получить объект типа ModelType по определенному значению атрибута.
        #### Args:
            - attr_name(str): Название атрибута.
            - attr_value(str): Значение атрибута.
            - session(AsyncSession): Сеанс для выполнения запроса к базе данных.
        #### Returns:
            - Optional[ModelType]: Объект с указанным значением атрибута, если найдено;
            иначе None.
        """
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        """
        Получить объект типа ModelType по его идентификатору.
        #### Args:
            - obj_id(int): Идентификатор объекта.
            - session(AsyncSession): Сеанс для выполнения запроса к базе данных.
        #### Returns:
            - Optional[ModelType]: Объект с указанным идентификатором, если найдено;
            иначе None.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        """
        Получает все объекты модели из базы данных, используя указанную сессию.
        #### Args:
            - session(AsyncSession): Сессия для выполнения запроса.
        #### Returns:
            - List[ModelType]: Список всех объектов модели из базы данных.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: Optional[AsyncSession] = None,
            user: Optional[User] = None,
    ) -> ModelType:
        """
        Создает новый объект модели в базе данных, используя указанную сессию.
        #### Args:
            - obj_in(CreateSchemaType): Данные для создания нового объекта модели.
            - session(Optional[AsyncSession]): Сессия для выполнения запроса,
              если она указана.
            - user(Optional[User]): Пользователь, если он указан.
        #### Returns:
            - ModelType: Созданный объект модели.
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data, invested_amount=0)
        if session is not None:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: Union[Dict, UpdateSchemaType],
            session: AsyncSession,
    ) -> ModelType:
        """
        Обновляет существующий объект модели в базе данных, используя указанную сессию.
        #### Args:
            - db_obj(ModelType): Существующий объект модели.
            - obj_in(Union[Dict, UpdateSchemaType]): Данные для обновления объекта модели.
            - session(AsyncSession): Сессия для выполнения запроса.
        #### Returns:
            - ModelType - Обновленный объект модели.
        """
        if isinstance(obj_in, BaseModel):
            obj_in = obj_in.dict(exclude_unset=True)
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        """
        Удаляет существующий объект модели из базы данных, используя указанную сессию.
        #### Args:
            - db_obj(ModelType):Существующий объект модели.
            - session(AsyncSession): Сессия для выполнения запроса.
        #### Returns:
            - ModelType: Удаленный объект модели.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

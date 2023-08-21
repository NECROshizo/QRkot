from datetime import datetime
from typing import AsyncGenerator, Tuple

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import BaseModel, CharityProject, Donation


async def get_open_obj_generate(
        model: BaseModel,
        session: AsyncSession = Depends(get_async_session)
) -> AsyncGenerator[BaseModel, None]:
    """
    Асинхронный генератор генерует не закрытые объекты из базы данных
    #### Args:
        - model (BaseModel): Экземпляр базовой модели.
        - session (AsyncSession) асинхронная сессия базы данных.
    Добавлена через Depends.
    #### Returns:
        - AsyncGenerator[BaseModel, None]: Генерин=рует объекты BaseModel.
    """
    query_open_obj = await session.execute(
        select(model)
        .where(model.fully_invested == 0)
        .order_by(model.create_date)
    )
    list_open_obj = query_open_obj.scalars().all()
    for obj in list_open_obj:
        yield obj


async def close_obj(
        obj: BaseModel,
) -> None:
    """
    Закрывает инвестиции в объект
    #### Args:
        - obj (BaseModel): Экземпляр базовой модели.
    """
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()
    obj.fully_invested = True


async def just_do_investing(
    obj_giving: BaseModel,
    obj_receiving: BaseModel,
) -> Tuple[BaseModel]:
    """
    Переводит средства между двумя объектами,
    обновляя их инвестированные суммы и закрывая их при необходимости.
    #### Args:
        - obj_giving (BaseModel): Объект, с которого переводятся средства.
        - obj_receiving (BaseModel): Объект, которому переводятся средства.
    #### Returns:
        - Tuple[BaseModel]: Кортеж, содержащий обновленные объекты
        obj_giving и obj_receiving.
    """
    transferred_amount = obj_giving.full_amount - obj_giving.invested_amount
    required_amount = obj_receiving.full_amount - obj_receiving.invested_amount
    if required_amount == transferred_amount:
        await close_obj(obj_giving)
        await close_obj(obj_receiving)
    elif required_amount > transferred_amount:
        await close_obj(obj_giving)
        obj_receiving.invested_amount += transferred_amount
    else:
        obj_giving.invested_amount += required_amount
        await close_obj(obj_receiving)
    return obj_giving, obj_receiving


async def invest_process(
    obj_in: BaseModel,
    session: AsyncSession,
) -> BaseModel:
    """
    Запускает процесс инвестирования при создание нового объекта участника инвестирования
    #### Args:
        - obj_in (BaseModel): Объект, который нужно инвестировать
        - session (AsyncSession): Асинхронная сессия для работы с базой данных
    #### Returns:
        - BaseModel: Обновленный объект obj_in после завершения инвестиций
    """
    if isinstance(obj_in, Donation):
        open_obj = get_open_obj_generate(CharityProject, session)
    else:
        open_obj = get_open_obj_generate(Donation, session)
    add_obj = []
    async for obj_receiving in open_obj:
        obj_in, obj_receiving = await just_do_investing(
            obj_in, obj_receiving)
        add_obj.append(obj_receiving)
        if obj_in.fully_invested:
            break
    add_obj.append(obj_in)

    for obj in add_obj:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

    return obj_in

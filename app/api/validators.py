from datetime import datetime
from http import HTTPStatus as st

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate
from app.services import StringValidatorsError as const


async def check_full_amount(
    project_in: CharityProjectUpdate,
    project: CharityProject,
) -> CharityProject:
    """
    Проверка суммы вложений и коррекция объекта
    #### Args:
        project_in (CharityProjectUpdate): Обновленный объект проекта
        project (CharityProject): Исходный объект проекта
    #### Returns:
        CharityProject: Обновленный объект проекта
    #### Raises:
        HTTPException: Если сумма вложений меньше суммы, уже инвестированной в проект
    """
    if project_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=st.BAD_REQUEST,
            detail=const.AMOUNT_LESS,
        )
    elif project_in.full_amount == project.invested_amount:
        project_in = {
            **project_in.dict(exclude_unset=True),
            'close_date': datetime.now(),
            'fully_invested': True,
        }
    return project_in


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """
    Проверка имени на дубликаты
    #### Args:
        project_name (str): Имя проекта
        session (AsyncSession): Сессия для обращения к базе данных
    #### Raises:
        HTTPException: Если имя проекта уже существует
    """
    project = await charity_project_crud.get_by_attribute(
        'name', project_name, session)
    if project is not None:
        raise HTTPException(
            status_code=st.BAD_REQUEST,
            detail=const.NAME_EXISTS,
        )


async def check_project_close(project: CharityProject) -> None:
    """
    Проверка закрытости проекта
    #### Args:
        project (CharityProject): Объект проекта
    #### Raises:
        HTTPException: Если проект уже закрыт
    """
    if project.fully_invested:
        raise HTTPException(
            status_code=st.BAD_REQUEST,
            detail=const.CLOSED_PROJECT
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверка существования проекта
    #### Args:
        project_id (int): Идентификатор проекта
        session (AsyncSession): Сессия для обращения к базе данных
    #### Returns:
        CharityProject: Объект проекта
    #### Raises:
        HTTPException: Если проект с указанным идентификатором не найден
    """
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=st.NOT_FOUND,
            detail=const.NOT_FOUND
        )
    return project


async def check_project_start(project: CharityProject) -> None:
    """
    Проверка наличия средств у проекта
    #### Args:
        project (CharityProject): Объект проекта
    #### Raises:
        HTTPException: Если у проекта уже есть средства
    """
    if project.invested_amount:
        raise HTTPException(
            status_code=st.BAD_REQUEST,
            detail=const.FUNDS_PROJECT
        )

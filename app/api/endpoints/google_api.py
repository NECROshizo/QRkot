from typing import Dict, Union
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services import StringGoogleApi as const
from app.services import (
    set_user_permissions, spreadsheets_update_value, spreadsheets_create)

router = APIRouter()


@router.post(
    '/',
    summary=const.GET_CREATE,
    description=const.GET_CREATE_DESCRIPTION,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

) -> Dict[str, Union[str, Dict[str, str]]]:
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    """
    Получение списка всех благотворительных проектов
    #### Args:
        - session (AsyncSession) асинхронная сессия базы данных.
        - wrapper_services (Aiogoogle): Объект Aiogoogle,
    используемый для взаимодействия с Google Drive API.
    Добавлена через Depends.
    #### Returns:
        - Dict[str, Union[str, Dict[str,str]]]: возвращает ссылку на
        сформированный отчет и список данных что включенны в отчет
    """
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id,
                                    projects,
                                    wrapper_services)

    return {
        'URL': f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}',
        'data': projects
    }

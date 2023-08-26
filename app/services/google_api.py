from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Создает новую Google таблицу.
    #### Args:
    - wrapper_services (Aiogoogle): Экземпляр библиотеки Aiogoogle.
    #### Returns:
    - str: ID новой созданной таблицы.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 7}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """
    Устанавливает разрешения пользователю для
    электронной таблицы в Google Drive
    #### Args:
    - spreadsheetid (строка): Идентификатор электронной таблицы.
    - wrapper_services (Aiogoogle): Объект Aiogoogle,
    используемый для взаимодействия с Google Drive API.
    """
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """
    Обновляет значения в таблице Google Spreadsheet.
    #### Args:
    - spreadsheetid (строка): Идентификатор электронной таблицы.
    - projects: list - Список проектов для обновления в таблице.
    - wrapper_services (Aiogoogle): Объект Aiogoogle,
    используемый для взаимодействия с Google Drive API.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ поектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [
            project['name'],
            str(timedelta(days=project['сollection_rate'])),
            project['description'],
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:C100',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectUpdate


charity_project_crud = CRUDBase[
    CharityProject, CharityProjectCreate, CharityProjectUpdate
](CharityProject)
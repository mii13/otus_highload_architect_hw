from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from src.api.dependencies.session import get_session


def get_repository(repo_type):
    def _get_repository(
        session: Session = Depends(get_session),
    ):
        return repo_type(session)

    return _get_repository

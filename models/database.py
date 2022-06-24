import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

db = SQLAlchemy()

log = logging.getLogger(__name__)


def db_add_obj(database: SQLAlchemy, obj: db.Model) -> None:
    database.session.add(obj)
    try:
        database.session.commit()
    except IntegrityError:
        log.exception(f"Could not add {obj.__class__.__name__} {obj}")
        database.session.rollback()
        raise BadRequest(f"Could not save {obj.__class__.__name__}")


__all__ = (
    'db',
    'db_add_obj',
)

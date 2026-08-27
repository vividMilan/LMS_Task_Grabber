from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session

from ..models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD repository class for SQLAlchemy models."""

    def __init__(self, model: type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, id_val: Any) -> ModelType | None:
        """Fetch a single record by its primary key."""
        return db.query(self.model).filter(self.model.id == id_val).first()

    def get_all(self, db: Session) -> Sequence[ModelType]:
        """Fetch all records in the table."""
        return db.query(self.model).all()

    def create(self, db: Session, **kwargs: Any) -> ModelType:
        """Create and persist a new record."""
        instance = self.model(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def delete(self, db: Session, id_val: Any) -> bool:
        """Delete a record by primary key."""
        instance = self.get_by_id(db, id_val)

        if instance:
            db.delete(instance)
            db.commit()
            return True

        return False

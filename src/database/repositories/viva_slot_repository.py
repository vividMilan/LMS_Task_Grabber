from src.database.repositories.base_repository import BaseRepository
from src.database.models import VivaSlot

from sqlalchemy.orm import Session

from datetime import datetime

class VivaSlotRepository(BaseRepository[VivaSlot]):

    def __init__(self):
        super().__init__(VivaSlot)

    def upsert_viva_slot(self, db: Session, start_time: datetime, end_time: datetime, assignment_id: str) -> tuple[VivaSlot, bool]:

        new_viva_slot = self.create(
            db=db,
            start_time=start_time,
            end_time=end_time,
            assignment_id=assignment_id
        )

        return new_viva_slot, True

viva_slot_repo = VivaSlotRepository()
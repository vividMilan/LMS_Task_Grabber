from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, sessionmaker, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Course(Base):
    __tablename__ = 'courses'
    
    id: Mapped[str] = Column(String, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    excluded: Mapped[bool] = Column(Integer, default=0)

    files: Mapped[list["File"]] = relationship(
        back_populates="course"
    )

    assignments: Mapped[list["Assignment"]] = relationship(
        back_populates="course"
    )


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    file_path: Mapped[str] =  Column(String, nullable=False)
    file_link: Mapped[str] = Column(String, nullable=False)
    course_id: Mapped[str] = mapped_column(
        ForeignKey("courses.id")
    )

    course: Mapped["Course"] = relationship(
        back_populates="files"
    )

    assignments: Mapped[list["Assignment"]] = relationship(
        back_populates="file"
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[str] = Column(String, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    course_id: Mapped[str] = mapped_column(
        ForeignKey("courses.id")
    )
    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"),
        nullable=True
    )
    completed: Mapped[bool] = Column(Integer, default=0)
    type: Mapped[str] = Column(String, nullable=True)
    due: Mapped[datetime] = Column(DateTime, nullable=False)
    link: Mapped[str] = Column(String, nullable=False)


    course: Mapped["Course"] = relationship(
        back_populates="assignments"
    )

    file: Mapped["File"] = relationship(
        back_populates="assignments"
    )


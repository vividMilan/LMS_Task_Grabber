from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, sessionmaker, relationship
from datetime import datetime
from enum import Enum


class AssignmentType(str, Enum):
    MINI_PROJECT = "mini_project"
    VIVA_SLOT = "viva_slot"
    QUIZ = "quiz"
    TMA = "tma"
    EXAM = "exam"


class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = 'courses'
    
    id: Mapped[str] = Column(String, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    excluded: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

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

    assignment_id: Mapped[str] = mapped_column(
        ForeignKey("assignments.id"),
        nullable=False
    )

    assignment: Mapped["Assignment"] = relationship(
        back_populates="files"
    )

    course: Mapped["Course"] = relationship(
        back_populates="files"
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[str] = Column(String, primary_key=True)

    name: Mapped[str] = Column(String, nullable=False)

    course_id: Mapped[str] = mapped_column(
        ForeignKey("courses.id")
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    type: Mapped[AssignmentType | None] = mapped_column(
        SQLEnum(AssignmentType),
        nullable=True
    )

    due: Mapped[datetime] = Column(DateTime, nullable=False)

    link: Mapped[str] = Column(String, nullable=False)

    course: Mapped["Course"] = relationship(
        back_populates="assignments"
    )

    files: Mapped[list["File"]] = relationship(
        back_populates="assignment"
    )

    viva_slot: Mapped["VivaSlot | None"] = relationship(
        back_populates="assignment",
        uselist=False
    )


class VivaSlot(Base):
    __tablename__="viva_slots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    assignment_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("assignments.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    assignment: Mapped["Assignment"] = relationship(
        back_populates="viva_slot"
    )

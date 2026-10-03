from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from sqlalchemy.orm import declarative_base


# --------------------------------------------------
# BASE
# --------------------------------------------------

Base = declarative_base()


# --------------------------------------------------
# MEETING TABLE
# --------------------------------------------------

class Meeting(Base):

    __tablename__ = "meetings"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    transcript = Column(
        Text,
        nullable=False
    )

    summary = Column(
        Text,
        nullable=True
    )


# --------------------------------------------------
# KEY POINT TABLE
# --------------------------------------------------

class KeyPoint(Base):

    __tablename__ = "key_points"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id"),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )


# --------------------------------------------------
# DECISION TABLE
# --------------------------------------------------

class Decision(Base):

    __tablename__ = "decisions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id"),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )


# --------------------------------------------------
# ACTION ITEM TABLE
# --------------------------------------------------

class ActionItem(Base):

    __tablename__ = "action_items"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id"),
        nullable=False
    )

    task = Column(
        Text,
        nullable=False
    )

    owner = Column(
        String(255),
        nullable=False,
        default="Not specified"
    )

    deadline = Column(
        String(255),
        nullable=False,
        default="Not specified"
    )
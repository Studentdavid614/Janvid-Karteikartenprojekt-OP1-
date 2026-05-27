from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import UTC, datetime
from enum import Enum


class PermissionLevel(str, Enum):
    VIEW = "view"
    EDIT = "edit"
    ADMIN = "admin"


class Visibility(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    card_sets: List["CardSet"] = Relationship(back_populates="creator")
    permissions: List["SetPermission"] = Relationship(back_populates="user")
    learning_history: List["LearningHistory"] = Relationship(back_populates="user")


class CardSet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    creator_id: int = Field(foreign_key="user.id")
    visibility: Visibility = Field(default=Visibility.PRIVATE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    creator: User = Relationship(back_populates="card_sets")
    cards: List["Card"] = Relationship(back_populates="card_set", cascade_delete=True)
    permissions: List["SetPermission"] = Relationship(back_populates="card_set", cascade_delete=True)


class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_set_id: int = Field(foreign_key="cardset.id")
    front: str
    back: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correct_count: int = 0
    incorrect_count: int = 0
    
    card_set: CardSet = Relationship(back_populates="cards")
    learning_history: List["LearningHistory"] = Relationship(back_populates="card")


class SetPermission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_set_id: int = Field(foreign_key="cardset.id")
    user_id: int = Field(foreign_key="user.id")
    permission_level: PermissionLevel = Field(default=PermissionLevel.VIEW)
    granted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    card_set: CardSet = Relationship(back_populates="permissions")
    user: User = Relationship(back_populates="permissions")


class LearningHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    card_id: int = Field(foreign_key="card.id")
    is_correct: bool
    answered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    user: User = Relationship(back_populates="learning_history")
    card: Card = Relationship(back_populates="learning_history")

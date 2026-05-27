"""
Tests for models.
"""

from sqlmodel import SQLModel, create_engine, Session
from app.models import User, CardSet, Card, SetPermission, LearningHistory, PermissionLevel, Visibility
from app.auth import hash_password


def test_create_user():
    """Test creating a user."""
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123")
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"


def test_create_card_set():
    """Test creating a card set."""
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123")
        )
        session.add(user)
        session.commit()
        
        card_set = CardSet(
            creator_id=user.id,
            name="Test Set",
            description="A test card set",
            visibility=Visibility.PRIVATE
        )
        session.add(card_set)
        session.commit()
        session.refresh(card_set)
        
        assert card_set.id is not None
        assert card_set.name == "Test Set"
        assert card_set.creator_id == user.id


def test_create_card():
    """Test creating a card."""
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123")
        )
        session.add(user)
        session.commit()
        
        card_set = CardSet(
            creator_id=user.id,
            name="Test Set",
            visibility=Visibility.PRIVATE
        )
        session.add(card_set)
        session.commit()
        
        card = Card(
            card_set_id=card_set.id,
            front="What is 2+2?",
            back="4"
        )
        session.add(card)
        session.commit()
        session.refresh(card)
        
        assert card.id is not None
        assert card.front == "What is 2+2?"
        assert card.back == "4"


def test_set_permission():
    """Test setting permissions."""
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user1 = User(
            username="user1",
            email="user1@example.com",
            password_hash=hash_password("password123")
        )
        user2 = User(
            username="user2",
            email="user2@example.com",
            password_hash=hash_password("password123")
        )
        session.add(user1)
        session.add(user2)
        session.commit()
        
        card_set = CardSet(
            creator_id=user1.id,
            name="Test Set",
            visibility=Visibility.PRIVATE
        )
        session.add(card_set)
        session.commit()
        
        permission = SetPermission(
            card_set_id=card_set.id,
            user_id=user2.id,
            permission_level=PermissionLevel.EDIT
        )
        session.add(permission)
        session.commit()
        session.refresh(permission)
        
        assert permission.card_set_id == card_set.id
        assert permission.user_id == user2.id
        assert permission.permission_level == PermissionLevel.EDIT


def test_learning_history():
    """Test recording learning history."""
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123")
        )
        session.add(user)
        session.commit()
        
        card_set = CardSet(
            creator_id=user.id,
            name="Test Set",
            visibility=Visibility.PRIVATE
        )
        session.add(card_set)
        session.commit()
        
        card = Card(
            card_set_id=card_set.id,
            front="What is 2+2?",
            back="4"
        )
        session.add(card)
        session.commit()
        
        history = LearningHistory(
            user_id=user.id,
            card_id=card.id,
            is_correct=True
        )
        session.add(history)
        session.commit()
        session.refresh(history)
        
        assert history.user_id == user.id
        assert history.card_id == card.id
        assert history.is_correct is True


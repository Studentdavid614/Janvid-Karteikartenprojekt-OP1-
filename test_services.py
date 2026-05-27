"""
Tests for services.
"""

from contextlib import contextmanager
import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
from app import services
from app.models import Visibility, PermissionLevel
from app.auth import hash_password


@pytest.fixture
def isolated_services(monkeypatch):
    """Create an isolated in-memory database for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    @contextmanager
    def _get_session():
        with Session(engine) as session:
            yield session

    monkeypatch.setattr(services, "get_session", _get_session)
    return services


def test_create_and_list_card_sets(isolated_services):
    """Test creating and listing card sets."""
    svc = isolated_services
    
    # Create a user first
    from app.auth import create_user as auth_create_user
    with svc.get_session() as session:
        user = auth_create_user(session, "testuser", "test@example.com", "password123")
    
    # Create card set
    card_set = svc.create_card_set(user.id, "Test Set", "Test Description", Visibility.PRIVATE)
    assert card_set.id is not None
    assert card_set.name == "Test Set"
    assert card_set.creator_id == user.id
    
    # List card sets
    sets = svc.list_card_sets_for_user(user.id)
    assert len(sets) >= 1
    assert any(s.name == "Test Set" for s in sets)


def test_card_crud_flow(isolated_services):
    """Test creating, reading, updating and deleting cards."""
    svc = isolated_services
    
    from app.auth import create_user as auth_create_user
    with svc.get_session() as session:
        user = auth_create_user(session, "testuser", "test@example.com", "password123")
    
    # Create card set
    card_set = svc.create_card_set(user.id, "Test Set", "", Visibility.PRIVATE)
    
    # Create card
    card = svc.create_card(card_set.id, "What is 2+2?", "4")
    assert card.id is not None
    assert card.front == "What is 2+2?"
    assert card.back == "4"
    
    # List cards
    cards = svc.list_cards_in_set(card_set.id)
    assert len(cards) == 1
    assert cards[0].front == "What is 2+2?"
    
    # Get card
    loaded = svc.get_card(card.id)
    assert loaded is not None
    assert loaded.back == "4"
    
    # Update card
    updated = svc.update_card(card.id, "What is 3+3?", "6")
    assert updated is not None
    assert updated.front == "What is 3+3?"
    assert updated.back == "6"
    
    # Delete card
    deleted = svc.delete_card(card.id)
    assert deleted is True
    
    cards = svc.list_cards_in_set(card_set.id)
    assert len(cards) == 0


def test_permissions(isolated_services):
    """Test setting and checking permissions."""
    svc = isolated_services
    
    from app.auth import create_user as auth_create_user
    with svc.get_session() as session:
        user1 = auth_create_user(session, "user1", "user1@example.com", "password123")
        user2 = auth_create_user(session, "user2", "user2@example.com", "password123")
    
    # Create card set
    card_set = svc.create_card_set(user1.id, "Test Set", "", Visibility.PRIVATE)
    
    # Grant permission
    perm = svc.grant_permission(card_set.id, user2.id, PermissionLevel.VIEW)
    assert perm.permission_level == PermissionLevel.VIEW
    
    # Check permission
    can_view = svc.can_view_card_set(user2.id, card_set.id)
    assert can_view is True
    
    can_edit = svc.can_edit_card_set(user2.id, card_set.id)
    assert can_edit is False
    
    # Grant edit permission
    svc.grant_permission(card_set.id, user2.id, PermissionLevel.EDIT)
    can_edit = svc.can_edit_card_set(user2.id, card_set.id)
    assert can_edit is True
    
    # Revoke permission
    revoked = svc.revoke_permission(card_set.id, user2.id)
    assert revoked is True
    
    can_view = svc.can_view_card_set(user2.id, card_set.id)
    assert can_view is False


def test_learning_history_and_statistics(isolated_services):
    """Test recording learning history and getting statistics."""
    svc = isolated_services
    
    from app.auth import create_user as auth_create_user
    with svc.get_session() as session:
        user = auth_create_user(session, "testuser", "test@example.com", "password123")
    
    # Create card set and cards
    card_set = svc.create_card_set(user.id, "Test Set", "", Visibility.PRIVATE)
    card1 = svc.create_card(card_set.id, "Question 1?", "Answer 1")
    card2 = svc.create_card(card_set.id, "Question 2?", "Answer 2")
    
    # Record answers
    svc.record_answer(user.id, card1.id, True)
    svc.record_answer(user.id, card1.id, True)
    svc.record_answer(user.id, card2.id, False)
    
    # Check user statistics
    stats = svc.get_user_statistics(user.id)
    assert stats["total_answers"] == 3
    assert stats["correct"] == 2
    assert stats["incorrect"] == 1
    assert stats["accuracy"] == pytest.approx(66.66666666666666)
    
    # Check card set statistics
    set_stats = svc.get_card_set_statistics(card_set.id, user.id)
    assert set_stats["total_cards"] == 2
    assert set_stats["total_answers"] == 3
    assert set_stats["correct"] == 2
    assert set_stats["incorrect"] == 1


def test_public_sets(isolated_services):
    """Test public and private card sets."""
    svc = isolated_services
    
    from app.auth import create_user as auth_create_user
    with svc.get_session() as session:
        user = auth_create_user(session, "testuser", "test@example.com", "password123")
    
    # Create public set
    public_set = svc.create_card_set(user.id, "Public Set", "", Visibility.PUBLIC)
    
    # Create private set
    private_set = svc.create_card_set(user.id, "Private Set", "", Visibility.PRIVATE)
    
    # List public sets
    public_sets = svc.list_public_card_sets()
    assert any(s.id == public_set.id for s in public_sets)
    assert not any(s.id == private_set.id for s in public_sets)
    
    # Can view public set without permission
    other_user_id = 999
    can_view_public = svc.can_view_card_set(other_user_id, public_set.id)
    assert can_view_public is True
    
    can_view_private = svc.can_view_card_set(other_user_id, private_set.id)
    assert can_view_private is False

    assert deleted is True
    assert svc.get_card(created.id) is None


def test_record_answer_and_subjects(isolated_services):
    svc = isolated_services

    c1 = svc.create_card("Physik", "g", "9.81")
    c2 = svc.create_card("Physik", "c", "299792458")

    assert svc.record_answer(c1.id, True) is True
    assert svc.record_answer(c1.id, False) is True
    assert svc.record_answer(999999, True) is False

    c1_reloaded = svc.get_card(c1.id)
    assert c1_reloaded.correct_count == 1
    assert c1_reloaded.incorrect_count == 1

    subjects = svc.list_subjects()
    assert len(subjects) == 1
    assert subjects[0].name == "Physik"

    cards = svc.list_cards()
    assert {card.id for card in cards} == {c1.id, c2.id}

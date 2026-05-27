from typing import List, Optional
from sqlmodel import select, and_
from datetime import UTC, datetime

try:
    from .models import Card, CardSet, User, SetPermission, LearningHistory, PermissionLevel, Visibility
    from .db import get_session
except ImportError:
    try:
        from app.models import Card, CardSet, User, SetPermission, LearningHistory, PermissionLevel, Visibility
        from app.db import get_session
    except ImportError:
        from models import Card, CardSet, User, SetPermission, LearningHistory, PermissionLevel, Visibility
        from db import get_session


# ============ OOP Service Classes ============

class CardSetService:
    """Encapsulates all business logic for card set management."""

    @staticmethod
    def create(creator_id: int, name: str, description: str = "",
               visibility: Visibility = Visibility.PRIVATE) -> CardSet:
        with get_session() as session:
            card_set = CardSet(
                creator_id=creator_id,
                name=name,
                description=description,
                visibility=visibility,
            )
            session.add(card_set)
            session.commit()
            session.refresh(card_set)
            return card_set

    @staticmethod
    def get(card_set_id: int) -> Optional[CardSet]:
        with get_session() as session:
            return session.get(CardSet, card_set_id)

    @staticmethod
    def list_for_user(user_id: int) -> List[CardSet]:
        with get_session() as session:
            user_sets = list(session.exec(
                select(CardSet).where(CardSet.creator_id == user_id)
            ).all())
            permissions = session.exec(
                select(SetPermission).where(SetPermission.user_id == user_id)
            ).all()
            shared_sets = [perm.card_set for perm in permissions]
            return user_sets + shared_sets

    @staticmethod
    def list_public() -> List[CardSet]:
        with get_session() as session:
            return list(session.exec(
                select(CardSet).where(CardSet.visibility == Visibility.PUBLIC)
            ).all())

    @staticmethod
    def update(card_set_id: int, name: str = None, description: str = None,
               visibility: Visibility = None) -> Optional[CardSet]:
        with get_session() as session:
            card_set = session.get(CardSet, card_set_id)
            if not card_set:
                return None
            if name is not None:
                card_set.name = name
            if description is not None:
                card_set.description = description
            if visibility is not None:
                card_set.visibility = visibility
            card_set.updated_at = datetime.now(UTC)
            session.add(card_set)
            session.commit()
            session.refresh(card_set)
            return card_set

    @staticmethod
    def delete(card_set_id: int) -> bool:
        with get_session() as session:
            card_set = session.get(CardSet, card_set_id)
            if not card_set:
                return False
            session.delete(card_set)
            session.commit()
            return True


class CardService:
    """Encapsulates all business logic for individual card management."""

    @staticmethod
    def create(card_set_id: int, front: str, back: str) -> Card:
        with get_session() as session:
            card = Card(card_set_id=card_set_id, front=front.strip(), back=back.strip())
            session.add(card)
            session.commit()
            session.refresh(card)
            return card

    @staticmethod
    def get(card_id: int) -> Optional[Card]:
        with get_session() as session:
            return session.get(Card, card_id)

    @staticmethod
    def list_in_set(card_set_id: int) -> List[Card]:
        with get_session() as session:
            return list(session.exec(
                select(Card).where(Card.card_set_id == card_set_id)
            ).all())

    @staticmethod
    def update(card_id: int, front: str = None, back: str = None) -> Optional[Card]:
        with get_session() as session:
            card = session.get(Card, card_id)
            if not card:
                return None
            if front is not None:
                card.front = front.strip()
            if back is not None:
                card.back = back.strip()
            session.add(card)
            session.commit()
            session.refresh(card)
            return card

    @staticmethod
    def delete(card_id: int) -> bool:
        with get_session() as session:
            card = session.get(Card, card_id)
            if not card:
                return False
            session.delete(card)
            session.commit()
            return True


class PermissionService:
    """Encapsulates access-control logic for card set permissions."""

    @staticmethod
    def grant(card_set_id: int, user_id: int,
              level: PermissionLevel = PermissionLevel.VIEW) -> SetPermission:
        with get_session() as session:
            existing = session.exec(
                select(SetPermission).where(
                    and_(SetPermission.card_set_id == card_set_id,
                         SetPermission.user_id == user_id)
                )
            ).first()
            if existing:
                existing.permission_level = level
                session.add(existing)
                session.commit()
                session.refresh(existing)
                return existing
            perm = SetPermission(card_set_id=card_set_id, user_id=user_id,
                                 permission_level=level)
            session.add(perm)
            session.commit()
            session.refresh(perm)
            return perm

    @staticmethod
    def revoke(card_set_id: int, user_id: int) -> bool:
        with get_session() as session:
            perm = session.exec(
                select(SetPermission).where(
                    and_(SetPermission.card_set_id == card_set_id,
                         SetPermission.user_id == user_id)
                )
            ).first()
            if not perm:
                return False
            session.delete(perm)
            session.commit()
            return True

    @staticmethod
    def can_edit(user_id: int, card_set_id: int) -> bool:
        with get_session() as session:
            card_set = session.get(CardSet, card_set_id)
            if not card_set:
                return False
            if card_set.creator_id == user_id:
                return True
            return session.exec(
                select(SetPermission).where(
                    and_(SetPermission.card_set_id == card_set_id,
                         SetPermission.user_id == user_id,
                         SetPermission.permission_level == PermissionLevel.EDIT)
                )
            ).first() is not None

    @staticmethod
    def can_view(user_id: int, card_set_id: int) -> bool:
        with get_session() as session:
            card_set = session.get(CardSet, card_set_id)
            if not card_set:
                return False
            if card_set.creator_id == user_id:
                return True
            if card_set.visibility == Visibility.PUBLIC:
                return True
            return session.exec(
                select(SetPermission).where(
                    and_(SetPermission.card_set_id == card_set_id,
                         SetPermission.user_id == user_id)
                )
            ).first() is not None

    @staticmethod
    def list_for_set(card_set_id: int) -> List[SetPermission]:
        with get_session() as session:
            return list(session.exec(
                select(SetPermission).where(SetPermission.card_set_id == card_set_id)
            ).all())


class LearningService:
    """Encapsulates learning session tracking and statistics."""

    @staticmethod
    def record_answer(user_id: int, card_id: int, is_correct: bool) -> LearningHistory:
        with get_session() as session:
            history = LearningHistory(user_id=user_id, card_id=card_id,
                                      is_correct=is_correct)
            session.add(history)
            session.commit()
            session.refresh(history)
            return history

    @staticmethod
    def get_user_statistics(user_id: int) -> dict:
        with get_session() as session:
            history = session.exec(
                select(LearningHistory).where(LearningHistory.user_id == user_id)
            ).all()
            if not history:
                return {"total_answers": 0, "correct": 0, "incorrect": 0, "accuracy": 0.0}
            total = len(history)
            correct = sum(1 for h in history if h.is_correct)
            return {
                "total_answers": total,
                "correct": correct,
                "incorrect": total - correct,
                "accuracy": correct / total * 100,
            }

    @staticmethod
    def get_card_set_statistics(card_set_id: int, user_id: int) -> dict:
        with get_session() as session:
            cards = session.exec(
                select(Card).where(Card.card_set_id == card_set_id)
            ).all()
            card_ids = [c.id for c in cards]
            if not card_ids:
                return {"total_cards": 0, "cards_mastered": 0,
                        "accuracy": 0.0, "total_answers": 0,
                        "correct": 0, "incorrect": 0}
            history = session.exec(
                select(LearningHistory).where(
                    and_(LearningHistory.user_id == user_id,
                         LearningHistory.card_id.in_(card_ids))
                )
            ).all()
            total = len(history)
            correct = sum(1 for h in history if h.is_correct)
            card_stats: dict = {}
            for h in history:
                card_stats.setdefault(h.card_id, {"correct": 0, "total": 0})
                card_stats[h.card_id]["total"] += 1
                if h.is_correct:
                    card_stats[h.card_id]["correct"] += 1
            mastered = sum(1 for s in card_stats.values() if s["correct"] >= 5)
            return {
                "total_cards": len(cards),
                "total_answers": total,
                "correct": correct,
                "incorrect": total - correct,
                "accuracy": correct / total * 100 if total else 0.0,
                "cards_mastered": mastered,
            }


# ============ Module-level wrappers (backward-compatible) ============

def create_card_set(creator_id: int, name: str, description: str = "",
                    visibility: Visibility = Visibility.PRIVATE) -> CardSet:
    return CardSetService.create(creator_id, name, description, visibility)


def get_card_set(card_set_id: int) -> Optional[CardSet]:
    return CardSetService.get(card_set_id)


def list_card_sets_for_user(user_id: int) -> List[CardSet]:
    return CardSetService.list_for_user(user_id)


def list_public_card_sets() -> List[CardSet]:
    return CardSetService.list_public()


def update_card_set(card_set_id: int, name: str = None, description: str = None,
                    visibility: Visibility = None) -> Optional[CardSet]:
    return CardSetService.update(card_set_id, name, description, visibility)


def delete_card_set(card_set_id: int) -> bool:
    return CardSetService.delete(card_set_id)


def create_card(card_set_id: int, front: str, back: str) -> Card:
    return CardService.create(card_set_id, front, back)


def get_card(card_id: int) -> Optional[Card]:
    return CardService.get(card_id)


def list_cards_in_set(card_set_id: int) -> List[Card]:
    return CardService.list_in_set(card_set_id)


def update_card(card_id: int, front: str = None, back: str = None) -> Optional[Card]:
    return CardService.update(card_id, front, back)


def delete_card(card_id: int) -> bool:
    return CardService.delete(card_id)


def grant_permission(card_set_id: int, user_id: int,
                     permission_level: PermissionLevel = PermissionLevel.VIEW) -> SetPermission:
    return PermissionService.grant(card_set_id, user_id, permission_level)


def get_permission(card_set_id: int, user_id: int) -> Optional[SetPermission]:
    with get_session() as session:
        return session.exec(
            select(SetPermission).where(
                and_(SetPermission.card_set_id == card_set_id,
                     SetPermission.user_id == user_id)
            )
        ).first()


def revoke_permission(card_set_id: int, user_id: int) -> bool:
    return PermissionService.revoke(card_set_id, user_id)


def can_edit_card_set(user_id: int, card_set_id: int) -> bool:
    return PermissionService.can_edit(user_id, card_set_id)


def can_view_card_set(user_id: int, card_set_id: int) -> bool:
    return PermissionService.can_view(user_id, card_set_id)


def record_answer(user_id: int, card_id: int, is_correct: bool) -> LearningHistory:
    return LearningService.record_answer(user_id, card_id, is_correct)


def get_user_statistics(user_id: int) -> dict:
    return LearningService.get_user_statistics(user_id)


def get_card_set_statistics(card_set_id: int, user_id: int) -> dict:
    return LearningService.get_card_set_statistics(card_set_id, user_id)

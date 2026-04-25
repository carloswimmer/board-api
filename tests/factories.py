from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(slots=True)
class FakeUser:
    id: str
    email: str
    name: str
    image: str = ''


@dataclass(slots=True)
class FakeIssue:
    id: str
    issue_number: int
    title: str
    description: str
    status: str
    likes: int
    created_at: datetime


def create_user(
    *,
    id: str | None = None,
    email: str | None = None,
    name: str = 'Test User',
    image: str = '',
) -> FakeUser:
    user_id = id or str(uuid4())
    user_email = email or f'{user_id[:8]}@example.com'
    return FakeUser(
        id=user_id,
        email=user_email,
        name=name,
        image=image,
    )


def create_issue(
    *,
    id: str | None = None,
    issue_number: int = 1,
    title: str = 'Sample issue',
    description: str = 'Sample issue description',
    status: str = 'backlog',
    likes: int = 0,
    created_at: datetime | None = None,
) -> FakeIssue:
    return FakeIssue(
        id=id or str(uuid4()),
        issue_number=issue_number,
        title=title,
        description=description,
        status=status,
        likes=likes,
        created_at=created_at or datetime.now(UTC),
    )

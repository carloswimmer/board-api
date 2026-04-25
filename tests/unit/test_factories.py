from tests.factories import create_issue, create_user


def test_create_user_defaults() -> None:
    user = create_user()

    assert user.id
    assert user.email.endswith('@example.com')
    assert user.name == 'Test User'
    assert user.image == ''


def test_create_user_accepts_overrides() -> None:
    user = create_user(
        id='user-123',
        email='carlos@example.com',
        name='Carlos',
        image='https://example.com/avatar.png',
    )

    assert user.id == 'user-123'
    assert user.email == 'carlos@example.com'
    assert user.name == 'Carlos'
    assert user.image == 'https://example.com/avatar.png'


def test_create_issue_defaults() -> None:
    issue = create_issue()

    assert issue.id
    assert issue.issue_number == 1
    assert issue.title == 'Sample issue'
    assert issue.description == 'Sample issue description'
    assert issue.status == 'backlog'
    assert issue.likes == 0
    assert issue.created_at is not None


def test_create_issue_accepts_overrides() -> None:
    issue = create_issue(
        id='issue-123',
        issue_number=42,
        title='Fix login bug',
        description='Users cannot login with GitHub',
        status='in_progress',
        likes=7,
    )

    assert issue.id == 'issue-123'
    assert issue.issue_number == 42
    assert issue.title == 'Fix login bug'
    assert issue.description == 'Users cannot login with GitHub'
    assert issue.status == 'in_progress'
    assert issue.likes == 7

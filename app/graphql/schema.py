import strawberry


@strawberry.type
class IssueCard:
    id: strawberry.ID
    issue_number: int
    title: str
    status: str
    comments: int


@strawberry.type
class IssuesByStatus:
    backlog: list[IssueCard]
    todo: list[IssueCard]
    in_progress: list[IssueCard]
    done: list[IssueCard]


@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return 'pong'

    @strawberry.field
    def issues(self) -> IssuesByStatus:
        return IssuesByStatus(
            backlog=[],
            todo=[],
            in_progress=[],
            done=[],
        )


schema = strawberry.Schema(query=Query)
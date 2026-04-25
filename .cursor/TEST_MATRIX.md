# Test Matrix (SPEC -> Tests)

## Legend
- [ ] todo
- [~] doing
- [x] done

## Queries

### issues(input: ListIssuesInput): IssuesByStatus!
- [ ] Happy path: list all grouped by status
- [ ] Filter by status
- [ ] Search by title (case-insensitive contains)
- [ ] Sort by issueNumber ASC
- [ ] Sort by issueNumber DESC
- [ ] Comments field returns count
- [ ] BAD_REQUEST for invalid enum/sort input

### issue(id: ID!): Issue!
- [ ] Happy path: returns issue details
- [ ] Includes comments count
- [ ] NOT_FOUND when issue does not exist

### issueComments(input: ListIssueCommentsInput!): CommentsPage!
- [ ] Happy path: paginated list by issue
- [ ] Ordered by createdAt DESC
- [ ] limit default = 50
- [ ] offset default = 0
- [ ] BAD_REQUEST when limit < 1
- [ ] BAD_REQUEST when limit > 100
- [ ] BAD_REQUEST when offset < 0
- [ ] NOT_FOUND when issue does not exist

### issueInteractions(issueIds: [ID!]!): [IssueInteraction!]!
- [ ] Happy path authenticated: isLiked + likesCount
- [ ] Happy path anonymous: isLiked=false
- [ ] Empty input returns empty list

## Mutations

### createIssue(input: CreateIssueInput!): Issue!
- [ ] Happy path: create with explicit status
- [ ] Happy path: default status = BACKLOG
- [ ] likes starts at 0
- [ ] comments starts at 0
- [ ] auto-generates unique sequential issueNumber
- [ ] BAD_REQUEST title empty
- [ ] BAD_REQUEST description empty

### updateIssue(id: ID!, input: UpdateIssueInput!): Issue!
- [ ] Happy path partial update (title only)
- [ ] Happy path partial update (description only)
- [ ] Happy path partial update (status only)
- [ ] NOT_FOUND for missing issue
- [ ] BAD_REQUEST invalid status

### deleteIssue(id: ID!): Boolean!
- [ ] Happy path returns true
- [ ] NOT_FOUND for missing issue
- [ ] Cascade removes comments/likes

### createComment(input: CreateCommentInput!): Comment!
- [ ] UNAUTHORIZED when anonymous
- [ ] Happy path authenticated
- [ ] Author comes from current_user (name/image)
- [ ] Uses empty string when image missing
- [ ] NOT_FOUND when issue does not exist
- [ ] BAD_REQUEST text empty

### updateComment(input: UpdateCommentInput!): Comment!
- [ ] UNAUTHORIZED when anonymous
- [ ] Happy path author updates own comment
- [ ] FORBIDDEN when not owner
- [ ] NOT_FOUND when comment does not exist
- [ ] BAD_REQUEST text empty

### deleteComment(input: DeleteCommentInput!): Boolean!
- [ ] UNAUTHORIZED when anonymous
- [ ] Happy path owner deletes comment
- [ ] FORBIDDEN when not owner
- [ ] NOT_FOUND when comment does not exist

### toggleIssueLike(input: ToggleIssueLikeInput!): LikeResult!
- [ ] UNAUTHORIZED when anonymous
- [ ] Like when not previously liked
- [ ] Unlike when previously liked
- [ ] likes denormalized counter updates correctly
- [ ] NOT_FOUND when issue does not exist
- [ ] Transaction consistency (like row + counter)

## Cross-cutting (errors + semantics)
- [ ] BAD_REQUEST mapping in GraphQL errors.extensions.code
- [ ] UNAUTHORIZED mapping in GraphQL errors.extensions.code
- [ ] FORBIDDEN mapping in GraphQL errors.extensions.code
- [ ] NOT_FOUND mapping in GraphQL errors.extensions.code
- [ ] DateTime returned in UTC
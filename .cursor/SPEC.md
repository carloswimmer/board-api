# SPEC - board-api (FastAPI + GraphQL)

## 1) Objetivo

Implementar no `board-api` uma API GraphQL em Python (FastAPI) que replique o comportamento funcional da API atual em `board-app/src/api`, preservando:

- regras de domínio de board/issue/comment;
- regras de autenticação/autorização;
- formatos de dados (com pequenas adaptacoes idiomaticas para GraphQL);
- semantica de erros e validacoes.

O foco desta fase e **paridade funcional** com o backend atual.

## 2) Escopo funcional

### 2.1 Entidades principais

- `Issue`
- `Comment`
- `IssueLike`
- `User` (proveniente do provider de auth)
- `Session` (infra de autenticacao)

### 2.2 Casos de uso obrigatorios

1. Listar issues com filtros e ordenacao.
2. Obter detalhes de uma issue.
3. Criar issue.
4. Atualizar issue (patch parcial).
5. Excluir issue.
6. Listar comentarios de uma issue (paginado por limit/offset).
7. Criar comentario (autenticado).
8. Atualizar comentario (autenticado e dono do comentario).
9. Excluir comentario (autenticado e dono do comentario).
10. Alternar like em issue (autenticado).
11. Consultar interacoes de multiplas issues para o usuario atual (liked + likesCount por issue).

## 3) Modelo de dados (paridade)

### 3.1 Issue

- `id: UUID` (pk)
- `issue_number: int` (unico, sequencial crescente)
- `title: str` (obrigatorio, nao vazio)
- `description: str` (obrigatorio, nao vazio)
- `status: enum` em `["backlog", "todo", "in_progress", "done"]`
- `likes: int` (default 0, nao negativo)
- `created_at: datetime`

### 3.2 Comment

- `id: UUID` (pk)
- `issue_id: UUID` (fk -> issue, delete cascade)
- `author_name: str`
- `author_avatar: str` (url/string; pode ser vazio)
- `text: str` (obrigatorio, nao vazio)
- `created_at: datetime`

### 3.3 User/Session/Auth (infra)

Manter estrutura equivalente ao backend atual para suportar:
- identificacao de usuario logado (`user.id`, `user.email`, `user.name`, `user.image`);
- verificacao de sessao no contexto da requisicao.

### 3.4 IssueLike

- `id: UUID` (pk)
- `issue_id: UUID` (fk -> issue, delete cascade)
- `user_id: UUID` (fk -> user, delete cascade)
- `created_at: datetime`
- restricao logica: um unico like por par `(issue_id, user_id)`.

## 4) Regras de negocio

1. **Issue status** deve aceitar apenas valores do enum oficial.
2. **Issue number** e gerado automaticamente e e unico.
3. `comments` em payloads de issue e um **count** calculado.
4. `likes` em issue e mantido denormalizado e atualizado nas operacoes de like/unlike.
5. Operacoes de comentario e like exigem usuario autenticado quando indicado.
6. Atualizacao/remocao de comentario so pode ser feita pelo autor.
7. Exclusao de issue remove comentarios e likes relacionados por cascade.

## 5) Contrato GraphQL

> Observacao: nomes podem seguir snake_case internamente, mas o schema GraphQL deve ser consistente e previsivel para o frontend.

### 5.1 Scalars e enums

- `scalar DateTime`
- `enum IssueStatus { BACKLOG TODO IN_PROGRESS DONE }`

Mapeamento de status:
- `BACKLOG <-> "backlog"`
- `TODO <-> "todo"`
- `IN_PROGRESS <-> "in_progress"`
- `DONE <-> "done"`

### 5.2 Tipos

- `type IssueCard { id, issueNumber, title, status, comments }`
- `type Issue { id, issueNumber, title, description, status, likes, comments, createdAt }`
- `type CommentAuthor { name, avatar }`
- `type Comment { id, issueId, author, text, createdAt }`
- `type CommentsPage { comments, total, limit, offset }`
- `type IssueInteraction { issueId, isLiked, likesCount }`
- `type IssuesByStatus { backlog, todo, inProgress, done }`
- `type LikeResult { id, likes, liked }`
- `type ApiError { error, message }`

### 5.3 Inputs

- `input ListIssuesInput { status?: IssueStatus, search?: String, sort?: IssueSortField, direction?: SortDirection = ASC }`
- `enum IssueSortField { ISSUE_NUMBER }`
- `enum SortDirection { ASC DESC }`
- `input CreateIssueInput { title: String!, description: String!, status: IssueStatus = BACKLOG }`
- `input UpdateIssueInput { title?: String, description?: String, status?: IssueStatus }`
- `input ListIssueCommentsInput { issueId: ID!, limit: Int = 50, offset: Int = 0 }`
- `input CreateCommentInput { issueId: ID!, text: String! }`
- `input UpdateCommentInput { issueId: ID!, commentId: ID!, text: String! }`
- `input DeleteCommentInput { issueId: ID!, commentId: ID! }`
- `input ToggleIssueLikeInput { issueId: ID! }`

### 5.4 Queries

- `issues(input: ListIssuesInput): IssuesByStatus!`
- `issue(id: ID!): Issue!`
- `issueComments(input: ListIssueCommentsInput!): CommentsPage!`
- `issueInteractions(issueIds: [ID!]!): [IssueInteraction!]!`

### 5.5 Mutations

- `createIssue(input: CreateIssueInput!): Issue!`
- `updateIssue(id: ID!, input: UpdateIssueInput!): Issue!`
- `deleteIssue(id: ID!): Boolean!` (retorna `true` em sucesso)
- `createComment(input: CreateCommentInput!): Comment!`
- `updateComment(input: UpdateCommentInput!): Comment!`
- `deleteComment(input: DeleteCommentInput!): Boolean!`
- `toggleIssueLike(input: ToggleIssueLikeInput!): LikeResult!`

## 6) Comportamento esperado por operacao

### 6.1 Listagem de issues

- Filtro opcional por status.
- Busca opcional por `title` (contains, case-insensitive).
- Ordenacao opcional por `issueNumber` com direcao asc/desc.
- Resposta agrupada por status (`backlog`, `todo`, `inProgress`, `done`).
- Cada card inclui `comments` como contagem.

### 6.2 Obter issue por id

- Retorna issue completa.
- Inclui `comments` como contagem de comentarios.
- Se nao existir: erro de "Issue not found".

### 6.3 Criar issue

- Valida `title` e `description` nao vazios.
- `status` default para backlog quando ausente.
- `likes` inicia em 0 e `comments` em 0.

### 6.4 Atualizar issue

- Atualizacao parcial.
- Se nao existir: erro de "Issue not found".
- Retorna issue atualizada com contagem de comentarios.

### 6.5 Excluir issue

- Remove issue por id.
- Se nao existir: erro de "Issue not found".
- Em sucesso retorna booleano true (equivalente ao 204 REST).

### 6.6 Listar comentarios de issue

- Exige issue existente.
- Ordenacao por `createdAt` desc (mais recentes primeiro).
- Suporta `limit` (1..100, default 50) e `offset` (>=0, default 0).
- Retorna `comments`, `total`, `limit`, `offset`.

### 6.7 Criar comentario

- Requer autenticacao.
- Requer issue existente.
- `author` vem do usuario autenticado (`name`, `image`).
- Se `image` ausente, usar string vazia.

### 6.8 Atualizar comentario

- Requer autenticacao.
- Requer comentario existente.
- Somente autor pode editar.
- Se usuario nao for autor: erro de permissao.

### 6.9 Excluir comentario

- Requer autenticacao.
- Requer comentario existente.
- Somente autor pode excluir.

### 6.10 Toggle like de issue

- Requer autenticacao.
- Requer issue existente.
- Se usuario ja curtiu: remove like e decrementa contador.
- Se usuario nao curtiu: cria like e incrementa contador.
- Retorna `{ id, likes, liked }` da issue apos operacao.

### 6.11 Interactions em lote

- Entrada: lista de `issueIds`.
- Para cada issue existente na lista, retornar:
  - `issueId`
  - `isLiked` (dependente do usuario autenticado; false para anonimo)
  - `likesCount`
- Se lista vazia, retornar lista vazia.

## 7) Autenticacao e autorizacao

### 7.1 Contexto de auth

O servidor deve popular no contexto GraphQL:
- `current_user` (ou `None`)
- `current_session` (ou `None`)

### 7.2 Operacoes publicas

- `issues`
- `issue`
- `issueComments`
- `issueInteractions` (funciona anonimo, mas `isLiked` sera false sem usuario)

### 7.3 Operacoes protegidas

- `createComment`
- `updateComment`
- `deleteComment`
- `toggleIssueLike`

### 7.4 Ownership

Para update/delete de comentario, validar ownership comparando usuario autenticado com autor persistido.

## 8) Erros e validacao

### 8.1 Formato padrao de erro

Seguir payload semantico equivalente:

- `error: string`
- `message: string`

### 8.2 Categorias minimas

- `BAD_REQUEST` para validacoes de input (campos obrigatorios, enum invalido, limites de paginacao etc.)
- `UNAUTHORIZED` para falta de autenticacao
- `FORBIDDEN` para falta de permissao (ownership)
- `NOT_FOUND` para recursos inexistentes

Em GraphQL, retornar em `errors[]` com `extensions.code` apropriado e incluir metadados para mapear para `error/message` no cliente quando necessario.

## 9) Requisitos nao funcionais

1. Usar transacoes em operacoes de like/unlike para garantir consistencia entre tabela de likes e contador denormalizado.
2. Garantir indices para consultas frequentes:
   - issue status
   - issue title (ou estrategia de busca equivalente)
   - comments por issue_id e created_at
   - issue_likes por (issue_id, user_id)
3. Definir timezone consistente (UTC) para `DateTime`.
4. Garantir compatibilidade CORS com o frontend local.

## 10) Criterios de aceite

1. Todas as operacoes listadas no escopo estao disponiveis em GraphQL.
2. Regras de autenticacao/autorizacao equivalentes ao backend atual estao cobertas.
3. Respostas de dominio (issues/comments/likes/interactions) mantem semantica funcional esperada.
4. Erros previsiveis estao mapeados com codigos e mensagens consistentes.
5. Existe suite de testes (unit + integracao) cobrindo fluxos felizes e de erro para cada operacao.

## 11) Fora de escopo (nesta iteracao)

- Novas features alem da paridade (ex.: anexos, labels, prioridades, historico de auditoria).
- Mudancas no comportamento funcional do frontend.
- Otimizacoes prematuras que alterem contrato/semantica.

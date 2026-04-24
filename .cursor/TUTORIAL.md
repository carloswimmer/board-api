# Tutorial: Rebuild `board-api` with FastAPI + Strawberry GraphQL

Abaixo está um tutorial prático, seguindo o `PLAN.md` e o `SPEC.md`, para implementar a API com **paridade funcional** ao backend atual.

---

## Regra de commits durante o tutorial

- Sempre que concluir um passo relevante com verificação mínima (ex.: setup finalizado, dependências instaladas, app subindo, migration aplicada, testes de um slice passando), **sugira criar um commit**.
- Mantenha commits pequenos e com escopo único (um milestone, sub-milestone, ou resolver slice por commit).
- Mensagens de commit devem refletir o objetivo do passo concluído.

---

## 0) Objetivo e stack

Você vai construir uma API GraphQL em Python com:

- `FastAPI`
- `Strawberry GraphQL`
- `PostgreSQL`
- Auth com GitHub + sessão
- Gerenciamento com `uv`

Escopo funcional obrigatório (issues, comments, likes, interactions, auth rules, errors) vem daqui:

```md
Recreate the behavior defined in `/Users/carloswimmer/Documents/Estudos/Frameworks/python-fast-api/board-api/.cursor/SPEC.md` using:
- FastAPI
- Strawberry GraphQL
- PostgreSQL
- GitHub authentication
- `uv` for project/dependency management
```

---

## 1) Milestone 1 — Bootstrap do projeto

### 1.1 Criar projeto e dependências

No diretório `board-api`:

```bash
uv init
uv venv
source .venv/bin/activate
```

Instale dependências base:

```bash
uv add fastapi strawberry-graphql sqlalchemy alembic psycopg[binary] pydantic-settings python-dotenv
uv add httpx authlib itsdangerous
uv add -d pytest pytest-asyncio anyio
```

> Se quiser testes de integração com banco real por teste, adicione `testcontainers`.

### 1.2 Estrutura de pastas

Crie esta estrutura:

- `app/main.py`
- `app/graphql/` (`schema.py`, `types.py`, `inputs.py`, `resolvers/`)
- `app/db/` (`models.py`, `session.py`, `base.py`)
- `app/auth/` (`github.py`, `session.py`, `dependencies.py`)
- `tests/unit/`
- `tests/integration/`

### 1.3 Variáveis de ambiente

Crie `.env.example` com:

- `DATABASE_URL`
- `APP_SECRET`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `GITHUB_CALLBACK_URL`
- `CORS_ORIGINS`

### 1.4 Banco local com Docker

Use `docker-compose.yml` com serviço Postgres.
Suba o banco:

```bash
docker compose up -d
```

---

## 2) Milestone 2 — Runtime pronto antes das features

### 2.1 FastAPI + GraphQL mount

- Inicialize `FastAPI` em `app/main.py`
- Monte endpoint GraphQL (`/graphql`) via Strawberry ASGI
- Adicione `/health` para smoke test

### 2.2 Configuração de settings e DB

- `pydantic-settings` para validar envs no startup
- Engine + session factory SQLAlchemy
- Check de conexão no startup

### 2.3 Alembic baseline

```bash
alembic init migrations
alembic revision -m "baseline"
alembic upgrade head
```

### 2.4 Verificações mínimas

Confirme:

- app sobe sem erro
- `/graphql` responde
- conexão com DB funciona

---

## 3) Milestone 3 — Planeje testes antes dos resolvers

### 3.1 Crie um checklist SPEC → teste

Para cada operação no SPEC, tenha pelo menos:

- 1 teste feliz
- 1 teste de erro previsível (`BAD_REQUEST`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`)

### 3.2 Fixtures recomendadas

- usuário autenticado e anônimo
- seed de issues/comments/likes
- banco isolado por suite/execução

---

## 4) Milestone 4 — Modelo de dados e migrações

Implemente modelos:

- `issues`
- `comments`
- `issue_likes`
- `users`
- `sessions`

Restrições-chave do SPEC:

- `issue_number` único e sequencial
- unique `(issue_id, user_id)` em likes
- índices para status/título/comments

Campos obrigatórios (Issue/Comment/Like) estão definidos em `SPEC.md` seção 3.

---

## 5) Milestone 5 — Auth GitHub + contexto GraphQL

### 5.1 Fluxo OAuth

- login redirect para GitHub
- callback, persistência de usuário e sessão
- cookie de sessão seguro

### 5.2 Contexto GraphQL

No contexto de request, injete:

- `current_user` (ou `None`)
- `current_session` (ou `None`)

### 5.3 Regras de acesso

Públicas:

- `issues`, `issue`, `issueComments`, `issueInteractions`

Protegidas:

- `createComment`, `updateComment`, `deleteComment`, `toggleIssueLike`

---

## 6) Milestone 6 — Contrato GraphQL (schema first)

Implemente exatamente os tipos/inputs/enums do SPEC:

- `IssueStatus`, `Issue`, `IssueCard`, `Comment`, `CommentsPage`, `IssueInteraction`, etc.
- queries: `issues`, `issue`, `issueComments`, `issueInteractions`
- mutations: `createIssue`, `updateIssue`, `deleteIssue`, `createComment`, `updateComment`, `deleteComment`, `toggleIssueLike`

Mapeamento enum importante:

```md
- `scalar DateTime`
- `enum IssueStatus { BACKLOG TODO IN_PROGRESS DONE }`

Mapeamento de status:
- `BACKLOG <-> "backlog"`
- `TODO <-> "todo"`
- `IN_PROGRESS <-> "in_progress"`
- `DONE <-> "done"`
```

---

## 7) Milestone 7 — Resolvers em slices verticais (ordem)

Siga a ordem do plano:

1. `issues` (filtros/busca/sort/group by status + comments count)
2. `issue`
3. `createIssue`, `updateIssue`, `deleteIssue`
4. `issueComments` (paginação e ordenação)
5. `createComment`, `updateComment`, `deleteComment` (ownership)
6. `issueInteractions`
7. `toggleIssueLike` (transacional)

Para cada slice:

- implementar
- testar (unit + integration relevantes)
- refatorar
- commitar pequeno

---

## 8) Milestone 8 — Validação e semântica de erro

Padronize erros GraphQL com `extensions.code`:

- `BAD_REQUEST`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `NOT_FOUND`

Regras críticas:

- validação de campos obrigatórios
- ownership de comentário (apenas autor edita/deleta)
- timezone UTC
- semântica compatível com backend atual

---

## 9) Milestone 9 — Fechamento e documentação

### 9.1 Rodar suíte completa

```bash
pytest
```

### 9.2 Scripts úteis no `pyproject.toml`

- run server
- migrations up/down
- test unit
- test integration

### 9.3 README final

Inclua:

- setup de ambiente
- subir Postgres
- migrations
- executar server
- rodar testes
- exemplos de operações GraphQL

---

## Checklist final de aceite (baseado no SPEC)

- Todas as queries/mutations obrigatórias disponíveis
- Auth + autorização equivalentes
- Domínio de issues/comments/likes/interactions com paridade funcional
- Erros consistentes por categoria
- Testes cobrindo happy path e erros por operação

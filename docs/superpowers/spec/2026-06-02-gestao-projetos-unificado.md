# Spec: Módulo Unificado Gestão de Projetos

## Visão Geral

Combinar os módulos standalone `modulo-projeto`, `modulo-tarefas`, `modulo-recursos`, `modulo-cronograma` e `modulo-dashboard` em um único módulo `modulo-gestao-projetos` com múltiplas entidades e múltiplos frontends (cada entidade em sua própria aba no GrindX).

## Tech Stack

| Componente | Tecnologia |
|------------|------------|
| Frontend | HTML puro + CSS puro (`var(--...)`) + Vanilla JS |
| Backend | FastAPI + SQLAlchemy + PostgreSQL |
| Migrations | Alembic |
| Schema DB | `org` |
| Testes | pytest (unit + integration com SQLite) |

## Entidades

### 1. Projeto (tabela própria)

**Tabela:** `org.projetos`

| Campo | Tipo | Constraints |
|-------|------|-------------|
| `id` | int | PK, autoincrement |
| `nome` | String(200) | NOT NULL, indexado |
| `descricao` | Text | nullable |
| `status` | String(20) | NOT NULL, default `"planning"` |
| `data_inicio` | Date | NOT NULL |
| `data_fim` | Date | NOT NULL |
| `cor` | String(7) | NOT NULL, default `"#3b82f6"` |
| `gerente_id` | int | FK → `iam.usuarios.id`, nullable |
| `ativo` | bool | NOT NULL, default True |
| `criado_em` | DateTime(tz) | server_default now() |
| `atualizado_em` | DateTime(tz) | server_default now(), onupdate now() |

**Status válidos:** `planning`, `active`, `completed`, `on-hold`

**Rotas:** `/v1/projetos` (CRUD padrão)

---

### 2. Tarefa (tabela própria + tabela de registros)

**Tabela:** `org.tarefas`

| Campo | Tipo | Constraints |
|-------|------|-------------|
| `id` | int | PK, autoincrement |
| `titulo` | String(255) | NOT NULL, indexado |
| `descricao` | Text | nullable |
| `status` | String(20) | NOT NULL, default `"todo"` |
| `prioridade` | String(10) | NOT NULL, default `"medium"` |
| `data_inicio` | Date | NOT NULL |
| `data_fim` | Date | NOT NULL |
| `progresso` | int | NOT NULL, default 0 (0-100) |
| `projeto_id` | int | FK → `org.projetos.id`, CASCADE, nullable |
| `responsavel_id` | int | FK → `org.recursos.id`, SET NULL, nullable |
| `ativo` | bool | NOT NULL, default True |
| `criado_em` | DateTime(tz) | server_default now() |
| `atualizado_em` | DateTime(tz) | server_default now(), onupdate now() |

**Status válidos:** `todo`, `in-progress`, `done`
**Prioridade válida:** `low`, `medium`, `high`

**Tabela:** `org.registros_tarefas`

| Campo | Tipo | Constraints |
|-------|------|-------------|
| `id` | int | PK, autoincrement |
| `tarefa_id` | int | FK → `org.tarefas.id`, CASCADE, NOT NULL |
| `tipo` | String(20) | NOT NULL, default `"log"` |
| `conteudo` | Text | NOT NULL |
| `autor_id` | int | FK → `org.recursos.id`, SET NULL, nullable |
| `ativo` | bool | NOT NULL, default True |
| `criado_em` | DateTime(tz) | server_default now() |

**Tipo válido:** `log`, `decisao`

**Rotas:**
- `/v1/tarefas` (CRUD com filtros: projeto_id, status)
- `/v1/tarefas/{id}/registros` (CRUD para registros)

---

### 3. Recurso (tabela própria)

**Tabela:** `org.recursos`

| Campo | Tipo | Constraints |
|-------|------|-------------|
| `id` | int | PK, autoincrement |
| `user_id` | int | FK → `iam.usuarios.id`, NOT NULL |
| `projeto_id` | int | NOT NULL |
| `cargo_contexto` | String(100) | nullable |
| `cor` | String(7) | NOT NULL, default `"#3b82f6"` |
| `alocado` | bool | NOT NULL, default True |
| `criado_em` | DateTime(tz) | server_default now() |
| `atualizado_em` | DateTime(tz) | server_default now(), onupdate now() |

**Constraints:** `UniqueConstraint("user_id", "projeto_id")`

**Rotas:** `/v1/recursos` (CRUD com filtro: projeto_id)

---

### 4. Dashboard (visualização — sem tabela)

**Rotas:** `GET /v1/dashboard`

**Schemas de resposta:**
- `DashboardMetrics` — KPIs gerais
- `ProximoPrazo` — tarefas com prazo nos próximos 7 dias
- `TarefaAtrasada` — tarefas atrasadas
- `ProgressoProjeto` — progresso por projeto
- `CargaTrabalho` — carga por recurso

---

### 5. Cronograma/Gantt (visualização — sem tabela)

**Rotas:** `GET /v1/cronograma/tarefas`

**Schema de resposta:** `TarefaGanttResponse` — tarefas com dados de projeto e responsável para timeline Gantt

---

## Estrutura de Diretórios

```
Project_Management/modulo-gestao-projetos/
├── module.json
├── app/modules/gestao_projetos/
│   ├── __init__.py
│   ├── base.py                          # GestaoProjetosBase
│   ├── models/
│   │   ├── __init__.py
│   │   ├── projeto.py                   # Projeto
│   │   ├── tarefa.py                    # Tarefa
│   │   ├── registro_tarefa.py           # RegistroTarefa
│   │   └── recurso.py                   # Recurso
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── projeto.py                   # ProjetoCreate/Update/Response
│   │   ├── tarefa.py                    # TarefaCreate/Update/Response
│   │   ├── registro_tarefa.py           # RegistroCreate/Update/Response
│   │   ├── recurso.py                   # RecursoCreate/Update/Response
│   │   ├── dashboard.py                 # DashboardMetrics/Response
│   │   └── cronograma.py               # TarefaGanttResponse
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── projeto_repository.py
│   │   ├── tarefa_repository.py
│   │   ├── registro_repository.py
│   │   ├── recurso_repository.py
│   │   ├── dashboard_repository.py
│   │   └── cronograma_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── projeto_service.py
│   │   ├── tarefa_service.py
│   │   ├── registro_service.py
│   │   ├── recurso_service.py
│   │   ├── dashboard_service.py
│   │   └── cronograma_service.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── projeto_router.py
│   │   ├── tarefa_router.py
│   │   ├── recurso_router.py
│   │   ├── dashboard_router.py
│   │   └── cronograma_router.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_projeto_unit.py
│   │   ├── test_projeto_integration.py
│   │   ├── test_tarefa_unit.py
│   │   ├── test_tarefa_integration.py
│   │   ├── test_recurso_unit.py
│   │   ├── test_recurso_integration.py
│   │   ├── test_dashboard_integration.py
│   │   └── test_cronograma_integration.py
│   ├── export.py
│   └── README.md
├── frontend/
│   ├── projeto/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── tarefas/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── recursos/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── dashboard/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   └── cronograma/
│       ├── index.html
│       ├── script.js
│       └── style.css
├── migration/
│   └── {revision}_create_tables.py
├── Makefile
├── requirements.txt
├── pytest.ini
└── run_tests.ps1
```

## module.json

```json
{
  "module_name": "gestao_projetos",
  "entity_name": "GestaoProjetos",
  "version": "1.0.0",
  "schema_name": "org",
  "tables": ["projetos", "tarefas", "registros_tarefas", "recursos"],
  "route_prefix": "/v1",
  "route_tag": "Gestão de Projetos",
  "frontend_tabs": [
    {
      "name": "Dashboard",
      "url": "modules/gestao_projetos/dashboard/index.html",
      "menu_icone": "chart-bar",
      "order": 1
    },
    {
      "name": "Projetos",
      "url": "modules/gestao_projetos/projeto/index.html",
      "menu_icone": "folder",
      "order": 2
    },
    {
      "name": "Tarefas",
      "url": "modules/gestao_projetos/tarefas/index.html",
      "menu_icone": "check-square",
      "order": 3
    },
    {
      "name": "Recursos",
      "url": "modules/gestao_projetos/recursos/index.html",
      "menu_icone": "users",
      "order": 4
    },
    {
      "name": "Cronograma",
      "url": "modules/gestao_projetos/cronograma/index.html",
      "menu_icone": "calendar",
      "order": 5
    }
  ],
  "menu_label": "Gestão de Projetos",
  "menu_icone": "briefcase",
  "role_minima": "operador",
  "dependencies": ["iam"]
}
```

## Rotas da API

### Projeto
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/v1/projetos` | Listar (paginado) |
| GET | `/v1/projetos/{id}` | Buscar por ID |
| POST | `/v1/projetos` | Criar |
| PUT | `/v1/projetos/{id}` | Atualizar |
| DELETE | `/v1/projetos/{id}` | Desativar |

### Tarefa
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/v1/tarefas` | Listar (paginado, filtros: projeto_id, status) |
| GET | `/v1/tarefas/{id}` | Buscar por ID |
| POST | `/v1/tarefas` | Criar |
| PUT | `/v1/tarefas/{id}` | Atualizar |
| DELETE | `/v1/tarefas/{id}` | Desativar |
| GET | `/v1/tarefas/{id}/registros` | Listar registros |
| POST | `/v1/tarefas/{id}/registros` | Criar registro |
| PUT | `/v1/tarefas/registros/{id}` | Atualizar registro |
| DELETE | `/v1/tarefas/registros/{id}` | Desativar registro |

### Recurso
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/v1/recursos` | Listar (paginado, filtro: projeto_id) |
| GET | `/v1/recursos/{id}` | Buscar por ID |
| POST | `/v1/recursos` | Alocar recurso |
| PUT | `/v1/recursos/{id}` | Atualizar |
| DELETE | `/v1/recursos/{id}` | Desalocar |

### Dashboard
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/v1/dashboard` | Dados completos do dashboard |

### Cronograma
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/v1/cronograma/tarefas` | Tarefas para Gantt |

## Frontends (5 abas)

Cada aba é um HTML independente com seu próprio `script.js` e `style.css`:

1. **Dashboard** (`dashboard/`) — Métricas KPIs, gráficos de progresso, tarefas atrasadas, carga de trabalho
2. **Projetos** (`projeto/`) — CRUD de projetos com cards coloridos
3. **Tarefas** (`tarefas/`) — CRUD de tarefas com filtros por projeto/status, sistema de registros
4. **Recursos** (`recursos/`) — Alocação de recursos por projeto, gestão de equipe
5. **Cronograma** (`cronograma/`) — Visualização Gantt interativa das tarefas

**Regras para todos os frontends:**
- Zero dependências externas (sem CDN, sem frameworks)
- CSS usa apenas `var(--...)` para herdar skins do GrindX
- Eventos via delegated event bubbling
- Modais com `modal-overlay` + `modal-card`
- Templates com `<template>` ou template strings

## Migration

Uma única migration cria todas as tabelas:
- `org.projetos`
- `org.tarefas`
- `org.registros_tarefas`
- `org.recursos`

## Checklist de Implementação

- [ ] Criar estrutura de diretórios
- [ ] `base.py` com `GestaoProjetosBase`
- [ ] Models: Projeto, Tarefa, RegistroTarefa, Recurso
- [ ] Schemas: todos os Create/Update/Response
- [ ] Repositories: CRUD + queries customizadas (dashboard, cronograma)
- [ ] Services: lógica de negócio + validações
- [ ] Routers: todas as rotas documentadas
- [ ] `__init__.py` para cada camada
- [ ] `conftest.py` com fixtures SQLite
- [ ] Testes unitários (repo mockado)
- [ ] Testes de integração (SQLite real)
- [ ] Frontend: Dashboard (index.html + script.js + style.css)
- [ ] Frontend: Projetos
- [ ] Frontend: Tarefas
- [ ] Frontend: Recursos
- [ ] Frontend: Cronograma
- [ ] Migration Alembic
- [ ] `module.json`
- [ ] `export.py`
- [ ] `Makefile`, `requirements.txt`, `pytest.ini`, `run_tests.ps1`
- [ ] Todos os testes passando
- [ ] Gerar `.zip` com `make package`
- [ ] Verificar herança de skins (2+ skins)

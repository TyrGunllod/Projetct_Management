# Módulo Unificado Gestão de Projetos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Combinar 5 módulos standalone (projeto, tarefas, recursos, cronograma, dashboard) em um único módulo `modulo-gestao-projetos` com 5 abas frontend independentes.

**Architecture:** Módulo único FastAPI com 4 entidades com tabela própria (Projeto, Tarefa, RegistroTarefa, Recurso) e 2 módulos de visualização (Dashboard, Cronograma). Cada entidade tem seu frontend HTML para aba separada no GrindX. Backend segue padrão Repository/Service/Router com SQLAlchemy 2.0 e Pydantic v2.

**Tech Stack:** FastAPI + SQLAlchemy 2.0 (Mapped[T]) + PostgreSQL (schema `org`) + Pydantic v2 + Alembic + HTML puro + CSS puro (var(--...)) + Vanilla JS

---

## File Structure

```
Project_Management/modulo-gestao-projetos/
├── module.json
├── app/modules/gestao_projetos/
│   ├── __init__.py
│   ├── base.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── projeto.py
│   │   ├── tarefa.py
│   │   ├── registro_tarefa.py
│   │   └── recurso.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── projeto.py
│   │   ├── tarefa.py
│   │   ├── registro_tarefa.py
│   │   ├── recurso.py
│   │   ├── dashboard.py
│   │   └── cronograma.py
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

---

### Task 1: Criar estrutura base e base.py

**Files:**
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/__init__.py`
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/base.py`
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/models/__init__.py`
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/schemas/__init__.py`
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/repositories/__init__.py`
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/services/__init__.py`
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/routers/__init__.py`
- Create: `Project_Management/modulo-gestao-projetos/app/modules/gestao_projetos/tests/__init__.py`

- [ ] **Step 1: Criar diretório raiz do módulo**

```powershell
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\app\modules\gestao_projetos\models" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\app\modules\gestao_projetos\schemas" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\app\modules\gestao_projetos\repositories" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\app\modules\gestao_projetos\services" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\app\modules\gestao_projetos\routers" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\app\modules\gestao_projetos\tests" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\frontend\projeto" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\frontend\tarefas" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\frontend\recursos" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\frontend\dashboard" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\frontend\cronograma" -Force
New-Item -ItemType Directory -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos\migration" -Force
```

- [ ] **Step 2: Criar `__init__.py` da raiz do módulo**

```python
# app/modules/gestao_projetos/__init__.py
```

- [ ] **Step 3: Criar `base.py`**

```python
from sqlalchemy.orm import DeclarativeBase
from app.modules.iam.base import metadata, reg


class GestaoProjetosBase(DeclarativeBase):
    registry = reg
    metadata = metadata
    __table_args__ = {"schema": "org"}
```

- [ ] **Step 4: Criar `__init__.py` de cada camada**

```python
# models/__init__.py
from app.modules.gestao_projetos.models.projeto import Projeto
from app.modules.gestao_projetos.models.tarefa import Tarefa
from app.modules.gestao_projetos.models.registro_tarefa import RegistroTarefa
from app.modules.gestao_projetos.models.recurso import Recurso

__all__ = ["Projeto", "Tarefa", "RegistroTarefa", "Recurso"]
```

```python
# schemas/__init__.py
from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate, ProjetoUpdate, ProjetoResponse
from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate, TarefaUpdate, TarefaResponse
from app.modules.gestao_projetos.schemas.registro_tarefa import RegistroCreate, RegistroUpdate, RegistroResponse
from app.modules.gestao_projetos.schemas.recurso import RecursoCreate, RecursoUpdate, RecursoResponse

__all__ = [
    "ProjetoCreate", "ProjetoUpdate", "ProjetoResponse",
    "TarefaCreate", "TarefaUpdate", "TarefaResponse",
    "RegistroCreate", "RegistroUpdate", "RegistroResponse",
    "RecursoCreate", "RecursoUpdate", "RecursoResponse",
]
```

```python
# repositories/__init__.py
from app.modules.gestao_projetos.repositories.projeto_repository import ProjetoRepository
from app.modules.gestao_projetos.repositories.tarefa_repository import TarefaRepository
from app.modules.gestao_projetos.repositories.registro_repository import RegistroRepository
from app.modules.gestao_projetos.repositories.recurso_repository import RecursoRepository
from app.modules.gestao_projetos.repositories.dashboard_repository import DashboardRepository
from app.modules.gestao_projetos.repositories.cronograma_repository import CronogramaRepository

__all__ = [
    "ProjetoRepository", "TarefaRepository", "RegistroRepository",
    "RecursoRepository", "DashboardRepository", "CronogramaRepository",
]
```

```python
# services/__init__.py
from app.modules.gestao_projetos.services.projeto_service import ProjetoService
from app.modules.gestao_projetos.services.tarefa_service import TarefaService
from app.modules.gestao_projetos.services.registro_service import RegistroService
from app.modules.gestao_projetos.services.recurso_service import RecursoService
from app.modules.gestao_projetos.services.dashboard_service import DashboardService
from app.modules.gestao_projetos.services.cronograma_service import CronogramaService

__all__ = [
    "ProjetoService", "TarefaService", "RegistroService",
    "RecursoService", "DashboardService", "CronogramaService",
]
```

```python
# routers/__init__.py
from app.modules.gestao_projetos.routers.projeto_router import router as projeto_router
from app.modules.gestao_projetos.routers.tarefa_router import router as tarefa_router
from app.modules.gestao_projetos.routers.recurso_router import router as recurso_router
from app.modules.gestao_projetos.routers.dashboard_router import router as dashboard_router
from app.modules.gestao_projetos.routers.cronograma_router import router as cronograma_router

__all__ = [
    "projeto_router", "tarefa_router", "recurso_router",
    "dashboard_router", "cronograma_router",
]
```

```python
# tests/__init__.py
```

- [ ] **Step 5: Verificar que a estrutura foi criada**

Run: `Get-ChildItem -Path "D:\_Projetos\Project_Management\modulo-gestao-projetos" -Recurse -Directory | Select-Object FullName`
Expected: Lista dos 16 diretórios criados

---

### Task 2: Models — Projeto, Tarefa, RegistroTarefa, Recurso

**Files:**
- Create: `app/modules/gestao_projetos/models/projeto.py`
- Create: `app/modules/gestao_projetos/models/tarefa.py`
- Create: `app/modules/gestao_projetos/models/registro_tarefa.py`
- Create: `app/modules/gestao_projetos/models/recurso.py`

- [ ] **Step 1: Criar model Projeto**

```python
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.gestao_projetos.base import GestaoProjetosBase


class Projeto(GestaoProjetosBase):
    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True, comment="Nome")
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Descricao")
    status: Mapped[str] = mapped_column(String(20), default="planning", nullable=False, comment="Status")
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False, comment="Data de inicio")
    data_fim: Mapped[date] = mapped_column(Date, nullable=False, comment="Data de termino")
    cor: Mapped[str] = mapped_column(String(7), default="#3b82f6", nullable=False, comment="Cor hexadecimal")
    gerente_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("iam.usuarios.id"), nullable=True, comment="ID do gerente")
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="Se esta ativo")
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Projeto(id={self.id}, nome='{self.nome}')>"
```

- [ ] **Step 2: Criar model Tarefa**

```python
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.gestao_projetos.base import GestaoProjetosBase


class Tarefa(GestaoProjetosBase):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="Titulo da tarefa")
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Descricao detalhada")
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False, comment="todo | in-progress | done")
    prioridade: Mapped[str] = mapped_column(String(10), default="medium", nullable=False, comment="low | medium | high")
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False, comment="Data de inicio")
    data_fim: Mapped[date] = mapped_column(Date, nullable=False, comment="Data de termino")
    progresso: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="Progresso 0-100")
    projeto_id: Mapped[int | None] = mapped_column(
        ForeignKey("org.projetos.id", ondelete="CASCADE"),
        nullable=True, index=True, comment="FK para projetos",
    )
    responsavel_id: Mapped[int | None] = mapped_column(
        ForeignKey("org.recursos.id", ondelete="SET NULL"),
        nullable=True, index=True, comment="FK para recursos (responsavel)",
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="Se esta ativo")
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Tarefa(id={self.id}, titulo='{self.titulo}', status='{self.status}')>"
```

- [ ] **Step 3: Criar model RegistroTarefa**

```python
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.gestao_projetos.base import GestaoProjetosBase


class RegistroTarefa(GestaoProjetosBase):
    __tablename__ = "registros_tarefas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tarefa_id: Mapped[int] = mapped_column(
        ForeignKey("org.tarefas.id", ondelete="CASCADE"),
        nullable=False, index=True, comment="FK para tarefas",
    )
    tipo: Mapped[str] = mapped_column(String(20), default="log", nullable=False, comment="log | decisao")
    conteudo: Mapped[str] = mapped_column(Text, nullable=False, comment="Conteudo do registro")
    autor_id: Mapped[int | None] = mapped_column(
        ForeignKey("org.recursos.id", ondelete="SET NULL"),
        nullable=True, index=True, comment="FK para recursos (autor)",
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="Se esta ativo")
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<RegistroTarefa(id={self.id}, tarefa_id={self.tarefa_id}, tipo='{self.tipo}')>"
```

- [ ] **Step 4: Criar model Recurso**

```python
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.gestao_projetos.base import GestaoProjetosBase


class Recurso(GestaoProjetosBase):
    __tablename__ = "recursos"

    __table_args__ = (
        UniqueConstraint("user_id", "projeto_id", name="uq_recurso_user_projeto"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("iam.usuarios.id"), nullable=False, comment="FK para usuario do IAM",
    )
    projeto_id: Mapped[int] = mapped_column(nullable=False, comment="ID do projeto")
    cargo_contexto: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Cargo/funcao no contexto do projeto")
    cor: Mapped[str] = mapped_column(String(7), default="#3b82f6", nullable=False, comment="Cor de identificacao visual")
    alocado: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="Se esta ativamente alocado")
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Recurso(id={self.id}, user_id={self.user_id}, projeto_id={self.projeto_id})>"
```

---

### Task 3: Schemas — Todos os Create/Update/Response

**Files:**
- Create: `app/modules/gestao_projetos/schemas/projeto.py`
- Create: `app/modules/gestao_projetos/schemas/tarefa.py`
- Create: `app/modules/gestao_projetos/schemas/registro_tarefa.py`
- Create: `app/modules/gestao_projetos/schemas/recurso.py`
- Create: `app/modules/gestao_projetos/schemas/dashboard.py`
- Create: `app/modules/gestao_projetos/schemas/cronograma.py`

- [ ] **Step 1: Criar schemas Projeto**

```python
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjetoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=200, description="Nome")
    descricao: str | None = Field(default=None, description="Descricao")
    status: str = Field(default="planning", pattern=r"^(planning|active|completed|on-hold)$")
    data_inicio: date = Field(..., description="Data de inicio")
    data_fim: date = Field(..., description="Data de termino")
    cor: str = Field(default="#3b82f6", min_length=7, max_length=7, description="Cor hexadecimal")
    gerente_id: int | None = Field(default=None, description="ID do gerente")


class ProjetoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=200)
    descricao: str | None = Field(default=None)
    status: str | None = Field(default=None, pattern=r"^(planning|active|completed|on-hold)$")
    data_inicio: date | None = Field(default=None)
    data_fim: date | None = Field(default=None)
    cor: str | None = Field(default=None, min_length=7, max_length=7)
    gerente_id: int | None = Field(default=None)


class ProjetoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    status: str
    data_inicio: date
    data_fim: date
    cor: str
    gerente_id: int | None
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 2: Criar schemas Tarefa**

```python
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=255, description="Titulo")
    descricao: str | None = Field(default=None, description="Descricao")
    status: str = Field(default="todo", pattern=r"^(todo|in-progress|done)$")
    prioridade: str = Field(default="medium", pattern=r"^(low|medium|high)$")
    data_inicio: date = Field(..., description="Data de inicio")
    data_fim: date = Field(..., description="Data de termino")
    progresso: int = Field(default=0, ge=0, le=100, description="Progresso 0-100")
    projeto_id: int | None = Field(default=None, description="ID do projeto")
    responsavel_id: int | None = Field(default=None, description="ID do responsavel")

    @field_validator("data_fim")
    @classmethod
    def validate_data_fim(cls, v: date, info) -> date:
        if "data_inicio" in info.data and v < info.data["data_inicio"]:
            raise ValueError("data_fim deve ser >= data_inicio")
        return v


class TarefaUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=2, max_length=255)
    descricao: str | None = Field(default=None)
    status: str | None = Field(default=None, pattern=r"^(todo|in-progress|done)$")
    prioridade: str | None = Field(default=None, pattern=r"^(low|medium|high)$")
    data_inicio: date | None = Field(default=None)
    data_fim: date | None = Field(default=None)
    progresso: int | None = Field(default=None, ge=0, le=100)
    projeto_id: int | None = Field(default=None)
    responsavel_id: int | None = Field(default=None)


class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str | None
    status: str
    prioridade: str
    data_inicio: date
    data_fim: date
    progresso: int
    projeto_id: int | None
    responsavel_id: int | None
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 3: Criar schemas RegistroTarefa**

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RegistroCreate(BaseModel):
    tipo: str = Field(default="log", pattern=r"^(log|decisao)$")
    conteudo: str = Field(..., min_length=1, description="Conteudo do registro")
    autor_id: int | None = Field(default=None, description="ID do autor")


class RegistroUpdate(BaseModel):
    tipo: str | None = Field(default=None, pattern=r"^(log|decisao)$")
    conteudo: str | None = Field(default=None, min_length=1)


class RegistroResponse(BaseModel):
    id: int
    tarefa_id: int
    tipo: str
    conteudo: str
    autor_id: int | None
    ativo: bool
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 4: Criar schemas Recurso**

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RecursoCreate(BaseModel):
    user_id: int = Field(..., description="ID do usuario IAM")
    projeto_id: int = Field(..., description="ID do projeto")
    cargo_contexto: str | None = Field(default=None, max_length=100, description="Cargo/funcao")
    cor: str = Field(default="#3b82f6", pattern=r"^#[0-9a-fA-F]{6}$", description="Cor hexadecimal")


class RecursoUpdate(BaseModel):
    cargo_contexto: str | None = Field(default=None, max_length=100)
    cor: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    alocado: bool | None = Field(default=None)


class RecursoResponse(BaseModel):
    id: int
    user_id: int
    projeto_id: int
    cargo_contexto: str | None
    cor: str
    alocado: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 5: Criar schemas Dashboard**

```python
from datetime import date

from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_projetos: int
    projetos_ativos: int
    total_tarefas: int
    tarefas_concluidas: int
    tarefas_em_progresso: int
    tarefas_a_fazer: int
    total_recursos: int
    progresso_geral: int


class ProximoPrazo(BaseModel):
    id: int
    titulo: str
    data_fim: date
    dias_restantes: int
    projeto_id: int | None
    project_name: str | None
    project_color: str | None


class TarefaAtrasada(BaseModel):
    id: int
    titulo: str
    data_fim: date
    dias_atraso: int
    projeto_id: int | None
    project_name: str | None
    project_color: str | None


class ProgressoProjeto(BaseModel):
    id: int
    nome: str
    cor: str
    total_tarefas: int
    tarefas_concluidas: int
    progresso: int


class CargaTrabalho(BaseModel):
    id: int
    nome: str
    cor: str
    tarefas_ativas: int
    tarefas_concluidas: int


class DashboardResponse(BaseModel):
    metrics: DashboardMetrics
    proximos_prazos: list[ProximoPrazo]
    tarefas_atrasadas: list[TarefaAtrasada]
    total_tarefas_atrasadas: int
    progresso_projetos: list[ProgressoProjeto]
    carga_trabalho: list[CargaTrabalho]
```

- [ ] **Step 6: Criar schemas Cronograma**

```python
from datetime import date

from pydantic import BaseModel


class TarefaGanttResponse(BaseModel):
    id: int
    titulo: str
    status: str
    prioridade: str
    data_inicio: date
    data_fim: date
    progresso: int
    projeto_id: int | None
    project_name: str | None
    project_color: str | None
    responsavel_id: int | None
    assignee_name: str | None
    assignee_color: str | None
```

---

### Task 4: Repositories — CRUD + Queries Customizadas

**Files:**
- Create: `app/modules/gestao_projetos/repositories/projeto_repository.py`
- Create: `app/modules/gestao_projetos/repositories/tarefa_repository.py`
- Create: `app/modules/gestao_projetos/repositories/registro_repository.py`
- Create: `app/modules/gestao_projetos/repositories/recurso_repository.py`
- Create: `app/modules/gestao_projetos/repositories/dashboard_repository.py`
- Create: `app/modules/gestao_projetos/repositories/cronograma_repository.py`

- [ ] **Step 1: Criar ProjetoRepository**

```python
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.gestao_projetos.models.projeto import Projeto
from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate, ProjetoUpdate


class ProjetoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_id(self, id: int) -> Projeto | None:
        stmt = select(Projeto).where(Projeto.id == id)
        return self.db.execute(stmt).scalar_one_or_none()

    def listar_todos(self, page: int = 1, page_size: int = 20) -> tuple[list[Projeto], int]:
        count_stmt = select(func.count()).select_from(Projeto)
        total = self.db.scalar(count_stmt) or 0
        stmt = select(Projeto).order_by(Projeto.id).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(stmt).all())
        return items, total

    def listar_ativos(self) -> list[Projeto]:
        stmt = select(Projeto).where(Projeto.ativo.is_(True)).order_by(Projeto.nome)
        return list(self.db.scalars(stmt).all())

    def buscar_por_nome(self, nome: str) -> list[Projeto]:
        stmt = select(Projeto).where(Projeto.nome.ilike(f"%{nome}%"))
        return list(self.db.scalars(stmt).all())

    def criar(self, dados: ProjetoCreate) -> Projeto:
        obj = Projeto(**dados.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def atualizar(self, obj: Projeto, dados: ProjetoUpdate) -> Projeto:
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def desativar(self, obj: Projeto) -> Projeto:
        obj.ativo = False
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

- [ ] **Step 2: Criar TarefaRepository**

```python
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.gestao_projetos.models.tarefa import Tarefa
from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate, TarefaUpdate


class TarefaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_id(self, id: int) -> Tarefa | None:
        stmt = select(Tarefa).where(Tarefa.id == id)
        return self.db.execute(stmt).scalar_one_or_none()

    def listar_todos(
        self, page: int = 1, page_size: int = 20,
        projeto_id: int | None = None, status: str | None = None,
    ) -> tuple[list[Tarefa], int]:
        stmt_base = select(Tarefa).where(Tarefa.ativo.is_(True))
        count_base = select(func.count()).select_from(Tarefa).where(Tarefa.ativo.is_(True))
        if projeto_id is not None:
            stmt_base = stmt_base.where(Tarefa.projeto_id == projeto_id)
            count_base = count_base.where(Tarefa.projeto_id == projeto_id)
        if status is not None:
            stmt_base = stmt_base.where(Tarefa.status == status)
            count_base = count_base.where(Tarefa.status == status)
        total = self.db.scalar(count_base) or 0
        stmt = stmt_base.order_by(Tarefa.data_inicio).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(stmt).all())
        return items, total

    def criar(self, dados: TarefaCreate) -> Tarefa:
        obj = Tarefa(**dados.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def atualizar(self, obj: Tarefa, dados: TarefaUpdate) -> Tarefa:
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def desativar(self, obj: Tarefa) -> Tarefa:
        obj.ativo = False
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

- [ ] **Step 3: Criar RegistroRepository**

```python
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.gestao_projetos.models.registro_tarefa import RegistroTarefa
from app.modules.gestao_projetos.schemas.registro_tarefa import RegistroCreate, RegistroUpdate


class RegistroRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_id(self, id: int) -> RegistroTarefa | None:
        stmt = select(RegistroTarefa).where(RegistroTarefa.id == id)
        return self.db.execute(stmt).scalar_one_or_none()

    def listar_por_tarefa(
        self, tarefa_id: int, page: int = 1, page_size: int = 50, tipo: str | None = None,
    ) -> tuple[list[RegistroTarefa], int]:
        stmt_base = select(RegistroTarefa).where(
            RegistroTarefa.tarefa_id == tarefa_id, RegistroTarefa.ativo.is_(True)
        )
        count_base = select(func.count()).select_from(RegistroTarefa).where(
            RegistroTarefa.tarefa_id == tarefa_id, RegistroTarefa.ativo.is_(True)
        )
        if tipo is not None:
            stmt_base = stmt_base.where(RegistroTarefa.tipo == tipo)
            count_base = count_base.where(RegistroTarefa.tipo == tipo)
        total = self.db.scalar(count_base) or 0
        stmt = stmt_base.order_by(RegistroTarefa.criado_em.desc()).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(stmt).all())
        return items, total

    def criar(self, tarefa_id: int, dados: RegistroCreate) -> RegistroTarefa:
        obj = RegistroTarefa(tarefa_id=tarefa_id, **dados.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def atualizar(self, obj: RegistroTarefa, dados: RegistroUpdate) -> RegistroTarefa:
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def desativar(self, obj: RegistroTarefa) -> RegistroTarefa:
        obj.ativo = False
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

- [ ] **Step 4: Criar RecursoRepository**

```python
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.gestao_projetos.models.recurso import Recurso
from app.modules.gestao_projetos.schemas.recurso import RecursoCreate, RecursoUpdate


class RecursoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_id(self, id: int) -> Recurso | None:
        stmt = select(Recurso).where(Recurso.id == id)
        return self.db.execute(stmt).scalar_one_or_none()

    def listar_todos(
        self, page: int = 1, page_size: int = 20, projeto_id: int | None = None,
    ) -> tuple[list[Recurso], int]:
        stmt_base = select(Recurso).where(Recurso.alocado.is_(True))
        count_base = select(func.count()).select_from(Recurso).where(Recurso.alocado.is_(True))
        if projeto_id is not None:
            stmt_base = stmt_base.where(Recurso.projeto_id == projeto_id)
            count_base = count_base.where(Recurso.projeto_id == projeto_id)
        total = self.db.scalar(count_base) or 0
        stmt = stmt_base.order_by(Recurso.id).offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.scalars(stmt).all())
        return items, total

    def buscar_por_user_projeto(self, user_id: int, projeto_id: int) -> Recurso | None:
        stmt = select(Recurso).where(Recurso.user_id == user_id, Recurso.projeto_id == projeto_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def criar(self, dados: RecursoCreate) -> Recurso:
        obj = Recurso(**dados.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def atualizar(self, obj: Recurso, dados: RecursoUpdate) -> Recurso:
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def desalocar(self, obj: Recurso) -> Recurso:
        obj.alocado = False
        self.db.commit()
        self.db.refresh(obj)
        return obj
```

- [ ] **Step 5: Criar DashboardRepository**

```python
from datetime import date, timedelta

from sqlalchemy import text
from sqlalchemy.orm import Session


class DashboardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_metrics(self) -> dict:
        queries = {
            "total_projetos": "SELECT COUNT(*) FROM org.projetos WHERE ativo = true",
            "projetos_ativos": "SELECT COUNT(*) FROM org.projetos WHERE status = 'active' AND ativo = true",
            "total_tarefas": "SELECT COUNT(*) FROM org.tarefas WHERE ativo = true",
            "tarefas_concluidas": "SELECT COUNT(*) FROM org.tarefas WHERE status = 'done' AND ativo = true",
            "tarefas_em_progresso": "SELECT COUNT(*) FROM org.tarefas WHERE status = 'in-progress' AND ativo = true",
            "tarefas_a_fazer": "SELECT COUNT(*) FROM org.tarefas WHERE status = 'todo' AND ativo = true",
            "total_recursos": "SELECT COUNT(*) FROM org.recursos WHERE alocado = true",
            "progresso_geral": "SELECT COALESCE(AVG(progresso), 0) FROM org.tarefas WHERE ativo = true",
        }
        result = {}
        for key, sql in queries.items():
            result[key] = self.db.execute(text(sql)).scalar() or 0
        result["progresso_geral"] = round(result["progresso_geral"])
        return result

    def buscar_proximos_prazos(self) -> list[dict]:
        hoje = date.today()
        limite = hoje + timedelta(days=7)
        sql = """
            SELECT t.id, t.titulo, t.data_fim, t.projeto_id,
                   p.nome AS project_name, p.cor AS project_color
            FROM org.tarefas t
            JOIN org.projetos p ON t.projeto_id = p.id
            WHERE t.ativo = true AND t.status != 'done'
              AND t.data_fim BETWEEN :hoje AND :limite
            ORDER BY t.data_fim ASC
            LIMIT 5
        """
        rows = self.db.execute(text(sql), {"hoje": hoje, "limite": limite}).mappings().all()
        result = []
        for row in rows:
            dias = (row["data_fim"] - hoje).days
            result.append({
                "id": row["id"],
                "titulo": row["titulo"],
                "data_fim": row["data_fim"],
                "dias_restantes": max(dias, 0),
                "projeto_id": row["projeto_id"],
                "project_name": row["project_name"],
                "project_color": row["project_color"],
            })
        return result

    def buscar_tarefas_atrasadas(self) -> tuple[list[dict], int]:
        hoje = date.today()
        sql_lista = """
            SELECT t.id, t.titulo, t.data_fim, t.projeto_id,
                   p.nome AS project_name, p.cor AS project_color
            FROM org.tarefas t
            JOIN org.projetos p ON t.projeto_id = p.id
            WHERE t.ativo = true AND t.status != 'done'
              AND t.data_fim < :hoje
            ORDER BY t.data_fim ASC
            LIMIT 5
        """
        sql_total = """
            SELECT COUNT(*) FROM org.tarefas
            WHERE ativo = true AND status != 'done' AND data_fim < :hoje
        """
        rows = self.db.execute(text(sql_lista), {"hoje": hoje}).mappings().all()
        total = self.db.execute(text(sql_total), {"hoje": hoje}).scalar() or 0
        result = []
        for row in rows:
            dias = (hoje - row["data_fim"]).days
            result.append({
                "id": row["id"],
                "titulo": row["titulo"],
                "data_fim": row["data_fim"],
                "dias_atraso": max(dias, 1),
                "projeto_id": row["projeto_id"],
                "project_name": row["project_name"],
                "project_color": row["project_color"],
            })
        return result, total

    def buscar_progresso_projetos(self) -> list[dict]:
        sql = """
            SELECT p.id, p.nome, p.cor,
                   COUNT(t.id) AS total_tarefas,
                   COALESCE(SUM(CASE WHEN t.status = 'done' THEN 1 ELSE 0 END), 0) AS tarefas_concluidas,
                   COALESCE(AVG(t.progresso), 0) AS progresso
            FROM org.projetos p
            LEFT JOIN org.tarefas t ON t.projeto_id = p.id AND t.ativo = true
            WHERE p.ativo = true
            GROUP BY p.id, p.nome, p.cor
            ORDER BY p.nome ASC
        """
        rows = self.db.execute(text(sql)).mappings().all()
        return [
            {
                "id": r["id"],
                "nome": r["nome"],
                "cor": r["cor"],
                "total_tarefas": r["total_tarefas"],
                "tarefas_concluidas": r["tarefas_concluidas"],
                "progresso": round(r["progresso"]),
            }
            for r in rows
        ]

    def buscar_carga_trabalho(self) -> list[dict]:
        sql = """
            SELECT r.id, r.user_id AS nome, r.cor,
                   COALESCE(SUM(CASE WHEN t.status != 'done' THEN 1 ELSE 0 END), 0) AS tarefas_ativas,
                   COALESCE(SUM(CASE WHEN t.status = 'done' THEN 1 ELSE 0 END), 0) AS tarefas_concluidas
            FROM org.recursos r
            LEFT JOIN org.tarefas t ON t.responsavel_id = r.id AND t.ativo = true
            WHERE r.alocado = true
            GROUP BY r.id, r.user_id, r.cor
            ORDER BY r.id ASC
        """
        rows = self.db.execute(text(sql)).mappings().all()
        return [
            {
                "id": r["id"],
                "nome": r["nome"],
                "cor": r["cor"],
                "tarefas_ativas": r["tarefas_ativas"],
                "tarefas_concluidas": r["tarefas_concluidas"],
            }
            for r in rows
        ]
```

- [ ] **Step 6: Criar CronogramaRepository**

```python
from sqlalchemy import text
from sqlalchemy.orm import Session


class CronogramaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar_tarefas_gantt(
        self, page: int = 1, page_size: int = 100, projeto_id: int | None = None,
    ) -> tuple[list[dict], int]:
        base_from = """
            FROM org.tarefas t
            LEFT JOIN org.projetos p ON t.projeto_id = p.id
            LEFT JOIN org.recursos r ON t.responsavel_id = r.id
            LEFT JOIN iam.usuarios u ON r.user_id = u.id
        """
        where_clause = "WHERE t.ativo = 1"
        params: dict = {}
        if projeto_id is not None:
            where_clause += " AND t.projeto_id = :projeto_id"
            params["projeto_id"] = projeto_id

        count_sql = text(f"SELECT COUNT(*) {base_from} {where_clause}")
        total = self.db.scalar(count_sql, params) or 0

        offset = (page - 1) * page_size
        data_sql = text(f"""
            SELECT t.id, t.titulo, t.status, t.prioridade,
                   t.data_inicio, t.data_fim, t.progresso,
                   t.projeto_id, p.nome AS project_name, p.cor AS project_color,
                   t.responsavel_id, u.nome_completo AS assignee_name, r.cor AS assignee_color
            {base_from}
            {where_clause}
            ORDER BY t.data_inicio, t.id
            LIMIT :limit OFFSET :offset
        """)
        params["limit"] = page_size
        params["offset"] = offset
        rows = self.db.execute(data_sql, params).mappings().all()
        items = [dict(row) for row in rows]
        return items, total
```

---

### Task 5: Services — Lógica de Negócio

**Files:**
- Create: `app/modules/gestao_projetos/services/projeto_service.py`
- Create: `app/modules/gestao_projetos/services/tarefa_service.py`
- Create: `app/modules/gestao_projetos/services/registro_service.py`
- Create: `app/modules/gestao_projetos/services/recurso_service.py`
- Create: `app/modules/gestao_projetos/services/dashboard_service.py`
- Create: `app/modules/gestao_projetos/services/cronograma_service.py`

- [ ] **Step 1: Criar ProjetoService**

```python
import math

import structlog
from shared.exceptions.base import ConflictError, NotFoundError
from shared.schemas.base import PaginatedResponse

from app.modules.gestao_projetos.repositories.projeto_repository import ProjetoRepository
from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate, ProjetoUpdate

logger = structlog.get_logger(__name__)


class ProjetoService:
    def __init__(self, repository: ProjetoRepository) -> None:
        self.repository = repository

    def buscar(self, id: int):
        obj = self.repository.buscar_por_id(id)
        if not obj:
            raise NotFoundError(resource="Projeto", identifier=id)
        return obj

    def listar(self, page: int = 1, page_size: int = 20) -> PaginatedResponse:
        items, total = self.repository.listar_todos(page, page_size)
        return PaginatedResponse(
            items=items, total=total, page=page, page_size=page_size,
            total_pages=math.ceil(total / page_size) if total else 0,
        )

    def criar(self, dados: ProjetoCreate):
        existente = self.repository.buscar_por_nome(dados.nome)
        if existente:
            raise ConflictError(f"Projeto '{dados.nome}' ja existe")
        obj = self.repository.criar(dados)
        logger.info("Projeto criado", id=obj.id, nome=obj.nome)
        return obj

    def atualizar(self, id: int, dados: ProjetoUpdate):
        obj = self.buscar(id)
        return self.repository.atualizar(obj, dados)

    def desativar(self, id: int):
        obj = self.buscar(id)
        return self.repository.desativar(obj)
```

- [ ] **Step 2: Criar TarefaService**

```python
import math

import structlog
from shared.exceptions.base import NotFoundError
from shared.schemas.base import PaginatedResponse

from app.modules.gestao_projetos.repositories.tarefa_repository import TarefaRepository
from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate, TarefaUpdate

logger = structlog.get_logger(__name__)


class TarefaService:
    def __init__(self, repository: TarefaRepository) -> None:
        self.repository = repository

    def buscar(self, id: int):
        obj = self.repository.buscar_por_id(id)
        if not obj:
            raise NotFoundError(resource="Tarefa", identifier=id)
        return obj

    def listar(
        self, page: int = 1, page_size: int = 20,
        projeto_id: int | None = None, status: str | None = None,
    ) -> PaginatedResponse:
        items, total = self.repository.listar_todos(page, page_size, projeto_id, status)
        return PaginatedResponse(
            items=items, total=total, page=page, page_size=page_size,
            total_pages=math.ceil(total / page_size) if total else 0,
        )

    def criar(self, dados: TarefaCreate):
        obj = self.repository.criar(dados)
        logger.info("Tarefa criada", id=obj.id, titulo=obj.titulo)
        return obj

    def atualizar(self, id: int, dados: TarefaUpdate):
        obj = self.buscar(id)
        return self.repository.atualizar(obj, dados)

    def desativar(self, id: int):
        obj = self.buscar(id)
        return self.repository.desativar(obj)
```

- [ ] **Step 3: Criar RegistroService**

```python
import math

import structlog
from shared.exceptions.base import NotFoundError
from shared.schemas.base import PaginatedResponse

from app.modules.gestao_projetos.repositories.registro_repository import RegistroRepository
from app.modules.gestao_projetos.schemas.registro_tarefa import RegistroCreate, RegistroUpdate

logger = structlog.get_logger(__name__)


class RegistroService:
    def __init__(self, repository: RegistroRepository) -> None:
        self.repository = repository

    def buscar(self, id: int):
        obj = self.repository.buscar_por_id(id)
        if not obj:
            raise NotFoundError(resource="Registro", identifier=id)
        return obj

    def listar_por_tarefa(
        self, tarefa_id: int, page: int = 1, page_size: int = 50, tipo: str | None = None,
    ) -> PaginatedResponse:
        items, total = self.repository.listar_por_tarefa(tarefa_id, page, page_size, tipo)
        return PaginatedResponse(
            items=items, total=total, page=page, page_size=page_size,
            total_pages=math.ceil(total / page_size) if total else 0,
        )

    def criar(self, tarefa_id: int, dados: RegistroCreate):
        obj = self.repository.criar(tarefa_id, dados)
        logger.info("Registro criado", id=obj.id, tarefa_id=tarefa_id, tipo=obj.tipo)
        return obj

    def atualizar(self, id: int, dados: RegistroUpdate):
        obj = self.buscar(id)
        return self.repository.atualizar(obj, dados)

    def desativar(self, id: int):
        obj = self.buscar(id)
        return self.repository.desativar(obj)
```

- [ ] **Step 4: Criar RecursoService**

```python
import math

import structlog
from shared.exceptions.base import ConflictError, NotFoundError
from shared.schemas.base import PaginatedResponse

from app.modules.gestao_projetos.repositories.recurso_repository import RecursoRepository
from app.modules.gestao_projetos.schemas.recurso import RecursoCreate, RecursoUpdate

logger = structlog.get_logger(__name__)


class RecursoService:
    def __init__(self, repository: RecursoRepository) -> None:
        self.repository = repository

    def buscar(self, id: int):
        obj = self.repository.buscar_por_id(id)
        if not obj:
            raise NotFoundError(resource="Recurso", identifier=id)
        return obj

    def listar(self, page: int = 1, page_size: int = 20, projeto_id: int | None = None) -> PaginatedResponse:
        items, total = self.repository.listar_todos(page, page_size, projeto_id)
        return PaginatedResponse(
            items=items, total=total, page=page, page_size=page_size,
            total_pages=math.ceil(total / page_size) if total else 0,
        )

    def criar(self, dados: RecursoCreate):
        existente = self.repository.buscar_por_user_projeto(dados.user_id, dados.projeto_id)
        if existente:
            raise ConflictError(f"Recurso ja alocado neste projeto")
        obj = self.repository.criar(dados)
        logger.info("Recurso criado", id=obj.id, user_id=obj.user_id)
        return obj

    def atualizar(self, id: int, dados: RecursoUpdate):
        obj = self.buscar(id)
        return self.repository.atualizar(obj, dados)

    def desalocar(self, id: int):
        obj = self.buscar(id)
        return self.repository.desalocar(obj)
```

- [ ] **Step 5: Criar DashboardService**

```python
from app.modules.gestao_projetos.repositories.dashboard_repository import DashboardRepository
from app.modules.gestao_projetos.schemas.dashboard import (
    CargaTrabalho,
    DashboardMetrics,
    DashboardResponse,
    ProximoPrazo,
    ProgressoProjeto,
    TarefaAtrasada,
)


class DashboardService:
    def __init__(self, repository: DashboardRepository) -> None:
        self.repository = repository

    def carregar_dados(self) -> DashboardResponse:
        metrics_data = self.repository.buscar_metrics()
        metrics = DashboardMetrics(**metrics_data)

        proximos_prazos = [ProximoPrazo(**p) for p in self.repository.buscar_proximos_prazos()]
        tarefas_atrasadas_data, total_atrasadas = self.repository.buscar_tarefas_atrasadas()
        tarefas_atrasadas = [TarefaAtrasada(**t) for t in tarefas_atrasadas_data]
        progresso_projetos = [ProgressoProjeto(**p) for p in self.repository.buscar_progresso_projetos()]
        carga_trabalho = [CargaTrabalho(**c) for c in self.repository.buscar_carga_trabalho()]

        return DashboardResponse(
            metrics=metrics,
            proximos_prazos=proximos_prazos,
            tarefas_atrasadas=tarefas_atrasadas,
            total_tarefas_atrasadas=total_atrasadas,
            progresso_projetos=progresso_projetos,
            carga_trabalho=carga_trabalho,
        )
```

- [ ] **Step 6: Criar CronogramaService**

```python
import math

from shared.schemas.base import PaginatedResponse

from app.modules.gestao_projetos.repositories.cronograma_repository import CronogramaRepository
from app.modules.gestao_projetos.schemas.cronograma import TarefaGanttResponse


class CronogramaService:
    def __init__(self, repository: CronogramaRepository) -> None:
        self.repository = repository

    def listar_tarefas_gantt(
        self, page: int = 1, page_size: int = 100, projeto_id: int | None = None,
    ) -> PaginatedResponse:
        items, total = self.repository.listar_tarefas_gantt(page, page_size, projeto_id)
        gantt_items = [TarefaGanttResponse(**item) for item in items]
        return PaginatedResponse(
            items=gantt_items, total=total, page=page, page_size=page_size,
            total_pages=math.ceil(total / page_size) if total else 0,
        )
```

---

### Task 6: Routers — Todas as Rotas

**Files:**
- Create: `app/modules/gestao_projetos/routers/projeto_router.py`
- Create: `app/modules/gestao_projetos/routers/tarefa_router.py`
- Create: `app/modules/gestao_projetos/routers/recurso_router.py`
- Create: `app/modules/gestao_projetos/routers/dashboard_router.py`
- Create: `app/modules/gestao_projetos/routers/cronograma_router.py`

- [ ] **Step 1: Criar ProjetoRouter**

```python
from fastapi import APIRouter, Depends, Query
from shared.schemas.base import ErrorResponse, MessageResponse, PaginatedResponse
from shared.security.permissions import Role

from app.auth.dependencies import get_gestao_projetos_service, require_role
from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate, ProjetoResponse, ProjetoUpdate
from app.modules.gestao_projetos.services.projeto_service import ProjetoService

router = APIRouter(prefix="/v1/projetos", tags=["Projetos"])


@router.get(
    "",
    response_model=PaginatedResponse[ProjetoResponse],
    summary="Listar",
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR, Role.LEITURA))],
)
def listar(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ProjetoService = Depends(get_gestao_projetos_service),
):
    return service.listar(page, page_size)


@router.get(
    "/{id}",
    response_model=ProjetoResponse,
    summary="Buscar por ID",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR, Role.LEITURA))],
)
def buscar(id: int, service: ProjetoService = Depends(get_gestao_projetos_service)):
    return service.buscar(id)


@router.post(
    "",
    response_model=ProjetoResponse,
    status_code=201,
    summary="Criar",
    responses={409: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def criar(dados: ProjetoCreate, service: ProjetoService = Depends(get_gestao_projetos_service)):
    return service.criar(dados)


@router.put(
    "/{id}",
    response_model=ProjetoResponse,
    summary="Atualizar",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def atualizar(id: int, dados: ProjetoUpdate, service: ProjetoService = Depends(get_gestao_projetos_service)):
    return service.atualizar(id, dados)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Desativar",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN))],
)
def desativar(id: int, service: ProjetoService = Depends(get_gestao_projetos_service)):
    service.desativar(id)
    return MessageResponse(message=f"Projeto {id} desativado com sucesso.")
```

- [ ] **Step 2: Criar TarefaRouter**

```python
from fastapi import APIRouter, Depends, Query
from shared.schemas.base import ErrorResponse, MessageResponse, PaginatedResponse
from shared.security.permissions import Role

from app.auth.dependencies import get_gestao_projetos_tarefa_service, get_gestao_projetos_registro_service, require_role
from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate, TarefaResponse, TarefaUpdate
from app.modules.gestao_projetos.schemas.registro_tarefa import RegistroCreate, RegistroResponse, RegistroUpdate
from app.modules.gestao_projetos.services.tarefa_service import TarefaService
from app.modules.gestao_projetos.services.registro_service import RegistroService

router = APIRouter(prefix="/v1/tarefas", tags=["Tarefas"])


@router.get(
    "",
    response_model=PaginatedResponse[TarefaResponse],
    summary="Listar",
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR, Role.LEITURA))],
)
def listar(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    projeto_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    service: TarefaService = Depends(get_gestao_projetos_tarefa_service),
):
    return service.listar(page, page_size, projeto_id, status)


@router.get(
    "/{id}",
    response_model=TarefaResponse,
    summary="Buscar por ID",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR, Role.LEITURA))],
)
def buscar(id: int, service: TarefaService = Depends(get_gestao_projetos_tarefa_service)):
    return service.buscar(id)


@router.post(
    "",
    response_model=TarefaResponse,
    status_code=201,
    summary="Criar",
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def criar(dados: TarefaCreate, service: TarefaService = Depends(get_gestao_projetos_tarefa_service)):
    return service.criar(dados)


@router.put(
    "/{id}",
    response_model=TarefaResponse,
    summary="Atualizar",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def atualizar(id: int, dados: TarefaUpdate, service: TarefaService = Depends(get_gestao_projetos_tarefa_service)):
    return service.atualizar(id, dados)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Desativar",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN))],
)
def desativar(id: int, service: TarefaService = Depends(get_gestao_projetos_tarefa_service)):
    service.desativar(id)
    return MessageResponse(message=f"Tarefa {id} desativada com sucesso.")


@router.get(
    "/{tarefa_id}/registros",
    response_model=PaginatedResponse[RegistroResponse],
    summary="Listar registros",
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR, Role.LEITURA))],
)
def listar_registros(
    tarefa_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    tipo: str | None = Query(default=None),
    service: RegistroService = Depends(get_gestao_projetos_registro_service),
):
    return service.listar_por_tarefa(tarefa_id, page, page_size, tipo)


@router.post(
    "/{tarefa_id}/registros",
    response_model=RegistroResponse,
    status_code=201,
    summary="Criar registro",
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def criar_registro(
    tarefa_id: int,
    dados: RegistroCreate,
    service: RegistroService = Depends(get_gestao_projetos_registro_service),
):
    return service.criar(tarefa_id, dados)


@router.put(
    "/registros/{registro_id}",
    response_model=RegistroResponse,
    summary="Atualizar registro",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def atualizar_registro(
    registro_id: int,
    dados: RegistroUpdate,
    service: RegistroService = Depends(get_gestao_projetos_registro_service),
):
    return service.atualizar(registro_id, dados)


@router.delete(
    "/registros/{registro_id}",
    response_model=MessageResponse,
    summary="Desativar registro",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN))],
)
def desativar_registro(
    registro_id: int,
    service: RegistroService = Depends(get_gestao_projetos_registro_service),
):
    service.desativar(registro_id)
    return MessageResponse(message=f"Registro {registro_id} desativado com sucesso.")
```

- [ ] **Step 3: Criar RecursoRouter**

```python
from fastapi import APIRouter, Depends, Query
from shared.schemas.base import ErrorResponse, MessageResponse, PaginatedResponse
from shared.security.permissions import Role

from app.auth.dependencies import get_gestao_projetos_recurso_service, require_role
from app.modules.gestao_projetos.schemas.recurso import RecursoCreate, RecursoResponse, RecursoUpdate
from app.modules.gestao_projetos.services.recurso_service import RecursoService

router = APIRouter(prefix="/v1/recursos", tags=["Recursos"])


@router.get(
    "",
    response_model=PaginatedResponse[RecursoResponse],
    summary="Listar",
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR, Role.LEITURA))],
)
def listar(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    projeto_id: int | None = Query(default=None),
    service: RecursoService = Depends(get_gestao_projetos_recurso_service),
):
    return service.listar(page, page_size, projeto_id)


@router.get(
    "/{id}",
    response_model=RecursoResponse,
    summary="Buscar por ID",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR, Role.LEITURA))],
)
def buscar(id: int, service: RecursoService = Depends(get_gestao_projetos_recurso_service)):
    return service.buscar(id)


@router.post(
    "",
    response_model=RecursoResponse,
    status_code=201,
    summary="Alocar recurso",
    responses={409: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def criar(dados: RecursoCreate, service: RecursoService = Depends(get_gestao_projetos_recurso_service)):
    return service.criar(dados)


@router.put(
    "/{id}",
    response_model=RecursoResponse,
    summary="Atualizar",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN, Role.OPERADOR))],
)
def atualizar(id: int, dados: RecursoUpdate, service: RecursoService = Depends(get_gestao_projetos_recurso_service)):
    return service.atualizar(id, dados)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Desalocar",
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(require_role(Role.ADMIN))],
)
def desalocar(id: int, service: RecursoService = Depends(get_gestao_projetos_recurso_service)):
    service.desalocar(id)
    return MessageResponse(message=f"Recurso {id} desalocado com sucesso.")
```

- [ ] **Step 4: Criar DashboardRouter**

```python
from fastapi import APIRouter, Depends

from app.auth.dependencies import get_gestao_projetos_dashboard_service
from app.modules.gestao_projetos.schemas.dashboard import DashboardResponse
from app.modules.gestao_projetos.services.dashboard_service import DashboardService

router = APIRouter(prefix="/v1/dashboard", tags=["Dashboard"])


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Dados completos do dashboard",
)
def carregar(service: DashboardService = Depends(get_gestao_projetos_dashboard_service)):
    return service.carregar_dados()
```

- [ ] **Step 5: Criar CronogramaRouter**

```python
from fastapi import APIRouter, Depends, Query
from shared.schemas.base import PaginatedResponse

from app.auth.dependencies import get_gestao_projetos_cronograma_service
from app.modules.gestao_projetos.schemas.cronograma import TarefaGanttResponse
from app.modules.gestao_projetos.services.cronograma_service import CronogramaService

router = APIRouter(prefix="/v1/cronograma", tags=["Cronograma"])


@router.get(
    "/tarefas",
    response_model=PaginatedResponse[TarefaGanttResponse],
    summary="Listar tarefas para Gantt",
)
def listar_tarefas(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    projeto_id: int | None = Query(default=None),
    service: CronogramaService = Depends(get_gestao_projetos_cronograma_service),
):
    return service.listar_tarefas_gantt(page, page_size, projeto_id)
```

---

### Task 7: Tests — conftest + Unit + Integration

**Files:**
- Create: `app/modules/gestao_projetos/tests/conftest.py`
- Create: `app/modules/gestao_projetos/tests/test_projeto_unit.py`
- Create: `app/modules/gestao_projetos/tests/test_projeto_integration.py`
- Create: `app/modules/gestao_projetos/tests/test_tarefa_unit.py`
- Create: `app/modules/gestao_projetos/tests/test_tarefa_integration.py`
- Create: `app/modules/gestao_projetos/tests/test_recurso_unit.py`
- Create: `app/modules/gestao_projetos/tests/test_recurso_integration.py`
- Create: `app/modules/gestao_projetos/tests/test_dashboard_integration.py`
- Create: `app/modules/gestao_projetos/tests/test_cronograma_integration.py`

- [ ] **Step 1: Criar conftest.py**

```python
import importlib.util
import os
import sys
from pathlib import Path

import pytest
from sqlalchemy import Column, Integer, String, Table, create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

GRINDX_PACKAGES = os.environ.get(
    "GRINDX_PACKAGES",
    str(Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent.parent / "GrindX" / "packages"),
)
GRINDX_API = str(Path(GRINDX_PACKAGES).parent / "apps" / "api-postgres")
LOCAL_MODULES = str(Path(__file__).resolve().parent.parent.parent)

for p in [GRINDX_PACKAGES, GRINDX_API, LOCAL_MODULES]:
    if p not in sys.path:
        sys.path.insert(0, p)

import app  # noqa: E402
import app.modules  # noqa: E402

_local_pkg = Path(LOCAL_MODULES) / "gestao_projetos"
_spec = importlib.util.spec_from_file_location(
    "app.modules.gestao_projetos",
    str(_local_pkg / "__init__.py"),
    submodule_search_locations=[str(_local_pkg)],
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["app.modules.gestao_projetos"] = _mod
_spec.loader.exec_module(_mod)

from app.modules.iam.base import IamBase  # noqa: E402

Table(
    "usuarios",
    IamBase.metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(200)),
    Column("nome_completo", String(200)),
    schema="iam",
)

from app.modules.gestao_projetos.models.projeto import Projeto  # noqa: E402, F401
from app.modules.gestao_projetos.models.tarefa import Tarefa  # noqa: E402, F401
from app.modules.gestao_projetos.models.registro_tarefa import RegistroTarefa  # noqa: E402, F401
from app.modules.gestao_projetos.models.recurso import Recurso  # noqa: E402, F401

_SCHEMA_TRANSLATE = {"iam": None, "portal": None, "catalogo": None, "org": None}
_all_metadata = IamBase.metadata


@pytest.fixture(scope="function")
def db_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    with engine.execution_options(schema_translate_map=_SCHEMA_TRANSLATE).connect() as conn:
        _all_metadata.create_all(conn)

    TestingSession = sessionmaker(
        bind=engine.execution_options(schema_translate_map=_SCHEMA_TRANSLATE),
        autocommit=False,
        autoflush=False,
    )
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        with engine.execution_options(schema_translate_map=_SCHEMA_TRANSLATE).connect() as conn:
            _all_metadata.drop_all(conn)


@pytest.fixture
def projeto_repository(db_session: Session):
    from app.modules.gestao_projetos.repositories.projeto_repository import ProjetoRepository
    return ProjetoRepository(db_session)


@pytest.fixture
def tarefa_repository(db_session: Session):
    from app.modules.gestao_projetos.repositories.tarefa_repository import TarefaRepository
    return TarefaRepository(db_session)


@pytest.fixture
def registro_repository(db_session: Session):
    from app.modules.gestao_projetos.repositories.registro_repository import RegistroRepository
    return RegistroRepository(db_session)


@pytest.fixture
def recurso_repository(db_session: Session):
    from app.modules.gestao_projetos.repositories.recurso_repository import RecursoRepository
    return RecursoRepository(db_session)


@pytest.fixture
def projeto_service(projeto_repository):
    from app.modules.gestao_projetos.services.projeto_service import ProjetoService
    return ProjetoService(projeto_repository)


@pytest.fixture
def tarefa_service(tarefa_repository):
    from app.modules.gestao_projetos.services.tarefa_service import TarefaService
    return TarefaService(tarefa_repository)


@pytest.fixture
def registro_service(registro_repository):
    from app.modules.gestao_projetos.services.registro_service import RegistroService
    return RegistroService(registro_repository)


@pytest.fixture
def recurso_service(recurso_repository):
    from app.modules.gestao_projetos.services.recurso_service import RecursoService
    return RecursoService(recurso_repository)
```

- [ ] **Step 2: Criar test_projeto_unit.py**

```python
from unittest.mock import MagicMock

import pytest
from shared.exceptions.base import NotFoundError


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.buscar_por_nome.return_value = []
    return repo


@pytest.fixture
def service(mock_repository):
    from app.modules.gestao_projetos.services.projeto_service import ProjetoService
    return ProjetoService(mock_repository)


class TestBuscar:
    def test_quando_encontrado_retorna_objeto(self, service, mock_repository):
        mock_repository.buscar_por_id.return_value = MagicMock(id=1)
        result = service.buscar(1)
        assert result.id == 1
        mock_repository.buscar_por_id.assert_called_once_with(1)

    def test_quando_nao_encontrado_lanca_not_found(self, service, mock_repository):
        mock_repository.buscar_por_id.return_value = None
        with pytest.raises(NotFoundError):
            service.buscar(999)


class TestCriar:
    def test_cria_com_sucesso(self, service, mock_repository):
        mock_repository.criar.return_value = MagicMock(id=1)
        from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate
        dados = ProjetoCreate(nome="Projeto Teste", data_inicio="2026-01-01", data_fim="2026-03-31")
        result = service.criar(dados)
        assert result.id == 1
        mock_repository.criar.assert_called_once_with(dados)

    def test_cria_com_nome_duplicado_lanca_conflict(self, service, mock_repository):
        mock_repository.buscar_por_nome.return_value = [MagicMock()]
        from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate
        dados = ProjetoCreate(nome="Duplicado", data_inicio="2026-01-01", data_fim="2026-03-31")
        with pytest.raises(Exception):
            service.criar(dados)


class TestAtualizar:
    def test_atualiza_campos_fornecidos(self, service, mock_repository):
        from app.modules.gestao_projetos.schemas.projeto import ProjetoUpdate
        obj = MagicMock(id=1)
        mock_repository.buscar_por_id.return_value = obj
        dados = ProjetoUpdate(nome="Novo Nome")
        service.atualizar(1, dados)
        mock_repository.atualizar.assert_called_once_with(obj, dados)


class TestDesativar:
    def test_desativa_projeto_existente(self, service, mock_repository):
        obj = MagicMock(id=1)
        mock_repository.buscar_por_id.return_value = obj
        service.desativar(1)
        mock_repository.desativar.assert_called_once_with(obj)
```

- [ ] **Step 3: Criar test_projeto_integration.py**

```python
import pytest
from shared.exceptions.base import NotFoundError


class TestRepository:
    def test_criar_e_buscar_por_id(self, repository):
        from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate
        obj = repository.criar(ProjetoCreate(nome="Teste", data_inicio="2026-01-01", data_fim="2026-03-31"))
        assert obj.id is not None
        assert obj.nome == "Teste"
        assert obj.status == "planning"
        assert repository.buscar_por_id(obj.id) is not None

    def test_listar_com_paginacao(self, repository):
        from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate
        for i in range(5):
            repository.criar(ProjetoCreate(nome=f"Item {i}", data_inicio="2026-01-01", data_fim="2026-03-31"))
        items, total = repository.listar_todos(page=1, page_size=2)
        assert total == 5
        assert len(items) == 2

    def test_atualizar(self, repository):
        from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate, ProjetoUpdate
        obj = repository.criar(ProjetoCreate(nome="Original", data_inicio="2026-01-01", data_fim="2026-03-31"))
        dados = ProjetoUpdate(nome="Alterado")
        atualizado = repository.atualizar(obj, dados)
        assert atualizado.nome == "Alterado"

    def test_desativar(self, repository):
        from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate
        obj = repository.criar(ProjetoCreate(nome="Teste", data_inicio="2026-01-01", data_fim="2026-03-31"))
        assert obj.ativo is True
        desativado = repository.desativar(obj)
        assert desativado.ativo is False


class TestService:
    def test_buscar_inexistente_lanca_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.buscar(9999)

    def test_listar_retorna_todos(self, service, repository):
        from app.modules.gestao_projetos.schemas.projeto import ProjetoCreate
        for i in range(3):
            repository.criar(ProjetoCreate(nome=f"Item {i}", data_inicio="2026-01-01", data_fim="2026-03-31"))
        result = service.listar()
        assert result.total == 3
```

- [ ] **Step 4: Criar test_tarefa_unit.py**

```python
from unittest.mock import MagicMock

import pytest
from shared.exceptions.base import NotFoundError


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    from app.modules.gestao_projetos.services.tarefa_service import TarefaService
    return TarefaService(mock_repository)


class TestBuscar:
    def test_quando_encontrado_retorna_objeto(self, service, mock_repository):
        mock_repository.buscar_por_id.return_value = MagicMock(id=1)
        result = service.buscar(1)
        assert result.id == 1

    def test_quando_nao_encontrado_lanca_not_found(self, service, mock_repository):
        mock_repository.buscar_por_id.return_value = None
        with pytest.raises(NotFoundError):
            service.buscar(999)


class TestCriar:
    def test_cria_com_sucesso(self, service, mock_repository):
        mock_repository.criar.return_value = MagicMock(id=1)
        from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate
        dados = TarefaCreate(titulo="Tarefa Teste", data_inicio="2026-01-01", data_fim="2026-01-15")
        result = service.criar(dados)
        assert result.id == 1
```

- [ ] **Step 5: Criar test_tarefa_integration.py**

```python
import pytest
from shared.exceptions.base import NotFoundError


class TestRepository:
    def test_criar_e_buscar_por_id(self, tarefa_repository):
        from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate
        obj = tarefa_repository.criar(TarefaCreate(titulo="Tarefa Teste", data_inicio="2026-01-01", data_fim="2026-01-15"))
        assert obj.id is not None
        assert obj.titulo == "Tarefa Teste"
        assert obj.status == "todo"

    def test_listar_com_filtro_status(self, tarefa_repository):
        from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate
        tarefa_repository.criar(TarefaCreate(titulo="T1", data_inicio="2026-01-01", data_fim="2026-01-15", status="todo"))
        tarefa_repository.criar(TarefaCreate(titulo="T2", data_inicio="2026-01-01", data_fim="2026-01-15", status="done"))
        items, total = tarefa_repository.listar_todos(page=1, page_size=10, status="todo")
        assert total == 1
        assert items[0].titulo == "T1"


class TestService:
    def test_buscar_inexistente_lanca_not_found(self, tarefa_service):
        with pytest.raises(NotFoundError):
            tarefa_service.buscar(9999)
```

- [ ] **Step 6: Criar test_recurso_unit.py**

```python
from unittest.mock import MagicMock

import pytest
from shared.exceptions.base import NotFoundError


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    from app.modules.gestao_projetos.services.recurso_service import RecursoService
    return RecursoService(mock_repository)


class TestBuscar:
    def test_quando_encontrado_retorna_objeto(self, service, mock_repository):
        mock_repository.buscar_por_id.return_value = MagicMock(id=1)
        result = service.buscar(1)
        assert result.id == 1

    def test_quando_nao_encontrado_lanca_not_found(self, service, mock_repository):
        mock_repository.buscar_por_id.return_value = None
        with pytest.raises(NotFoundError):
            service.buscar(999)


class TestCriar:
    def test_cria_com_sucesso(self, service, mock_repository):
        mock_repository.buscar_por_user_projeto.return_value = None
        mock_repository.criar.return_value = MagicMock(id=1)
        from app.modules.gestao_projetos.schemas.recurso import RecursoCreate
        dados = RecursoCreate(user_id=1, projeto_id=1)
        result = service.criar(dados)
        assert result.id == 1

    def test_cria_duplicado_lanca_conflict(self, service, mock_repository):
        mock_repository.buscar_por_user_projeto.return_value = MagicMock()
        from app.modules.gestao_projetos.schemas.recurso import RecursoCreate
        dados = RecursoCreate(user_id=1, projeto_id=1)
        with pytest.raises(Exception):
            service.criar(dados)
```

- [ ] **Step 7: Criar test_recurso_integration.py**

```python
import pytest
from shared.exceptions.base import NotFoundError, ConflictError


class TestRepository:
    def test_criar_e_buscar_por_id(self, recurso_repository):
        from app.modules.gestao_projetos.schemas.recurso import RecursoCreate
        obj = recurso_repository.criar(RecursoCreate(user_id=1, projeto_id=1))
        assert obj.id is not None
        assert recurso_repository.buscar_por_id(obj.id) is not None

    def test_listar_por_projeto(self, recurso_repository):
        from app.modules.gestao_projetos.schemas.recurso import RecursoCreate
        recurso_repository.criar(RecursoCreate(user_id=1, projeto_id=1))
        recurso_repository.criar(RecursoCreate(user_id=2, projeto_id=1))
        recurso_repository.criar(RecursoCreate(user_id=3, projeto_id=2))
        items, total = recurso_repository.listar_todos(page=1, page_size=10, projeto_id=1)
        assert total == 2

    def test_desalocar(self, recurso_repository):
        from app.modules.gestao_projetos.schemas.recurso import RecursoCreate
        obj = recurso_repository.criar(RecursoCreate(user_id=1, projeto_id=1))
        assert obj.alocado is True
        desalocado = recurso_repository.desalocar(obj)
        assert desalocado.alocado is False


class TestService:
    def test_criar_duplicado_lanca_conflict(self, recurso_service, recurso_repository):
        from app.modules.gestao_projetos.schemas.recurso import RecursoCreate
        recurso_repository.criar(RecursoCreate(user_id=1, projeto_id=1))
        with pytest.raises(ConflictError):
            recurso_service.criar(RecursoCreate(user_id=1, projeto_id=1))
```

- [ ] **Step 8: Criar test_dashboard_integration.py**

```python
class TestDashboard:
    def test_carregar_dados_retorna_metrics(self, db_session):
        from app.modules.gestao_projetos.repositories.dashboard_repository import DashboardRepository
        from app.modules.gestao_projetos.services.dashboard_service import DashboardService
        repo = DashboardRepository(db_session)
        service = DashboardService(repo)
        result = service.carregar_dados()
        assert result.metrics.total_projetos == 0
        assert result.metrics.total_tarefas == 0
        assert result.progresso_projetos == []
```

- [ ] **Step 9: Criar test_cronograma_integration.py**

```python
class TestCronograma:
    def test_listar_tarefas_gantt_vazio(self, db_session):
        from app.modules.gestao_projetos.repositories.cronograma_repository import CronogramaRepository
        from app.modules.gestao_projetos.services.cronograma_service import CronogramaService
        repo = CronogramaRepository(db_session)
        service = CronogramaService(repo)
        result = service.listar_tarefas_gantt()
        assert result.total == 0
        assert result.items == []
```

---

### Task 8: Frontend — Projeto (Aba 1)

**Files:**
- Create: `frontend/projeto/index.html`
- Create: `frontend/projeto/script.js`
- Create: `frontend/projeto/style.css`

- [ ] **Step 1: Criar index.html do Projeto**

Copiar o conteúdo de `modulo-projeto/frontend/index.html` para `modulo-gestao-projetos/frontend/projeto/index.html`.

- [ ] **Step 2: Criar script.js do Projeto**

Copiar o conteúdo de `modulo-projeto/frontend/script.js` para `modulo-gestao-projetos/frontend/projeto/script.js`.

- [ ] **Step 3: Criar style.css do Projeto**

Copiar o conteúdo de `modulo-projeto/frontend/style.css` para `modulo-gestao-projetos/frontend/projeto/style.css`.

---

### Task 9: Frontend — Tarefas (Aba 2)

**Files:**
- Create: `frontend/tarefas/index.html`
- Create: `frontend/tarefas/script.js`
- Create: `frontend/tarefas/style.css`

- [ ] **Step 1: Criar index.html das Tarefas**

Copiar o conteúdo de `modulo-tarefas/frontend/index.html` para `modulo-gestao-projetos/frontend/tarefas/index.html`.

- [ ] **Step 2: Criar script.js das Tarefas**

Copiar o conteúdo de `modulo-tarefas/frontend/script.js` para `modulo-gestao-projetos/frontend/tarefas/script.js`.

- [ ] **Step 3: Criar style.css das Tarefas**

Copiar o conteúdo de `modulo-tarefas/frontend/style.css` para `modulo-gestao-projetos/frontend/tarefas/style.css`.

---

### Task 10: Frontend — Recursos (Aba 3)

**Files:**
- Create: `frontend/recursos/index.html`
- Create: `frontend/recursos/script.js`
- Create: `frontend/recursos/style.css`

- [ ] **Step 1: Criar index.html dos Recursos**

Copiar o conteúdo de `modulo-recursos/frontend/index.html` para `modulo-gestao-projetos/frontend/recursos/index.html`.

- [ ] **Step 2: Criar script.js dos Recursos**

Copiar o conteúdo de `modulo-recursos/frontend/script.js` para `modulo-gestao-projetos/frontend/recursos/script.js`.

- [ ] **Step 3: Criar style.css dos Recursos**

Copiar o conteúdo de `modulo-recursos/frontend/style.css` para `modulo-gestao-projetos/frontend/recursos/style.css`.

---

### Task 11: Frontend — Dashboard (Aba 4)

**Files:**
- Create: `frontend/dashboard/index.html`
- Create: `frontend/dashboard/script.js`
- Create: `frontend/dashboard/style.css`

- [ ] **Step 1: Criar index.html do Dashboard**

Copiar o conteúdo de `modulo-dashboard/frontend/index.html` para `modulo-gestao-projetos/frontend/dashboard/index.html`.

- [ ] **Step 2: Criar script.js do Dashboard**

Copiar o conteúdo de `modulo-dashboard/frontend/script.js` para `modulo-gestao-projetos/frontend/dashboard/script.js`.

- [ ] **Step 3: Criar style.css do Dashboard**

Copiar o conteúdo de `modulo-dashboard/frontend/style.css` para `modulo-gestao-projetos/frontend/dashboard/style.css`.

---

### Task 12: Frontend — Cronograma (Aba 5)

**Files:**
- Create: `frontend/cronograma/index.html`
- Create: `frontend/cronograma/script.js`
- Create: `frontend/cronograma/style.css`

- [ ] **Step 1: Criar index.html do Cronograma**

Copiar o conteúdo de `modulo-cronograma/frontend/index.html` para `modulo-gestao-projetos/frontend/cronograma/index.html`.

- [ ] **Step 2: Criar script.js do Cronograma**

Copiar o conteúdo de `modulo-cronograma/frontend/script.js` para `modulo-gestao-projetos/frontend/cronograma/script.js`.

- [ ] **Step 3: Criar style.css do Cronograma**

Copiar o conteúdo de `modulo-cronograma/frontend/style.css` para `modulo-gestao-projetos/frontend/cronograma/style.css`.

---

### Task 13: Migration Alembic

**Files:**
- Create: `migration/{revision}_create_tables.py`

- [ ] **Step 1: Criar migration**

```python
"""criar tabelas gestao_projetos

Revision ID: {revision}
Revises: {down_revision}
Create Date: {date}
"""

from typing import Sequence
from alembic import op
import sqlalchemy as sa

revision: str = "{revision}"
down_revision: str | None = "{down_revision}"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "projetos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="planning", nullable=False),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_fim", sa.Date(), nullable=False),
        sa.Column("cor", sa.String(length=7), server_default="#3b82f6", nullable=False),
        sa.Column("gerente_id", sa.Integer(), nullable=True),
        sa.Column("ativo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["gerente_id"], ["iam.usuarios.id"]),
        schema="org",
    )
    op.create_index("ix_org_projetos_nome", "projetos", ["nome"], schema="org")

    op.create_table(
        "tarefas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("titulo", sa.String(length=255), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="todo", nullable=False),
        sa.Column("prioridade", sa.String(length=10), server_default="medium", nullable=False),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_fim", sa.Date(), nullable=False),
        sa.Column("progresso", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("projeto_id", sa.Integer(), nullable=True),
        sa.Column("responsavel_id", sa.Integer(), nullable=True),
        sa.Column("ativo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["projeto_id"], ["org.projetos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["responsavel_id"], ["org.recursos.id"], ondelete="SET NULL"),
        schema="org",
    )
    op.create_index("ix_org_tarefas_titulo", "tarefas", ["titulo"], schema="org")
    op.create_index("ix_org_tarefas_projeto_id", "tarefas", ["projeto_id"], schema="org")
    op.create_index("ix_org_tarefas_responsavel_id", "tarefas", ["responsavel_id"], schema="org")

    op.create_table(
        "registros_tarefas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tarefa_id", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=20), server_default="log", nullable=False),
        sa.Column("conteudo", sa.Text(), nullable=False),
        sa.Column("autor_id", sa.Integer(), nullable=True),
        sa.Column("ativo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tarefa_id"], ["org.tarefas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["autor_id"], ["org.recursos.id"], ondelete="SET NULL"),
        schema="org",
    )
    op.create_index("ix_org_registros_tarefas_tarefa_id", "registros_tarefas", ["tarefa_id"], schema="org")
    op.create_index("ix_org_registros_tarefas_autor_id", "registros_tarefas", ["autor_id"], schema="org")

    op.create_table(
        "recursos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("projeto_id", sa.Integer(), nullable=False),
        sa.Column("cargo_contexto", sa.String(length=100), nullable=True),
        sa.Column("cor", sa.String(length=7), server_default="#3b82f6", nullable=False),
        sa.Column("alocado", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["iam.usuarios.id"]),
        sa.UniqueConstraint("user_id", "projeto_id", name="uq_recurso_user_projeto"),
        schema="org",
    )


def downgrade() -> None:
    op.drop_table("recursos", schema="org")
    op.drop_table("registros_tarefas", schema="org")
    op.drop_table("tarefas", schema="org")
    op.drop_table("projetos", schema="org")
```

---

### Task 14: Support Files — module.json, export.py, Makefile, etc.

**Files:**
- Create: `module.json`
- Create: `app/modules/gestao_projetos/export.py`
- Create: `Makefile`
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `run_tests.ps1`

- [ ] **Step 1: Criar module.json**

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

- [ ] **Step 2: Criar export.py**

Copiar a estrutura de `modulo-projeto/app/modules/projeto/export.py` adaptando para `gestao_projetos` com múltiplos frontends.

- [ ] **Step 3: Criar Makefile**

Copiar a estrutura de `modulo-projeto/Makefile` adaptando `MODULE := gestao_projetos` e `ENTITY := GestaoProjetos`.

- [ ] **Step 4: Criar requirements.txt**

```
pytest>=8.0
sqlalchemy>=2.0
pydantic>=2.0
structlog>=24.0
fastapi>=0.110
```

- [ ] **Step 5: Criar pytest.ini**

```ini
[pytest]
testpaths = app/modules/gestao_projetos/tests
```

- [ ] **Step 6: Criar run_tests.ps1**

```powershell
param(
    [string]$GrindxPackages = "D:\\_Projetos\\GrindX\\packages",
    [switch]$Verbose
)
$env:GRINDX_PACKAGES = $GrindxPackages
$pytestArgs = @("-v")
if ($Verbose) { $pytestArgs += "--tb=long" } else { $pytestArgs += "--tb=short" }
python -m pytest "app/modules/gestao_projetos/tests/" @pytestArgs
```

---

### Task 15: Rodar Testes e Verificar

- [ ] **Step 1: Rodar todos os testes**

Run: `cd D:\_Projetos\Project_Management\modulo-gestao-projetos && $env:GRINDX_PACKAGES = "D:\_Projetos\GrindX\packages"; python -m pytest app/modules/gestao_projetos/tests/ -v`
Expected: Todos os testes PASS

- [ ] **Step 2: Verificar cobertura de testes**

Run: `python -m pytest app/modules/gestao_projetos/tests/ -v --tb=short | Select-String "PASSED|FAILED"`
Expected: Lista de testes passando, nenhum falhando

- [ ] **Step 3: Gerar pacote .zip**

Run: `python -m app.modules.gestao_projetos.export package`
Expected: Zip gerado em `dist/modulo-gestao_projetos.zip`

- [ ] **Step 4: Verificar estrutura do zip**

Run: `python -c "import zipfile; [print(f) for f in zipfile.ZipFile('dist/modulo-gestao_projetos.zip').namelist()[:20]]"`
Expected: Estrutura com `module.json`, `app/modules/gestao_projetos/`, `frontend/`, `migration/`

---

## Registration Checklist

- [ ] Estrutura de diretórios criada
- [ ] `base.py` com `GestaoProjetosBase`
- [ ] Models: Projeto, Tarefa, RegistroTarefa, Recurso
- [ ] Schemas: todos os Create/Update/Response + Dashboard + Cronograma
- [ ] Repositories: CRUD + queries customizadas (dashboard, cronograma)
- [ ] Services: lógica de negócio + validações
- [ ] Routers: todas as rotas documentadas
- [ ] `__init__.py` para cada camada
- [ ] `conftest.py` com fixtures SQLite
- [ ] Testes unitários (repo mockado)
- [ ] Testes de integração (SQLite real)
- [ ] Frontend: Dashboard, Projetos, Tarefas, Recursos, Cronograma
- [ ] Migration Alembic
- [ ] `module.json`
- [ ] `export.py`
- [ ] `Makefile`, `requirements.txt`, `pytest.ini`, `run_tests.ps1`
- [ ] Todos os testes passando
- [ ] Gerar `.zip` com `make package`

"""
Standalone dependencies for local testing.
Provides dependency injection without modifying GrindX core.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.gestao_projetos.repositories.projeto_repository import ProjetoRepository
from app.modules.gestao_projetos.repositories.tarefa_repository import TarefaRepository
from app.modules.gestao_projetos.repositories.registro_repository import RegistroRepository
from app.modules.gestao_projetos.repositories.recurso_repository import RecursoRepository
from app.modules.gestao_projetos.repositories.dashboard_repository import DashboardRepository
from app.modules.gestao_projetos.repositories.cronograma_repository import CronogramaRepository
from app.modules.gestao_projetos.services.projeto_service import ProjetoService
from app.modules.gestao_projetos.services.tarefa_service import TarefaService
from app.modules.gestao_projetos.services.registro_service import RegistroService
from app.modules.gestao_projetos.services.recurso_service import RecursoService
from app.modules.gestao_projetos.services.dashboard_service import DashboardService
from app.modules.gestao_projetos.services.cronograma_service import CronogramaService


def get_gestao_projetos_service(db: Session = Depends(get_db)) -> ProjetoService:
    repository = ProjetoRepository(db)
    return ProjetoService(repository)


def get_gestao_projetos_tarefa_service(db: Session = Depends(get_db)) -> TarefaService:
    repository = TarefaRepository(db)
    return TarefaService(repository)


def get_gestao_projetos_registro_service(db: Session = Depends(get_db)) -> RegistroService:
    repository = RegistroRepository(db)
    return RegistroService(repository)


def get_gestao_projetos_recurso_service(db: Session = Depends(get_db)) -> RecursoService:
    repository = RecursoRepository(db)
    return RecursoService(repository)


def get_gestao_projetos_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    repository = DashboardRepository(db)
    return DashboardService(repository)


def get_gestao_projetos_cronograma_service(db: Session = Depends(get_db)) -> CronogramaService:
    repository = CronogramaRepository(db)
    return CronogramaService(repository)


class require_role:
    """Dummy require_role for standalone mode."""
    def __init__(self, *roles):
        self.roles = roles

    def __call__(self):
        pass

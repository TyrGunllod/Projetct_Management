from fastapi import APIRouter, Depends, Query
from shared.schemas.base import PaginatedResponse

from app.database import get_db
from app.modules.gestao_projetos.schemas.cronograma import TarefaGanttResponse
from app.modules.gestao_projetos.repositories.cronograma_repository import CronogramaRepository
from app.modules.gestao_projetos.services.cronograma_service import CronogramaService

router = APIRouter(prefix="/v1/cronograma", tags=["Cronograma"])


def _get_service(db=Depends(get_db)):
    return CronogramaService(CronogramaRepository(db))


@router.get(
    "/tarefas",
    response_model=PaginatedResponse[TarefaGanttResponse],
    summary="Listar tarefas para Gantt",
)
def listar_tarefas(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    projeto_id: int | None = Query(default=None),
    service: CronogramaService = Depends(_get_service),
):
    return service.listar_tarefas_gantt(page, page_size, projeto_id)

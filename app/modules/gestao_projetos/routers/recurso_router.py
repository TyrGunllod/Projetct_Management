from fastapi import APIRouter, Depends, Query
from shared.schemas.base import ErrorResponse, MessageResponse, PaginatedResponse

from app.database import get_db
from app.modules.gestao_projetos.schemas.recurso import RecursoCreate, RecursoResponse, RecursoUpdate
from app.modules.gestao_projetos.repositories.recurso_repository import RecursoRepository
from app.modules.gestao_projetos.services.recurso_service import RecursoService

router = APIRouter(prefix="/v1/recursos", tags=["Recursos"])


def _get_service(db=Depends(get_db)):
    return RecursoService(RecursoRepository(db))


@router.get(
    "",
    response_model=PaginatedResponse[RecursoResponse],
    summary="Listar",
)
def listar(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    projeto_id: int | None = Query(default=None),
    service: RecursoService = Depends(_get_service),
):
    return service.listar(page, page_size, projeto_id)


@router.get(
    "/{id}",
    response_model=RecursoResponse,
    summary="Buscar por ID",
    responses={404: {"model": ErrorResponse}},
)
def buscar(id: int, service: RecursoService = Depends(_get_service)):
    return service.buscar(id)


@router.post(
    "",
    response_model=RecursoResponse,
    status_code=201,
    summary="Alocar recurso",
    responses={409: {"model": ErrorResponse}},
)
def criar(dados: RecursoCreate, service: RecursoService = Depends(_get_service)):
    return service.criar(dados)


@router.put(
    "/{id}",
    response_model=RecursoResponse,
    summary="Atualizar",
    responses={404: {"model": ErrorResponse}},
)
def atualizar(id: int, dados: RecursoUpdate, service: RecursoService = Depends(_get_service)):
    return service.atualizar(id, dados)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Desalocar",
    responses={404: {"model": ErrorResponse}},
)
def desalocar(id: int, service: RecursoService = Depends(_get_service)):
    service.desalocar(id)
    return MessageResponse(message=f"Recurso {id} desalocado com sucesso.")

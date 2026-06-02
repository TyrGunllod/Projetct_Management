from fastapi import APIRouter, Depends, Query
from shared.schemas.base import ErrorResponse, MessageResponse, PaginatedResponse

from app.database import get_db
from app.modules.gestao_projetos.schemas.tarefa import TarefaCreate, TarefaResponse, TarefaUpdate
from app.modules.gestao_projetos.schemas.registro_tarefa import RegistroCreate, RegistroResponse, RegistroUpdate
from app.modules.gestao_projetos.repositories.tarefa_repository import TarefaRepository
from app.modules.gestao_projetos.repositories.registro_repository import RegistroRepository
from app.modules.gestao_projetos.services.tarefa_service import TarefaService
from app.modules.gestao_projetos.services.registro_service import RegistroService

router = APIRouter(prefix="/v1/tarefas", tags=["Tarefas"])


def _get_service(db=Depends(get_db)):
    return TarefaService(TarefaRepository(db))


def _get_registro_service(db=Depends(get_db)):
    return RegistroService(RegistroRepository(db))


@router.get(
    "",
    response_model=PaginatedResponse[TarefaResponse],
    summary="Listar",
)
def listar(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    projeto_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    service: TarefaService = Depends(_get_service),
):
    return service.listar(page, page_size, projeto_id, status)


@router.get(
    "/{id}",
    response_model=TarefaResponse,
    summary="Buscar por ID",
    responses={404: {"model": ErrorResponse}},
)
def buscar(id: int, service: TarefaService = Depends(_get_service)):
    return service.buscar(id)


@router.post(
    "",
    response_model=TarefaResponse,
    status_code=201,
    summary="Criar",
)
def criar(dados: TarefaCreate, service: TarefaService = Depends(_get_service)):
    return service.criar(dados)


@router.put(
    "/{id}",
    response_model=TarefaResponse,
    summary="Atualizar",
    responses={404: {"model": ErrorResponse}},
)
def atualizar(id: int, dados: TarefaUpdate, service: TarefaService = Depends(_get_service)):
    return service.atualizar(id, dados)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Desativar",
    responses={404: {"model": ErrorResponse}},
)
def desativar(id: int, service: TarefaService = Depends(_get_service)):
    service.desativar(id)
    return MessageResponse(message=f"Tarefa {id} desativada com sucesso.")


@router.get(
    "/{tarefa_id}/registros",
    response_model=PaginatedResponse[RegistroResponse],
    summary="Listar registros",
)
def listar_registros(
    tarefa_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    tipo: str | None = Query(default=None),
    service: RegistroService = Depends(_get_registro_service),
):
    return service.listar_por_tarefa(tarefa_id, page, page_size, tipo)


@router.post(
    "/{tarefa_id}/registros",
    response_model=RegistroResponse,
    status_code=201,
    summary="Criar registro",
)
def criar_registro(
    tarefa_id: int,
    dados: RegistroCreate,
    service: RegistroService = Depends(_get_registro_service),
):
    return service.criar(tarefa_id, dados)


@router.put(
    "/registros/{registro_id}",
    response_model=RegistroResponse,
    summary="Atualizar registro",
    responses={404: {"model": ErrorResponse}},
)
def atualizar_registro(
    registro_id: int,
    dados: RegistroUpdate,
    service: RegistroService = Depends(_get_registro_service),
):
    return service.atualizar(registro_id, dados)


@router.delete(
    "/registros/{registro_id}",
    response_model=MessageResponse,
    summary="Desativar registro",
    responses={404: {"model": ErrorResponse}},
)
def desativar_registro(
    registro_id: int,
    service: RegistroService = Depends(_get_registro_service),
):
    service.desativar(registro_id)
    return MessageResponse(message=f"Registro {registro_id} desativado com sucesso.")

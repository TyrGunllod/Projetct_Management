from fastapi import APIRouter, Depends

from app.database import get_db
from app.modules.gestao_projetos.schemas.dashboard import DashboardResponse
from app.modules.gestao_projetos.repositories.dashboard_repository import DashboardRepository
from app.modules.gestao_projetos.services.dashboard_service import DashboardService

router = APIRouter(prefix="/v1/dashboard", tags=["Dashboard"])


def _get_service(db=Depends(get_db)):
    return DashboardService(DashboardRepository(db))


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Dados completos do dashboard",
)
def carregar(service: DashboardService = Depends(_get_service)):
    return service.carregar_dados()

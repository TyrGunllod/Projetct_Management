"""
Standalone API server for local testing.
Run: python run_api.py
"""

import importlib.util
import sys
from pathlib import Path

GRINDX_PACKAGES = str(Path(__file__).resolve().parent.parent.parent / "GrindX" / "packages")
GRINDX_API = str(Path(GRINDX_PACKAGES).parent / "apps" / "api-postgres")
PROJECT_ROOT = str(Path(__file__).resolve().parent)

sys.path.insert(0, GRINDX_PACKAGES)
sys.path.insert(0, GRINDX_API)
sys.path.insert(0, PROJECT_ROOT)

import app  # noqa: E402
import app.modules  # noqa: E402

LOCAL_MODULES = str(Path(__file__).resolve().parent / "app" / "modules")
_local_pkg = Path(LOCAL_MODULES) / "gestao_projetos"
_spec = importlib.util.spec_from_file_location(
    "app.modules.gestao_projetos",
    str(_local_pkg / "__init__.py"),
    submodule_search_locations=[str(_local_pkg)],
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["app.modules.gestao_projetos"] = _mod
_spec.loader.exec_module(_mod)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.gestao_projetos.routers.projeto_router import router as projeto_router
from app.modules.gestao_projetos.routers.tarefa_router import router as tarefa_router
from app.modules.gestao_projetos.routers.recurso_router import router as recurso_router
from app.modules.gestao_projetos.routers.dashboard_router import router as dashboard_router
from app.modules.gestao_projetos.routers.cronograma_router import router as cronograma_router

app = FastAPI(title="Gestão de Projetos - Standalone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projeto_router)
app.include_router(tarefa_router)
app.include_router(recurso_router)
app.include_router(dashboard_router)
app.include_router(cronograma_router)


@app.get("/")
def root():
    return {"message": "Gestão de Projetos API - Standalone Mode"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

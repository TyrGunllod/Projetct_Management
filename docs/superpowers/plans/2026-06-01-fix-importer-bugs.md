# Fix Importer Bugs — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Corrigir 3 bugs no sistema de importação de módulos que impedem a importação dos módulos standalone via `.zip`.

**Architecture:** (1) Corrigir o `package()` nos `export.py` para gerar zips com estrutura correta; (2) Corrigir `register_router()` no `import_module.py` para usar o path correto dos routers; (3) Adicionar `register_dependency()` no `import_module.py` para registrar a factory de injeção de dependência.

**Tech Stack:** Python, FastAPI, Alembic, SQLAlchemy

---

## Arquivos Afetados

| Arquivo | Ação |
|---------|------|
| `D:\_Projetos\GrindX\apps\api-postgres\scripts\import_module.py` | Modificar (bug 2 + bug 3) |
| `D:\_Projetos\Project_Management\modulo-projeto\app\modules\projeto\export.py` | Modificar (bug 1) |
| `D:\_Projetos\Project_Management\modulo-recursos\app\modules\recursos\export.py` | Modificar (bug 1) |
| `D:\_Projetos\Project_Management\modulo-tarefas\app\modules\tarefas\export.py` | Modificar (bug 1) |
| `D:\_Projetos\Project_Management\modulo-cronograma\app\modules\cronograma\export.py` | Modificar (bug 1) |
| `D:\_Projetos\Project_Management\modulo-dashboard\app\modules\dashboard\export.py` | Modificar (bug 1) |
| `D:\_Projetos\GrindX\apps\api-postgres\tests\unit\test_import_module.py` | Criar (testes para as correções) |

---

## Task 1: Corrigir `register_router()` no import_module.py

**Files:**
- Modify: `D:\_Projetos\GrindX\apps\api-postgres\scripts\import_module.py:176-223`
- Test: `D:\_Projetos\GrindX\apps\api-postgres\tests\unit\test_import_module.py`

- [ ] **Step 1: Criar teste que valida o path correto do router**

```python
# D:\_Projetos\GrindX\apps\api-postgres\tests\unit\test_import_module.py
"""Tests for the import_module script."""

import importlib
import json
import textwrap
from pathlib import Path

import pytest


@pytest.fixture
def import_module():
    """Importa o módulo import_module fresh para cada teste."""
    import sys
    if "scripts.import_module" in sys.modules:
        del sys.modules["scripts.import_module"]
    mod = importlib.import_module("scripts.import_module")
    return mod


class TestRegisterRouter:
    def test_gera_import_path_para_modulo_dentro_de_modules(self, import_module, tmp_path):
        """O import do router deve usar app.modules.{name}.routers.{name}_router."""
        main_py = tmp_path / "main.py"
        main_py.write_text(textwrap.dedent("""\
            from app.routers.health_router import router as health_router
            app.include_router(health_router)
        """))

        manifest = {"module_name": "projeto"}

        import_module.register_router(manifest, main_py=main_py, force=False)

        content = main_py.read_text()
        assert "from app.modules.projeto.routers.projeto_router import router as projeto_router" in content
        assert "app.include_router(projeto_router)" in content

    def test_nao_duplica_se_ja_registrado(self, import_module, tmp_path):
        """Se o router já foi registrado, não adiciona de novo."""
        main_py = tmp_path / "main.py"
        import_line = "from app.modules.projeto.routers.projeto_router import router as projeto_router"
        register_line = "app.include_router(projeto_router)"
        main_py.write_text(f"from app.routers.health_router import router as health_router\n{import_line}\napp.include_router(health_router)\n{register_line}\n")

        manifest = {"module_name": "projeto"}
        import_module.register_router(manifest, main_py=main_py, force=False)

        content = main_py.read_text()
        assert content.count(import_line) == 1
        assert content.count(register_line) == 1
```

- [ ] **Step 2: Rodar teste para confirmar que falha**

Run: `cd D:\_Projetos\GrindX\apps\api-postgres && python -m pytest tests/unit/test_import_module.py::TestRegisterRouter -v`
Expected: FAIL — `register_router` não aceita parâmetro `main_py`

- [ ] **Step 3: Implementar correção no register_router**

Mudar a função `register_router` em `import_module.py` para:
1. Aceitar parâmetro opcional `main_py: Path | None` (para testes e uso direto)
2. Gerar `from app.modules.{module_name}.routers.{module_name}_router import router as {module_name}_router`
3. Buscar o último import que contenha `from app.` e `import router as` (incluindo `from app.modules.`)

```python
def register_router(manifest: dict, force: bool, main_py: Path | None = None) -> None:
    module_name = manifest["module_name"]
    if main_py is None:
        api_dir = _get_monorepo_root() / "apps" / "api-postgres"
        main_py = api_dir / "app" / "main.py"

    content = main_py.read_text(encoding="utf-8")

    import_line = (
        f"from app.modules.{module_name}.routers.{module_name}_router"
        f" import router as {module_name}_router"
    )
    register_line = f"app.include_router({module_name}_router)"

    if import_line in content and register_line in content:
        logger.info("Router já registrado em main.py")
        return

    if not force and (import_line in content or register_line in content):
        raise FileExistsError("Router parcialmente registrado. Use --force.")

    lines = content.splitlines(keepends=True)
    last_import_idx = None
    last_include_idx = None

    for i, line in enumerate(lines):
        if "from app." in line and "import router as" in line:
            last_import_idx = i
        if "app.include_router(" in line:
            last_include_idx = i

    if last_import_idx is None:
        logger.warning(
            "Não foi possível encontrar local para inserir import do router em main.py"
        )
    if last_include_idx is None:
        logger.warning(
            "Não foi possível encontrar local para inserir app.include_router() em main.py"
        )

    if last_import_idx is not None and import_line not in content:
        lines.insert(last_import_idx + 1, import_line + "\n")
        if last_include_idx is not None and last_include_idx >= last_import_idx:
            last_include_idx += 1

    if last_include_idx is not None and register_line not in content:
        lines.insert(last_include_idx + 1, register_line + "\n")

    main_py.write_text("".join(lines), encoding="utf-8")
    logger.info("Router registrado em main.py")
```

- [ ] **Step 4: Rodar teste para confirmar que passa**

Run: `cd D:\_Projetos\GrindX\apps\api-postgres && python -m pytest tests/unit/test_import_module.py::TestRegisterRouter -v`
Expected: 2 passed

- [ ] **Step 5: Corrigir register_alembic_import para aceitar env_py (mesmo padrão)**

A função `register_alembic_import` também precisa do parâmetro `env_py: Path | None` para ser testável:

```python
def register_alembic_import(manifest: dict, force: bool = False, env_py: Path | None = None) -> None:
    module_name = manifest["module_name"]
    entity_name = manifest["entity_name"]
    if env_py is None:
        api_dir = _get_monorepo_root() / "apps" / "api-postgres"
        env_py = api_dir / "alembic" / "env.py"

    content = env_py.read_text(encoding="utf-8")
    # ... resto da função permanece igual
```

- [ ] **Step 6: Commit**

```bash
cd D:\_Projetos\GrindX
git add apps/api-postgres/scripts/import_module.py apps/api-postgres/tests/unit/test_import_module.py
git commit -m "fix(importer): corrigir path do router e adicionar param testável em register_alembic_import"
```

---

## Task 2: Adicionar `register_dependency()` no import_module.py

**Files:**
- Modify: `D:\_Projetos\GrindX\apps\api-postgres\scripts\import_module.py`
- Test: `D:\_Projetos\GrindX\apps\api-postgres\tests\unit\test_import_module.py`

- [ ] **Step 1: Criar teste para register_dependency**

Adicionar ao `test_import_module.py`:

```python
class TestRegisterDependency:
    def test_cria_factory_no_dependencies_py(self, import_module, tmp_path):
        """Registra get_{module_name}_service em dependencies.py."""
        deps_py = tmp_path / "dependencies.py"
        deps_py.write_text(textwrap.dedent("""\
            from fastapi import Depends
            from sqlalchemy.orm import Session
            from app.database import get_db

            # --- Versoes vinculadas das permissoes ---

            def require_role(*roles):
                pass
        """))

        manifest = {"module_name": "projeto", "entity_name": "Projeto"}
        import_module.register_dependency(manifest, deps_py=deps_py)

        content = deps_py.read_text()
        assert "def get_projeto_service(db: Session = Depends(get_db)) -> ProjetoService:" in content
        assert "from app.modules.projeto.repositories.projeto_repository import ProjetoRepository" in content
        assert "from app.modules.projeto.services.projeto_service import ProjetoService" in content

    def test_nao_duplica_se_ja_existe(self, import_module, tmp_path):
        """Se a factory já existe, não duplica."""
        deps_py = tmp_path / "dependencies.py"
        deps_py.write_text(textwrap.dedent("""\
            def get_projeto_service(db):
                pass

            # --- Versoes vinculadas das permissoes ---
        """))

        manifest = {"module_name": "projeto", "entity_name": "Projeto"}
        import_module.register_dependency(manifest, deps_py=deps_py)

        content = deps_py.read_text()
        assert content.count("def get_projeto_service") == 1
```

- [ ] **Step 2: Rodar teste para confirmar que falha**

Run: `cd D:\_Projetos\GrindX\apps\api-postgres && python -m pytest tests/unit/test_import_module.py::TestRegisterDependency -v`
Expected: FAIL — `register_dependency` não existe

- [ ] **Step 3: Implementar register_dependency**

Adicionar a função em `import_module.py` (antes de `register_alembic_import`):

```python
def register_dependency(manifest: dict, force: bool = False, deps_py: Path | None = None) -> None:
    module_name = manifest["module_name"]
    entity_name = manifest["entity_name"]
    if deps_py is None:
        api_dir = _get_monorepo_root() / "apps" / "api-postgres"
        deps_py = api_dir / "app" / "auth" / "dependencies.py"

    content = deps_py.read_text(encoding="utf-8")

    factory_name = f"get_{module_name}_service"
    if factory_name in content:
        logger.info("Dependency já registrada")
        return

    marker = "# --- Versões vinculadas das permissões ---"
    if marker not in content:
        logger.warning("Marker não encontrado em dependencies.py. Adicione manualmente.")
        return

    entity_lower = entity_name.lower()
    factory = (
        f"from app.modules.{module_name}.repositories.{module_name}_repository import {entity_name}Repository\n"
        f"from app.modules.{module_name}.services.{module_name}_service import {entity_name}Service\n\n\n"
        f"def {factory_name}(db: Session = Depends(get_db)) -> {entity_name}Service:\n"
        f'    """Factory para o {entity_name}Service."""\n'
        f"    repository = {entity_name}Repository(db)\n"
        f"    return {entity_name}Service(repository)\n\n\n"
        f"{marker}\n"
    )

    content = content.replace(marker, factory)
    deps_py.write_text(content, encoding="utf-8")
    logger.info("Dependency registrada: %s", factory_name)
```

- [ ] **Step 4: Rodar teste para confirmar que passa**

Run: `cd D:\_Projetos\GrindX\apps\api-postgres && python -m pytest tests/unit/test_import_module.py::TestRegisterDependency -v`
Expected: 2 passed

- [ ] **Step 5: Integrar no fluxo de import_module()

Adicionar o step no função `import_module()` (linha ~354, antes de `register_alembic_import`):

```python
        if not dry_run:
            register_dependency(manifest, force)
        steps.append("Dependency registrada")
```

- [ ] **Step 6: Rodar todos os testes de import_module**

Run: `cd D:\_Projetos\GrindX\apps\api-postgres && python -m pytest tests/unit/test_import_module.py -v`
Expected: Todos passando

- [ ] **Step 7: Commit**

```bash
cd D:\_Projetos\GrindX
git add apps/api-postgres/scripts/import_module.py apps/api-postgres/tests/unit/test_import_module.py
git commit -m "feat(importer): adicionar register_dependency para factories de service"
```

---

## Task 3: Corrigir `package()` nos export.py (5 módulos)

**Files:**
- Modify: `D:\_Projetos\Project_Management\modulo-projeto\app\modules\projeto\export.py:156-194`
- Modify: `D:\_Projetos\Project_Management\modulo-recursos\app\modules\recursos\export.py:156-194`
- Modify: `D:\_Projetos\Project_Management\modulo-tarefas\app\modules\tarefas\export.py:156-194`
- Modify: `D:\_Projetos\Project_Management\modulo-cronograma\app\modules\cronograma\export.py:130-169`
- Modify: `D:\_Projetos\Project_Management\modulo-dashboard\app\modules\dashboard\export.py:130-169`

- [ ] **Step 1: Corrigir export.py do modulo-projeto**

Mudar a função `package()` — o `arcname` dos arquivos backend deve ser relativo ao diretório raiz do módulo standalone (onde está o `module.json`), NÃO ao `Project_Management`.

Trocar:
```python
        for file in MODULE_SRC.rglob("*"):
            if file.is_file() and "__pycache__" not in file.parts and not file.name.endswith(".pyc"):
                arcname = str(file.relative_to(MODULE_SRC.parent.parent.parent.parent.parent))
                zf.write(file, arcname)
```

Por:
```python
        standalone_root = MODULE_SRC.parent.parent.parent  # raiz do modulo-{name}/
        for file in MODULE_SRC.rglob("*"):
            if file.is_file() and "__pycache__" not in file.parts and not file.name.endswith(".pyc"):
                arcname = str(file.relative_to(standalone_root))
                zf.write(file, arcname)
```

Também corrigir o `FRONTEND_SRC` e `MIGRATION_SRC` para serem calculados a partir do `standalone_root`:

Trocar:
```python
    dist_dir = module_dir.parent.parent.parent.parent.parent / "dist"
```

Por:
```python
    standalone_root = module_dir.parent.parent.parent
    dist_dir = standalone_root / "dist"
```

- [ ] **Step 2: Testar o zip gerado**

```powershell
cd D:\_Projetos\Project_Management\modulo-projeto
$env:GRINDX_PACKAGES = "D:\_Projetos\GrindX\packages"
python -m app.modules.projeto.export package --dry-run
```

Depois gerar o zip real e verificar a estrutura:
```powershell
python -m app.modules.projeto.export package
# Verificar estrutura do zip:
python -c "import zipfile; zf=zipfile.ZipFile('dist/modulo-projeto.zip'); print('\n'.join(zf.namelist()[:20]))"
```

Esperado: `module.json` na raiz, `app/modules/projeto/...`, `frontend/...`, `migration/...`

- [ ] **Step 3: Aplicar a mesma correção nos outros 4 módulos**

Aplicar a mesma troca em:
- `modulo-recursos/app/modules/recursos/export.py`
- `modulo-tarefas/app/modules/tarefas/export.py`
- `modulo-cronograma/app/modules/cronograma/export.py`
- `modulo-dashboard/app/modules/dashboard/export.py`

A correção é idêntica em todos: trocar `MODULE_SRC.parent.parent.parent.parent.parent` por `MODULE_SRC.parent.parent.parent` no cálculo de `arcname` e `dist_dir`.

- [ ] **Step 4: Testar dry-run em todos os módulos**

```powershell
foreach ($mod in @("projeto", "recursos", "tarefas", "cronograma", "dashboard")) {
    cd "D:\_Projetos\Project_Management\modulo-$mod"
    python -m "app.modules.$mod.export" package --dry-run
    cd ..
}
```

- [ ] **Step 5: Commit**

```bash
cd D:\_Projetos\Project_Management
git add modulo-projeto/app/modules/projeto/export.py modulo-recursos/app/modules/recursos/export.py modulo-tarefas/app/modules/tarefas/export.py modulo-cronograma/app/modules/cronograma/export.py modulo-dashboard/app/modules/dashboard/export.py
git commit -m "fix(export): corrigir estrutura do zip para compatibilidade com importer"
```

---

## Task 4: Teste de integração — simular import completo

**Files:**
- Test: `D:\_Projetos\GrindX\apps\api-postgres\tests\unit\test_import_module.py`

- [ ] **Step 1: Criar teste de integração que simula o fluxo completo**

Adicionar ao `test_import_module.py`:

```python
class TestImportFlow:
    def test_fluxo_completo_register_router_e_dependency(self, import_module, tmp_path):
        """Simula o fluxo: register_router + register_dependency + register_alembic_import."""
        main_py = tmp_path / "main.py"
        main_py.write_text(textwrap.dedent("""\
            from app.routers.health_router import router as health_router
            app.include_router(health_router)
        """))

        deps_py = tmp_path / "dependencies.py"
        deps_py.write_text(textwrap.dedent("""\
            # --- Versoes vinculadas das permissoes ---
        """))

        env_py = tmp_path / "env.py"
        env_py.write_text(textwrap.dedent("""\
            from app.modules.portal.models.portal import Aba, Modulo  # noqa: F401
        """))

        manifest = {
            "module_name": "projeto",
            "entity_name": "Projeto",
        }

        # 1. Register router
        import_module.register_router(manifest, main_py=main_py, force=False)
        content_main = main_py.read_text()
        assert "from app.modules.projeto.routers.projeto_router import router as projeto_router" in content_main
        assert "app.include_router(projeto_router)" in content_main

        # 2. Register dependency
        import_module.register_dependency(manifest, deps_py=deps_py)
        content_deps = deps_py.read_text()
        assert "def get_projeto_service(" in content_deps

        # 3. Register alembic import
        import_module.register_alembic_import(manifest, env_py=env_py)
        content_env = env_py.read_text()
        assert "from app.modules.projeto.models.projeto import Projeto  # noqa: F401" in content_env
```

- [ ] **Step 2: Rodar teste de integração**

Run: `cd D:\_Projetos\GrindX\apps\api-postgres && python -m pytest tests/unit/test_import_module.py::TestImportFlow -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
cd D:\_Projetos\GrindX
git add apps/api-postgres/tests/unit/test_import_module.py
git commit -m "test(importer): adicionar teste de integração do fluxo completo"
```

---

## Self-Review

1. **Spec coverage:** Os 3 bugs estão cobertos — router path (Task 1), dependency factory (Task 2), zip structure (Task 3), integração (Task 4).

2. **Placeholder scan:** Nenhum placeholder encontrado. Todo o código está completo.

3. **Type consistency:** `register_router` aceita `main_py: Path | None`, `register_dependency` aceita `deps_py: Path | None`, `register_alembic_import` precisa de `env_py: Path | None`. Todos são consistentes.

**Nota:** A função `register_alembic_import` também precisa receber o parâmetro `env_py` para testes. Essa correção deve ser feita na Task 1 ou como follow-up.

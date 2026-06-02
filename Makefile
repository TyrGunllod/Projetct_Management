# ==========================================
# Módulo Gestão de Projetos — Standalone
# ==========================================

MODULE := gestao_projetos
ENTITY := GestaoProjetos

.PHONY: test test-unit test-integration package export dry-run clean help api frontend dev stop

# ==========================================
# Testes
# ==========================================

test:
	@python -m pytest app/modules/$(MODULE)/tests/ -v --tb=short

test-unit:
	@python -m pytest app/modules/$(MODULE)/tests/ -v --tb=short -k "unit"

test-integration:
	@python -m pytest app/modules/$(MODULE)/tests/ -v --tb=short -k "integration"

# ==========================================
# Desenvolvimento Standalone
# ==========================================

api:
	@echo Iniciando API Standalone em http://localhost:8000 ...
	@cmd /c "set DATABASE_URL=sqlite:///./test.db&& set SECRET_KEY=test-secret-key-for-standalone-only&& set DEBUG=true&& python run_api.py"

frontend:
	@echo Iniciando Frontend Standalone em http://localhost:3000 ...
	@python run_frontend.py

dev:
	@echo Iniciando API + Frontend...
	@cmd /c "set DATABASE_URL=sqlite:///./test.db&& set SECRET_KEY=test-secret-key-for-standalone-only&& set DEBUG=true&& start /b python run_api.py && python run_frontend.py"

stop:
	@echo Encerrando servidores...
	@taskkill /F /IM python.exe >nul 2>&1 || true
	@echo Servidores encerrados.

# ==========================================
# Empacotamento & Exportação
# ==========================================

package:
	@python -m app.modules.$(MODULE).export package
	@echo.
	@echo Zip gerado: dist/modulo-$(MODULE).zip

dry-run:
	@python -m app.modules.$(MODULE).export package --dry-run

export:
	@python -m app.modules.$(MODULE).export

export-dry:
	@python -m app.modules.$(MODULE).export --dry-run

# ==========================================
# Importação
# ==========================================

import: package
	@echo.
	@echo Copiando zip para import/ do GrindX...
	@python -c "import shutil,os; os.makedirs('../GrindX/import',exist_ok=True); shutil.copy2('dist/modulo-$(MODULE).zip','../GrindX/import/'); print('Copiado para ../GrindX/import/modulo-$(MODULE).zip')"

# ==========================================
# Utilitários
# ==========================================

clean:
	@echo Limpando caches...
	@if exist dist rmdir /s /q dist
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@echo Limpeza concluída

help:
	@echo.
	@echo Módulo $(ENTITY) — Comandos disponíveis:
	@echo.
	@echo   make test             Roda todos os testes
	@echo   make test-unit        Roda apenas testes unitários
	@echo   make test-integration Roda apenas testes de integração
	@echo   make api              Sobe API FastAPI em http://localhost:8000
	@echo   make frontend         Sobe Frontend HTML em http://localhost:3000
	@echo   make dev              Sobe API + Frontend simultaneamente
	@echo   make stop             Encerra todos os servidores
	@echo   make package          Gera o zip para importação
	@echo   make dry-run          Simula a geração do zip
	@echo   make export           Exporta direto para o GrindX (CLI)
	@echo   make import           Gera zip + copia para import/ do GrindX
	@echo   make clean            Limpa caches e __pycache__
	@echo   make help             Exibe esta ajuda
	@echo

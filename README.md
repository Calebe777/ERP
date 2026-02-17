# ERP Desktop Offline em Python (PySide6 + SQLite + SQLAlchemy + Alembic)

Projeto ERP desktop offline com foco em operação local e interface moderna:
- **UI desktop:** PySide6 (Qt)
- **Banco local:** SQLite (`data/erp.db`)
- **ORM:** SQLAlchemy 2.x
- **Migrations:** Alembic

## Módulos implementados
1. **Login local**
   - Usuário padrão criado automaticamente: `admin` / `admin123`
2. **Painel de indicadores (dashboard)**
   - Total de produtos, produtos ativos, NF-e importadas, itens e valor total em notas
3. **Cadastro de Produtos**
   - Campos: código, descrição, preço, estoque, ativo/inativo
   - Busca por código/descrição e CRUD completo
4. **Módulo Fiscal (NF-e XML)**
   - Importação de XML de NF-e
   - Extração dos dados principais: chave, número, série, emissor, CNPJ, emissão, valor total, itens
   - Listagem pesquisável e resumo gerencial

## Estrutura de pastas
```text
src/
  app/
    ui/
    data/
    domain/
    services/
alembic/
  versions/
scripts/
```

## Pré-requisitos (Windows)
- Python **3.11+** instalado
- PowerShell ou Prompt de Comando

## Como rodar no Windows (PowerShell)
```powershell
# 1) Criar ambiente virtual e instalar dependências
.\scripts\setup_venv.ps1

# 2) Aplicar migrations
.\scripts\run_migrations.ps1

# 3) Executar aplicação
.\scripts\run_app.ps1
```

## Como rodar no Windows (CMD)
```bat
scripts\setup_venv.bat
scripts\run_migrations.bat
scripts\run_app.bat
```

## Execução rápida (1 clique no Windows)
```bat
scripts\iniciar_erp.bat
```
- Na primeira execução, o script cria `.venv`, instala dependências e aplica migrations.
- Nas próximas execuções, ele só atualiza o banco e abre o ERP.

## Documentação complementar
- Requisitos funcionais e não funcionais: `docs/REQUISITOS_ERP_DESKTOP_OFFLINE.md`
- Guia de execução e atalho de desktop: `docs/COMO_EXECUTAR.md`

## Comandos manuais equivalentes
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
alembic upgrade head
python -m app.main
```

## Observações
- O banco é local/offline e fica no arquivo `data/erp.db`.
- As migrations ficam em `alembic/versions`.
- A importação de NF-e impede duplicidade da mesma chave de acesso.

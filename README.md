# ERP Desktop Offline (.NET 8 + WPF + EF Core + SQLite)

ERP desktop offline com arquitetura em camadas:
- **UI (WPF/MVVM)**
- **Application**
- **Domain**
- **Infrastructure**

## Recursos implementados
- Autenticação local (usuários e papel básico Admin/Operator).
- Seed automático de usuário admin padrão (`admin` / `admin123`).
- CRUD de Produtos:
  - Código
  - Descrição
  - Preço
  - Estoque
  - Ativo/Inativo
- Busca por código/descrição.
- Paginação simples.
- Validações básicas.
- 100% offline usando SQLite local.

## Estrutura
- `src/Erp.Domain`: entidades e enums.
- `src/Erp.Application`: contratos e regras de negócio.
- `src/Erp.Infrastructure`: EF Core, SQLite, repositórios, migrations.
- `src/Erp.UI`: WPF + MVVM.

## Scripts
- `scripts/restore.sh`: restaura dependências.
- `scripts/create-db.sh`: cria/atualiza banco aplicando migrations.
- `scripts/migrate.sh`: aplica migrations via `dotnet ef`.
- `scripts/run.sh`: executa aplicação WPF.

## Comandos diretos
```bash
dotnet restore ERP.sln
dotnet ef database update --project src/Erp.Infrastructure --startup-project src/Erp.UI
dotnet run --project src/Erp.UI
```

> Requisito: SDK .NET 8 instalado na máquina.

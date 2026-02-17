# Como executar o ERP Desktop Offline

Este guia mostra como executar o projeto localmente e como deixar um atalho de **1 clique** para abrir o ERP no Windows.

## 1) Pré-requisitos

- Windows 10/11
- Python 3.11+ instalado e disponível no PATH

## 2) Primeira execução (manual)

No terminal, dentro da pasta do projeto:

```bat
scripts\setup_venv.bat
scripts\run_migrations.bat
scripts\run_app.bat
```

Isso irá:
1. Criar `.venv`
2. Instalar dependências
3. Aplicar migrations no banco local
4. Abrir o ERP

## 3) Execução com 1 clique (recomendado)

Foi adicionado o script `scripts\iniciar_erp.bat`.

### Como usar
1. Dê duplo clique em `scripts\iniciar_erp.bat`.
2. Na primeira vez, ele prepara o ambiente automaticamente.
3. Nas próximas execuções, apenas atualiza banco (migrations) e abre o ERP.

### O que o script faz
- Detecta a raiz do projeto
- Cria `.venv` se não existir
- Instala dependências com `pip install -e .`
- Executa `alembic upgrade head`
- Inicia a aplicação com `python -m app.main`

## 4) Criar atalho no Desktop (abrir com um clique)

1. Clique com botão direito em `scripts\iniciar_erp.bat`.
2. Escolha **Enviar para > Área de trabalho (criar atalho)**.
3. Renomeie o atalho para `ERP Offline`.

Pronto: o usuário abre o ERP clicando no atalho do Desktop.

## 5) Banco local e operação offline

- O banco é local em `data\erp.db`.
- O sistema funciona sem internet para as operações internas.
- Internet só é necessária para futuras integrações externas (ex.: fiscal online, APIs).

## 6) Login padrão inicial

- Usuário: `admin`
- Senha: `admin123`

> Recomendação: alterar a senha padrão no primeiro acesso.

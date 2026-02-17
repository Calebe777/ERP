# Documento de Requisitos — ERP Desktop Offline (LAN opcional)

## 1) Visão geral

**Objetivo:** centralizar cadastro, estoque, compras, vendas/PDV, financeiro, relatórios e administração em um único sistema desktop, operando sem internet.

**Público-alvo:**
- Comércio varejista e atacadista
- Loja física com PDV
- Delivery e prestação de serviços
- Pequenas e médias empresas

**Premissas offline:**
- O sistema opera localmente com aplicação desktop + banco local.
- Cadastro, estoque, vendas, financeiro e relatórios funcionam sem internet.
- Integrações externas e rotinas fiscais podem exigir internet quando usadas, sem interromper o ERP principal.

---

## 2) Escopo funcional por módulos

### 2.1 Cadastro

#### Pessoas
- Tipos: clientes, fornecedores, funcionários, transportadoras, vendedores e motoristas
- Campos: nome/razão social, CPF/CNPJ, IE/RG, endereço, contatos, situação, observações
- Comercial: limite de crédito, condição de pagamento padrão, tabela de preço padrão

#### Produtos
- Identificação: código interno, código de barras, descrição, unidade, marca e categoria
- Comercial/estoque: custo, preço de venda, estoque atual e mínimo, localização
- Fiscal (opcional): NCM, CEST, CFOP padrão e regras de tributação

#### Tabelas auxiliares
- Formas de pagamento
- Plano de contas
- Centros de custo
- Bancos e contas
- Categorias, marcas, unidades e tabelas de preço

### 2.2 Estoque
- Entradas: compra, ajuste e devolução
- Saídas: venda, perda e consumo interno
- Transferência entre depósitos (quando aplicável)
- Inventário geral e parcial com ajuste de divergência
- Relatórios: posição de estoque, estoque mínimo, sem giro, curva ABC, histórico e mais vendidos

### 2.3 Compras
- Cotação com fornecedores (opcional)
- Pedido de compra
- Entrada de mercadoria com movimentação automática de estoque
- Importação XML (opcional)
- Integração com financeiro para gerar contas a pagar
- Devolução de compra

### 2.4 Vendas / Movimento

#### Orçamento
- Validade
- Conversão em venda
- Impressão

#### Pedido de venda
- Venda normal
- Entrega futura
- Múltiplas formas de pagamento

#### PDV
- Venda rápida por código de barras
- Regras de desconto por permissão
- Cancelamento de item e de venda com auditoria
- Sangria, suprimento e fechamento de caixa
- Controle de operador por turno

#### Delivery/Comandas (opcional)
- Mesas/comandas
- Taxa de entrega
- Status do pedido
- Impressão para cozinha

### 2.5 Fiscal (opcional e plugável)
- Emissão e gestão de NF-e, NFC-e, NFS-e, CTe e MDFe (quando necessário)
- Importação XML, cancelamento, carta de correção, inutilização, SPED etc.

> Observação: o módulo fiscal pode ser entregue em fase posterior sem impedir o ERP de operar no MVP.

### 2.6 Financeiro

#### Contas a receber
- Parcelamento
- Juros e multa
- Baixa manual e automática
- Controle de inadimplência

#### Contas a pagar
- Parcelamento
- Pagamento parcial
- Previsto x realizado

#### Caixa
- Abertura/fechamento por operador
- Resumo por forma de pagamento
- Conciliação simples (opcional)

#### Relatórios financeiros
- Fluxo de caixa
- DRE simplificado
- Despesas por categoria
- Lucro por período

### 2.7 Relatórios e Dashboard
- Vendas por período e por vendedor
- Produtos mais vendidos e margem
- Ticket médio e ranking de clientes
- KPIs básicos com gráficos

### 2.8 Administração
- Usuários, perfis e permissões por módulo/ação
- Log de atividades e auditoria
- Configurações da empresa, impressoras e formas de pagamento
- Rotina de backup local automático + backup opcional em nuvem

---

## 3) Requisitos não funcionais

- **Offline-first:** operações críticas devem funcionar sem internet.
- **Desempenho:** abertura rápida do PDV e buscas eficientes.
- **Confiabilidade:** transações atômicas em venda, baixa financeira e movimentação de estoque.
- **Auditoria:** rastrear usuário, data/hora e alterações antes/depois.
- **Segurança:** senha com hash forte, bloqueio por tentativas e permissões por função.
- **Backup:** backup diário automático, backup manual e restauração testável.

---

## 4) Priorização sugerida (MVP)

1. Cadastro base (pessoas, produtos e tabelas auxiliares)
2. Estoque + vendas + caixa (ciclo operacional mínimo)
3. Financeiro integrado (contas a pagar/receber)
4. Relatórios essenciais e dashboard
5. Auditoria, permissões e backup completo
6. Fiscal e integrações externas como módulo plugável

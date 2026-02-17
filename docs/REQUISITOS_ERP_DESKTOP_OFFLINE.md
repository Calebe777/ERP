# Documento de Requisitos — ERP Comercial Completo

## 1) Visão geral

Sistema ERP destinado a:
- Comércio varejista
- Atacado
- Loja física (PDV)
- Delivery
- Prestação de serviços
- Pequenas e médias empresas

**Objetivo:** centralizar cadastro, estoque, compras, vendas, fiscal e financeiro em uma única plataforma integrada.

---

## 2) Módulos do sistema

### 2.1 Módulo Cadastro

#### 2.1.1 Cadastro de Pessoas
Tipos:
- Clientes
- Fornecedores
- Funcionários
- Transportadoras
- Vendedores
- Motoristas

Campos obrigatórios:
- Nome / Razão social
- CPF/CNPJ
- RG/IE
- Endereço completo
- Telefones
- E-mail
- Limite de crédito
- Data de nascimento
- Situação (ativo/inativo)
- Observações

#### 2.1.2 Cadastro de Produtos
- Código interno
- Código de barras
- Descrição
- Categoria / Grupo
- Marca
- Unidade de medida
- NCM
- CEST
- CFOP padrão
- Preço de custo
- Preço de venda
- Estoque atual
- Estoque mínimo
- Peso
- Localização no estoque
- Produto ativo/inativo

#### 2.1.3 Outros Cadastros
- Formas de pagamento
- Plano de contas
- Bancos e contas
- Tabela de preço
- Categorias de produtos
- Marcas
- Unidades
- Centro de custo

### 2.2 Módulo Estoque

#### 2.2.1 Controle de Estoque
- Entrada de mercadoria
- Saída de mercadoria
- Ajuste manual
- Transferência entre depósitos
- Controle por lote
- Controle por validade
- Controle por número de série

#### 2.2.2 Inventário
- Inventário geral
- Inventário parcial
- Correção automática de divergências

#### 2.2.3 Relatórios
- Estoque atual
- Estoque mínimo
- Produtos sem giro
- Curva ABC
- Histórico de movimentação
- Produtos mais vendidos

### 2.3 Módulo Compras
- Pedido de compra
- Cotação com fornecedores
- Importação de XML
- Geração automática de contas a pagar
- Entrada automática no estoque
- Devolução de compra
- Relatório de compras por fornecedor
- Controle de pedidos pendentes

### 2.4 Módulo Vendas / Movimento

#### 2.4.1 Orçamento
- Criar orçamento
- Validade
- Conversão em venda
- Impressão PDF

#### 2.4.2 Pedido de Venda
- Venda faturada
- Venda para entrega futura
- Venda com múltiplas formas de pagamento

#### 2.4.3 PDV (Ponto de Venda)
- Venda rápida
- Leitor de código de barras
- Aplicar desconto
- Cancelamento de item
- Cancelamento de venda
- Sangria
- Suprimento
- Fechamento de caixa
- Controle por operador

#### 2.4.4 Delivery / Restaurante
- Controle por mesa
- Comandas
- Taxa de entrega
- Status do pedido
- Integração com impressora de cozinha

### 2.5 Módulo Fiscal

#### 2.5.1 Emissão de Documentos
- NF-e
- NFC-e
- NFS-e
- CTe
- MDFe

#### 2.5.2 Funções Fiscais
- Importação XML
- Cancelamento
- Carta de correção
- Inutilização de número
- SPED Fiscal
- SPED Contribuições
- Sintegra
- Inventário fiscal

#### 2.5.3 Impostos
- ICMS
- IPI
- PIS
- COFINS
- CST/CSOSN
- Simples Nacional
- Regime Normal

### 2.6 Módulo Financeiro

#### 2.6.1 Contas a Receber
- Parcelamento
- Juros e multa
- Baixa manual
- Baixa automática
- Geração de boleto
- Relatório de inadimplência

#### 2.6.2 Contas a Pagar
- Parcelamento
- Controle por fornecedor
- Pagamento parcial
- Fluxo de caixa previsto

#### 2.6.3 Caixa
- Abertura
- Fechamento
- Conferência por operador
- Resumo por forma de pagamento

#### 2.6.4 Relatórios Financeiros
- Fluxo de caixa
- DRE
- Resumo financeiro mensal
- Lucro por período
- Despesas por categoria

### 2.7 Módulo Relatórios e Dashboard
- Vendas por período
- Vendas por vendedor
- Produtos mais vendidos
- Margem de lucro
- Ticket médio
- Ranking de clientes
- Gráficos comparativos
- Indicadores (KPIs)

### 2.8 Módulo Administração

#### 2.8.1 Usuários
- Cadastro de usuários
- Permissões por módulo
- Nível de acesso
- Log de atividades

#### 2.8.2 Configurações
- Dados da empresa
- Certificado digital
- Impressoras
- Formas de pagamento
- Backup automático
- Multiempresa
- Multiusuário

### 2.9 Automações e Integrações
- Envio automático de cobrança via WhatsApp
- Integração com gateway de pagamento
- API para integração externa
- Integração com marketplace
- Backup em nuvem
- Notificação de estoque baixo

### 2.10 Diferenciais modernos
- Sistema web (módulo futuro)
- Responsivo (celular)
- Dashboard em tempo real
- Controle de permissões avançado
- Atualização automática
- Criptografia de dados
- Adequação à LGPD

---

## 3) Requisitos técnicos
- Banco de dados relacional (SQLite no desktop atual; PostgreSQL/MySQL em arquitetura servidor)
- Backend com API REST (para integração e expansão futura)
- Frontend desktop atual e possibilidade de frontend web
- Autenticação segura (hash de senha e sessão; JWT em APIs)
- Controle de sessões
- Logs de auditoria

---

## 4) Resumo
Seu ERP deve conter:
- Cadastro completo
- Controle total de estoque
- Vendas e PDV
- Fiscal completo
- Financeiro integrado
- Relatórios gerenciais
- Controle de usuários
- Integrações e automações

> Observação de escopo: este documento define o alvo completo do produto. A implementação pode ser entregue por fases (MVP + evoluções).

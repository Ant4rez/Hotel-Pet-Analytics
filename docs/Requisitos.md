

# Requisitos do Projeto de Gestão de Hotel para Pets

## 1. Introdução

### 1.1 Objetivo
Este documento especifica os requisitos funcionais e não-funcionais do sistema de gestão de hotel para pets, que gerencia clientes, pets, reservas, serviços e transações financeiras.

### 1.2 Escopo
O sistema suporta o cadastro de clientes e pets, gerenciamento de reservas e quartos, agendamento de serviços, processamento de pagamentos e geração de relatórios.

## 2. Requisitos Funcionais (RF)

### 2.1 Gestão de Clientes e Pets

| ID   | Requisito Funcional     | Descrição                                                    | Relacionado a                    |
|------|-------------------------|--------------------------------------------------------------|----------------------------------|
| RF01 | Cadastro de clientes    | Sistema deve permitir cadastro de tutores com dados completos | Tabela cliente                   |
| RF02 | Vínculo pet-cliente     | Associar múltiplos pets a um mesmo tutor                     | Relacionamento CLIENTE 1:N PET   |
| RF03 | Controle vacinal        | Registrar e alertar sobre status vacinal dos pets            | Atributo pet.vacinas_em_dia      |
| RF04 | Histórico de pets       | Visualizar todos os pets de um cliente                       | Relacionamento CLIENTE → PET     |

### 2.2 Gestão de Reservas e Hospedagem

| ID   | Requisito Funcional          | Descrição                                                    | Relacionado a                |
|------|------------------------------|--------------------------------------------------------------|------------------------------|
| RF05 | Reserva de quartos           | Alocar pets em quartos por período específico                | Tabela reserva               |
| RF06 | Controle diárias             | Calcular valor total com base em quarto.preco_diaria e dias  | Atributos reserva + quarto   |
| RF07 | Verificação disponibilidade  | Impedir reservas conflitantes para mesmo quarto              | Restrição reserva.status     |
| RF08 | Check-in/out                 | Atualizar status de reserva e quarto automaticamente         | ENUM status_reserva_enum     |

### 2.3 Gestão de Serviços

| ID   | Requisito Funcional          | Descrição                                                    | Relacionado a                    |
|------|------------------------------|--------------------------------------------------------------|----------------------------------|
| RF09 | Catálogo de serviços         | Manter lista de serviços com preços fixos                    | Tabela tipo_servico              |
| RF10 | Agendamento de serviços      | Vincular múltiplos serviços a uma reserva                    | Relacionamento RESERVA 1:N SERVICO|
| RF11 | Alocação de funcionários     | Designar profissional específico para cada serviço           | Atributo servico.funcionario_id  |
| RF12 | Controle tempo serviço       | Validar duração com tipo_servico.duracao_media               | CHECK servico.fim > inicio       |

### 2.4 Financeiro

| ID   | Requisito Funcional          | Descrição                                                    | Relacionado a                    |
|------|------------------------------|--------------------------------------------------------------|----------------------------------|
| RF13 | Registro de pagamentos       | Registrar múltiplas formas de pagamento por reserva          | Tabela pagamento                 |
| RF14 | Cálculo automático           | Calcular valor total (hospedagem + serviços)                 | Atributos relacionados           |
| RF15 | Controle de status           | Atualizar status de pagamentos e reservas                    | ENUM status_pagamento_enum       |
| RF16 | Estornos                     | Gerenciar reembolsos com histórico                           | status_pagamento_enum = 'Estornado' |

### 2.5 Relatórios

| ID   | Requisito Funcional          | Descrição                                                    | Relacionado a                    |
|------|------------------------------|--------------------------------------------------------------|----------------------------------|
| RF17 | Ocupação de quartos          | Gerar relatório de utilização por período                    | Tabelas quarto + reserva         |
| RF18 | Serviços realizados          | Relatório por funcionário/tipo/período                       | Tabelas servico + funcionario    |
| RF19 | Faturamento                  | Consolidar receitas por categoria (hospedagem/serviços)      | Tabelas pagamento + reserva      |
| RF20 | Clientes frequentes          | Identificar melhores clientes por valor gasto                | JOIN cliente→pet→reserva→pagamento |

## 3. Requisitos Não-Funcionais (RNF)

### 3.1 Desempenho e Escalabilidade

| ID    | Requisito Não-Funcional | Descrição                                                    | Justificativa                    |
|-------|-------------------------|--------------------------------------------------------------|----------------------------------|
| RNF01 | Tempo de resposta       | Consultas devem retornar em < 2s mesmo com 50k registros     | Índices em FKs e campos de busca |
| RNF02 | Carga de pico           | Suportar 50 usuários simultâneos                             | Arquitetura escalável            |
| RNF03 | Crescimento de dados    | Modelo deve suportar 5 anos de dados históricos              | Tipos de dados adequados         |

### 3.2 Segurança e Confiabilidade

| ID    | Requisito Não-Funcional | Descrição                                                    | Justificativa                    |
|-------|-------------------------|--------------------------------------------------------------|----------------------------------|
| RNF04 | Integridade dos dados   | Garantir consistência transacional em operações críticas     | ON DELETE CASCADE e transações ACID |
| RNF05 | Backup automático       | Backups diários com retenção de 7 dias                       | Prevenção contra perda de dados  |
| RNF06 | Criptografia            | Dados sensíveis (pagamentos) criptografados                  | LGPD e segurança financeira      |

### 3.3 Usabilidade e Manutenibilidade

| ID    | Requisito Não-Funcional | Descrição                                                    | Justificativa                    |
|-------|-------------------------|--------------------------------------------------------------|----------------------------------|
| RNF07 | Interface intuitiva     | Usuários devem realizar operações com ≤ 3 cliques            | Modelo bem normalizado facilita UI|
| RNF08 | Documentação            | Documentação completa do modelo e regras                     | Dicionário de dados detalhado    |
| RNF09 | Atualizações            | Permitir alteração de ENUMs sem recriar tabelas              | Uso de tipos customizados        |

### 3.4 Integração e Compatibilidade

| ID    | Requisito Não-Funcional | Descrição                                                    | Justificativa                    |
|-------|-------------------------|--------------------------------------------------------------|----------------------------------|
| RNF10 | API REST                | Fornecer endpoints para integração com outros sistemas       | Relacionamentos bem definidos facilitam APIs |
| RNF11 | Multiplataforma         | Funcionar em Windows/Linux para banco de dados               | Uso de PostgreSQL compatível     |
| RNF12 | Formato de datas        | Suportar ISO 8601 para integrações                           | Tipo TIMESTAMP adequado          |

## 4. Mapa de Relacionamento RF-RNF

| Requisito Funcional           | Requisitos Não-Funcionais Relacionados         |
|-------------------------------|-----------------------------------------------|
| RF05 (Reserva de quartos)     | RNF01 (Desempenho), RNF04 (Integridade)       |
| RF10 (Agendamento serviços)   | RNF07 (Usabilidade), RNF10 (API)              |
| RF13 (Registro pagamentos)    | RNF06 (Criptografia), RNF12 (Formatos)        |
| RF17 (Relatórios)             | RNF01 (Desempenho), RNF03 (Crescimento)       |


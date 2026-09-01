# 🐾 Pet Hotel Analytics & ML Platform

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Evolu%C3%A7%C3%A3o%20Ativa-success?style=for-the-badge&logo=git" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql" alt="MySQL">
  <img src="https://img.shields.io/badge/Apache%20Airflow-2.8%2B-teal?style=for-the-badge&logo=apacheairflow" alt="Airflow">
  <img src="https://img.shields.io/badge/Apache%20Spark-PySpark-red?style=for-the-badge&logo=apachespark" alt="Spark">
  <img src="https://img.shields.io/badge/Databricks-Lakehouse-blueviolet?style=for-the-badge&logo=databricks" alt="Databricks">
  <img src="https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?style=for-the-badge&logo=scikitlearn" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Docker-Containers-blue?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## 📌 Sumário
* [📖 Sobre o Projeto](#-sobre-o-projeto)
* [🌱 Origem & Evolução: Da Sala de Aula ao Mundo Real](#-origem--evolu%C3%A7%C3%A3o-da-sala-de-aula-ao-mundo-real)
* [🏛️ Arquitetura de Dados de Ponta a Ponta](#️-arquitetura-de-dados-de-ponta-a-ponta)
* [📊 Estado Atual vs. Visão Futura](#-estado-atual-vs-vis%C3%A3o-futura)
* [🏅 Arquitetura Medallion no Databricks](#-arquitetura-medallion-no-databricks)
* [🤖 Ciência de Dados & Machine Learning](#-ci%C3%AAncia-de-dados--machine-learning)
* [🛡️ Governança & Data Quality](#️-governan%C3%A7a--data-quality)
* [🗺️ Roadmap de Desenvolvimento](#️-roadmap-de-desenvolvimento)
* [📁 Estrutura de Diretórios](#-estrutura-de-diret%C3%B3rios)
* [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
* [👨‍💻 Autor & Créditos](#-autor--cr%C3%A9ditos)

---

## 📖 Sobre o Projeto

O **Pet Hotel Analytics & ML Platform** é uma plataforma moderna e completa de **Engenharia e Ciência de Dados** voltada para o setor de hotelaria e bem-estar animal.

O ecossistema integra desde o **banco de dados transacional (OLTP)** de um hotel para pets até um **Data Lakehouse distribuído** com orquestração automatizada, validação de qualidade de dados contínua e modelos preditivos de **Machine Learning** para tomada de decisão estratégica de negócio.

### 🎯 Desafios de Negócio Endereçados:
1. **Operação e Gestão**: Controle completo de cadastros, quartos, estadias, serviços veterinários/estética e faturamento.
2. **Engenharia de Dados em Escala**: Ingestão contínua e processamento distribuído de dados históricos com garantia de integridade e linhagem.
3. **Inteligência Preditiva**: Redução de perda de receita com previsão antecipada de cancelamentos de reservas (*no-show*) e análise de sazonalidade de ocupação.

---

## 🌱 Origem & Evolução: Da Sala de Aula ao Mundo Real

> *"Grandes projetos nascem de ideias sólidas e crescem através da visão e dedicação contínua."*

Este projeto teve seu ponto de partida como um trabalho acadêmico em um curso de **Administração de Banco de Dados (DBA)**, desenvolvido originalmente em grupo por 4 alunos para entrega e avaliação curricular.

A fundação do projeto — que inclui a modelagem conceitual (MER), criação dos esquemas relacionais normalizados em MySQL, regras de negócio e dicionário de dados — foi desenhada e estruturada pelo autor deste repositório como parte daquela entrega original.

### 🚀 A Nova Fase: Construindo um Pipeline Enterprise
Com o curso concluído com sucesso, o projeto foi desacoplado da sua versão acadêmica e assumido como um **projeto autoral contínuo de Engenharia e Ciência de Dados**. O objetivo nesta nova jornada é elevar a arquitetura ao padrão ouro de mercado (*production-ready*), incorporando as ferramentas e práticas mais modernas utilizadas por times de dados em escala global.

---

## 🏛️ Arquitetura de Dados de Ponta a Ponta

A arquitetura do projeto conecta o mundo transacional à inteligência preditiva através de um fluxo moderno e desacoplado:

```mermaid
flowchart TD
    subgraph SOURCELAYER ["1. Camada Fonte Transacional (OLTP)"]
        DB[(MySQL Database\nHotel Pet)]
        SEED["Python Data Generator\n(Simulador de volume e sazonalidade)"]
        SEED -->|Popula com escala| DB
    end

    subgraph ORCHESTRATION ["Orquestração Automatizada (Apache Airflow)"]
        DAG_ETL["DAG: Ingestão & Processamento Medallion"]
        DAG_ML["DAG: Treinamento & Inferência Preditiva"]
    end

    subgraph MEDALLION ["2. Databricks Lakehouse (PySpark & Delta Lake)"]
        RAW[("Camada Raw / Bronze\n• Dados brutos append-only\n• Formato Delta/Parquet\n• Metadados de ingestão")]
        
        TRUSTED[("Camada Trusted / Silver\n• Dados limpos e deduplicados\n• Tipagem estrita e sem anomalias\n• Modelagem histórica")]
        
        REFINED[("Camada Refined / Gold\n• Modelagem Dimensional (Star Schema)\n• Fatos & Dimensões\n• Feature Store para ML")]

        DQ1{"Validação de Qualidade\n(Data Quality Check)"}
        DQ2{"Validação de Qualidade\n(Integridade & Schemas)"}
    end

    subgraph ML_SCIENCE ["3. Ciência de Dados (scikit-learn)"]
        FEAT["Feature Engineering\n(Comportamento do tutor, antecedência, etc.)"]
        TRAIN["Pipeline de Treinamento\n(Gradient Boosting / Random Forest)"]
        EVAL["Avaliação de Métricas\n(ROC-AUC, Precision, Recall, F1)"]
        REGISTRY[("Model Registry\n(joblib / MLflow)")]
        INFER["Batch Inference\n(Previsão de Cancelamento)"]
    end

    subgraph CONSUMPTION ["4. Consumo & Valor de Negócio"]
        BI["Analytics & Dashboards\n(Power BI / Streamlit)"]
        ALERTS["Ações Preventivas\n(Gestão de Ocupação)"]
    end

    %% Fluxos de Dados
    DB -->|Ingestão Python / JDBC| RAW
    RAW --> DQ1
    DQ1 -->|Aprovado| TRUSTED
    TRUSTED --> DQ2
    DQ2 -->|Aprovado| REFINED

    %% Orquestração
    DAG_ETL -.->|Controla| RAW
    DAG_ETL -.->|Dispara Jobs PySpark| TRUSTED
    DAG_ETL -.->|Dispara Jobs PySpark| REFINED
    DAG_ML -.->|Dispara Treinamento| ML_SCIENCE

    %% ML Flow
    REFINED --> FEAT --> TRAIN --> EVAL --> REGISTRY
    REGISTRY --> INFER
    REFINED --> INFER

    %% Consumo
    REFINED --> BI
    INFER --> ALERTS
```

---

## 📊 Estado Atual vs. Visão Futura

| Dimensão | Estado Atual (Legado DBA) | Nova Arquitetura (Em Construção) |
| :--- | :--- | :--- |
| **Foco Principal** | Banco de Dados Relacional e Consultas SQL | Pipeline de Dados End-to-End & Ciência de Dados |
| **Banco Transacional** | MySQL com dados de teste manuais (poucas linhas) | MySQL populado por gerador sintético em larga escala |
| **Ingestão** | Inexistente (manual via scripts SQL) | Scripts Python modulares e orquestrados |
| **Processamento** | Queries locais pontuais | Processamento distribuído no Databricks com PySpark |
| **Organização do Dado** | Tabelas relacionais 3FN | Arquitetura Medallion (Raw $\rightarrow$ Trusted $\rightarrow$ Refined) em Delta Lake |
| **Qualidade de Dados** | Apenas `CHECK` e constraints SQL | Framework automatizado de Data Quality com alertas |
| **Orquestração** | Execução manual | DAGs automatizadas no Apache Airflow com monitoramento |
| **Analytics & ML** | Nenhuma camada analítica | Modelo preditivo em `scikit-learn` para prevenção de *no-show* |
| **Ambiente de Dev** | Instalação local avulsa | Ambiente conteinerizado com Docker Compose |

---

## 🏅 Arquitetura Medallion no Databricks

O processamento no Databricks com PySpark divide as responsabilidades em 3 camadas lógicas:

1. **🥉 Camada Raw (Bronze)**:
   * Armazena os dados brutos exatamente como chegam da origem MySQL.
   * Estrutura imutável (*append-only*) no formato Delta Lake, preservando histórico e incluindo metadados (`_ingested_at`, `_source_file`).
2. **🥈 Camada Trusted (Silver)**:
   * Aplica limpeza e padronização: tratamento de valores ausentes, correção de tipagem, remoção de duplicatas e conformidade com regras de negócio.
   * Tabelas limpas representando entidades de negócio confiáveis.
3. **🥇 Camada Refined (Gold)**:
   * Dados altamente agregados e modelados em esquema dimensional (**Star Schema** / Kimball).
   * Contém as tabelas **Fato** (`fato_reservas`, `fato_servicos`, `fato_pagamentos`) e **Dimensões** (`dim_cliente`, `dim_pet`, `dim_quarto`, `dim_tempo`, `dim_funcionario`), além de servir como **Feature Store** para os modelos de IA.

---

## 🤖 Ciência de Dados & Machine Learning

### Caso de Uso: *Previsão de Cancelamento de Reservas (No-Show)*
* **Problema**: O cancelamento tardio de reservas de quartos gera ociosidade inesperada, bloqueia clientes legítimos e reduz o faturamento do hotel.
* **Solução**: Modelo preditivo desenvolvido com **scikit-learn** que classifica a probabilidade de cancelamento de uma reserva no momento em que ela é criada.
* **Pipeline de ML**:
  * **Feature Engineering**: Cálculo de antecedência da reserva (dias entre reserva e check-in), histórico de estadias anteriores do tutor, espécie/porte do pet, valor total contratado, proporção de serviços adicionais (banho/tosa/veterinário) e forma de pagamento.
  * **Algoritmos**: Avaliação comparativa entre `RandomForestClassifier`, `HistGradientBoostingClassifier` e `LogisticRegression`.
  * **Métricas de Sucesso**: Foco em **F1-Score** e **ROC-AUC** para lidar com classes desbalanceadas.
  * **Inferência**: Geração periódica de *scores* de risco para que a equipe do hotel tome ações preventivas (confirmação por WhatsApp, solicitação de caução, etc.).

---

## 🛡️ Governança & Data Quality

A qualidade dos dados é tratada como requisito de primeira classe ao longo de todo o pipeline:
* **Validação de Schemas**: Garantia de que alterações na estrutura de tabelas do MySQL não quebrem o pipeline silenciosamente.
* **Regras de Integridade**: Verificações automáticas (ex: `data_saida > data_entrada`, `valor > 0`, unicidade de chaves, nulidade controlada).
* **Bloqueio de Propagação**: Em caso de falha em validações críticas na camada Silver, o pipeline interrompe a publicação na Gold e notifica o time de dados.

---

## 🗺️ Roadmap de Desenvolvimento

O projeto está estruturado em fases incrementais e bem definidas:

```
[✅] Fase 1: Modelagem Relacional & Schemas MySQL
 │   ├── Criação das tabelas relacionais (3FN)
 │   ├── Dicionário de dados e documentação MER/DER
 │   └── Scripts de teste de integridade e consultas base
 │
[⏳] Fase 2: Simulador de Dados & Infraestrutura Local
 │   ├── Criação de gerador de dados sintéticos em Python (Faker) com sazonalidade e histórico
 │   └── Configuração do ambiente conteinerizado (Docker Compose para Airflow e MySQL)
 │
[ ] Fase 3: Ingestão de Dados & Camada Raw (Bronze)
 │   ├── Módulo Python de extração do MySQL (Full & Incremental)
 │   └── Persistência no formato Delta Lake / Parquet com metadados
 │
[ ] Fase 4: Processamento Distribuído no Databricks (PySpark)
 │   ├── Pipeline Raw -> Trusted (Silver): limpeza e conformidade
 │   └── Pipeline Trusted -> Refined (Gold): modelagem dimensional (Star Schema)
 │
[ ] Fase 5: Validação Automatizada de Qualidade (Data Quality)
 │   └── Implementação de suítes de validação de schemas, nulos e limites de negócio
 │
[ ] Fase 6: Pipeline de Machine Learning (scikit-learn)
 │   ├── Feature Store e pipeline de pré-processamento
 │   ├── Treinamento e tuning do modelo de previsão de cancelamento
 │   └── Exportação e rotina de inferência preditiva em lote
 │
[ ] Fase 7: Orquestração com Apache Airflow & Dashboards
     ├── Construção das DAGs de orquestração end-to-end com monitoramento
     └── Dashboard analítico com métricas de negócio e predições
```

---

## 📁 Estrutura de Diretórios

```text
hotel-pet-analytics/
├── .github/
│   └── workflows/              # Pipelines de CI/CD (lint, testes)
├── config/                     # Configurações de conexão e parâmetros
│   ├── airflow.cfg
│   └── pipeline_config.yaml
├── dags/                       # Definição das DAGs do Apache Airflow
│   ├── dag_medallion_pipeline.py
│   └── dag_ml_predictive_pipeline.py
├── data_generator/             # Simulador de dados sintéticos em larga escala
│   └── generate_synthetic_data.py
├── database/                   # Modelagem e scripts SQL relacionais (MySQL)
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_insert_sample_data.sql
│   └── 04_test_reserva.sql
├── docker/                     # Docker Compose e Dockerfiles
│   ├── docker-compose.yml
│   └── Dockerfile.airflow
├── docs/                       # Documentação técnica, dicionário e diagramas
│   ├── Dicionario.md
│   ├── MER.png
│   └── Requisitos.md
├── src/                        # Código-fonte dos módulos da aplicação
│   ├── ingestion/              # Conectores e extração MySQL -> Raw
│   │   ├── __init__.py
│   │   └── mysql_extractor.py
│   ├── pyspark_jobs/           # Jobs distribuídos do Databricks / Spark
│   │   ├── raw_to_trusted.py
│   │   └── trusted_to_refined.py
│   ├── quality/                # Suíte de Data Quality e validações
│   │   ├── __init__.py
│   │   └── data_validator.py
│   └── ml/                     # Módulo de Ciência de Dados & Modelagem
│       ├── __init__.py
│       ├── features.py
│       ├── train.py
│       ├── evaluate.py
│       └── predict.py
├── tests/                      # Testes unitários e de integração (pytest)
│   ├── test_ingestion.py
│   ├── test_pyspark_jobs.py
│   └── test_ml_pipeline.py
├── requirements.txt            # Dependências Python
├── LICENSE.md                  # Termos de licença MIT
└── README.md                   # Documentação principal
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* **MySQL 8.0+** (ou Docker instalado)
* **Python 3.10+**
* Cliente SQL (MySQL Workbench, DBeaver ou VS Code Database Client)

### 1. Inicializando o Banco de Dados Relacional
Para criar o banco de dados e as tabelas com as regras de negócio:
```bash
# Conecte-se ao seu servidor MySQL e execute os scripts na ordem:
mysql -u seu_usuario -p < database/01_create_database.sql
mysql -u seu_usuario -p hotel_pet < database/02_create_tables.sql
mysql -u seu_usuario -p hotel_pet < database/03_insert_sample_data.sql
```

### 2. Validando as Consultas Operacionais
Execute o script de teste para simular o fluxo de reserva, serviço e pagamento:
```bash
mysql -u seu_usuario -p hotel_pet < database/04_test_reserva.sql
```

*(Instruções para inicialização do Docker Compose, Apache Airflow e Jobs Databricks serão adicionadas conforme o avanço das próximas fases do Roadmap).*

---

## 👨‍💻 Autor & Créditos

Este projeto é desenvolvido e mantido por **Thiago** como iniciativa de portfólio avançado em Engenharia e Ciência de Dados.

> **Reconhecimento Acadêmico**: A estrutura inicial do banco de dados relacional (esquema transacional) foi desenvolvida colaborativamente durante o curso de Administrador de Banco de Dados com os colegas de turma, servindo de base sólida para esta expansão analítica.

<p align="center">
  <i>"Tudo quanto fizerem, façam de todo o coração, como para o Senhor, e não para homens." – Colossenses 3:23</i>
</p>

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE.md](LICENSE.md) para obter mais detalhes.


# Dicionário de Dados

## Tabela: cliente

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| nome          | VARCHAR(100)  | Nome do cliente        | NOT NULL            |
| telefone      | VARCHAR(20)   | Contato principal      | NOT NULL, UNIQUE    |
| email         | VARCHAR(100)  | E-mail                 | UNIQUE              |

## Tabela: pet

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| nome          | VARCHAR(50)   | Nome do pet            | NOT NULL            |
| especie       | VARCHAR(50)   | Cão, gato, etc.        | NOT NULL            |
| porte         | ENUM('P','M','G') | Porte do animal     | NOT NULL            |
| vacinas_em_dia | BOOLEAN      | Vacinação atualizada?  | DEFAULT FALSE       |
| cliente_id    | INT           | Dono do pet            | FK (cliente.id), NOT NULL |

## Tabela: reserva

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| data_entrada  | DATE          | Data de check-in       | NOT NULL            |
| data_saida    | DATE          | Data de check-out      | NOT NULL, > data_entrada |
| status        | ENUM('Confirmada','Ativa','Concluída','Cancelada') | Status da reserva | NOT NULL            |
| pet_id        | INT           | Pet hospedado          | FK (pet.id), NOT NULL |
| quarto_id     | INT           | Quarto alocado         | FK (quarto.id), NOT NULL |

## Tabela: quarto

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| numero        | VARCHAR(10)   | Número do quarto       | NOT NULL, UNIQUE    |
| tipo          | ENUM('Standard','Luxo') | Categoria do quarto | NOT NULL            |
| preco_diaria  | DECIMAL(10,2) | Valor da diária        | NOT NULL, > 0       |
| status        | ENUM('Disponível','Ocupado','Manutenção') | Status do quarto | NOT NULL            |

## Tabela: servico

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| reserva_id    | INT           | Reserva associada      | FK (reserva.id), NOT NULL |
| tipo_id       | INT           | Tipo de serviço (catálogo) | FK (tipo_servico.id), NOT NULL |
| funcionario_id | INT           | Funcionário responsável | FK (funcionario.id) |
| inicio        | TIMESTAMP     | Início do serviço      | NOT NULL            |
| fim           | TIMESTAMP     | Fim do serviço         | NOT NULL, > inicio  |
| status        | ENUM('Agendado','Em andamento','Concluído','Cancelado') | Status do serviço | NOT NULL            |

## Tabela: tipo_servico

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| nome          | VARCHAR(50)   | Nome do serviço (ex: 'Banho') | NOT NULL, UNIQUE    |
| preco         | DECIMAL(10,2) | Preço base             | NOT NULL, > 0       |
| duracao_media | INT           | Duração em minutos     | NOT NULL, > 0       |

## Tabela: funcionario

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| nome          | VARCHAR(100)  | Nome completo          | NOT NULL            |
| funcao_id     | INT           | Função no hotel        | FK (funcao.id), NOT NULL |

## Tabela: funcao

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| nome          | VARCHAR(50)   | Nome da função (ex: 'Tosador') | NOT NULL, UNIQUE    |

## Tabela: pagamento

| Atributo      | Tipo          | Descrição              | Restrições          |
|---------------|---------------|------------------------|---------------------|
| id            | SERIAL        | Chave primária         | PK, NOT NULL        |
| reserva_id    | INT           | Reserva associada      | FK (reserva.id), NOT NULL |
| valor         | DECIMAL(10,2) | Valor pago             | NOT NULL, > 0       |
| metodo        | ENUM('Cartão','PIX','Dinheiro') | Método de pagamento | NOT NULL            |
| status        | ENUM('Pendente','Concluído','Estornado') | Status do pagamento |                     |
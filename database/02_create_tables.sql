-- Tabelas --

-- Tabela: cliente
CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE
);

-- Tabela: funcao
CREATE TABLE funcao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Tabela: tipo_servico
CREATE TABLE tipo_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    preco DECIMAL(10,2) NOT NULL CHECK (preco > 0),
    duracao_media INT NOT NULL CHECK (duracao_media > 0)
);

-- Tabela: quarto
CREATE TABLE quarto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) NOT NULL UNIQUE,
    tipo ENUM('Standard', 'Luxo') NOT NULL,
    preco_diaria DECIMAL(10,2) NOT NULL CHECK (preco_diaria > 0),
    status ENUM('Disponível', 'Ocupado', 'Manutenção') NOT NULL
);

-- Tabela: pet
CREATE TABLE pet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    porte ENUM('P', 'M', 'G') NOT NULL,
    vacinas_em_dia BOOLEAN DEFAULT FALSE,
    cliente_id INT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE CASCADE
);

-- Tabela: funcionario
CREATE TABLE funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    funcao_id INT NOT NULL,
    FOREIGN KEY (funcao_id) REFERENCES funcao(id) ON DELETE CASCADE
);

-- Tabela: reserva
CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_entrada DATE NOT NULL,
    data_saida DATE NOT NULL,
    status ENUM('Confirmada', 'Ativa', 'Concluída', 'Cancelada') NOT NULL,
    pet_id INT NOT NULL,
    quarto_id INT NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE,
    FOREIGN KEY (quarto_id) REFERENCES quarto(id) ON DELETE CASCADE,
    CHECK (data_saida > data_entrada)
);

-- Tabela: servico
CREATE TABLE servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    tipo_id INT NOT NULL,
    funcionario_id INT,
    inicio DATETIME NOT NULL,
    fim DATETIME NOT NULL,
    status ENUM('Agendado', 'Em andamento', 'Concluído', 'Cancelado') NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES reserva(id) ON DELETE CASCADE,
    FOREIGN KEY (tipo_id) REFERENCES tipo_servico(id) ON DELETE CASCADE,
    FOREIGN KEY (funcionario_id) REFERENCES funcionario(id) ON DELETE SET NULL,
    CHECK (fim > inicio)
);

-- Tabela: pagamento
CREATE TABLE pagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL CHECK (valor > 0),
    metodo ENUM('Cartão', 'PIX', 'Dinheiro') NOT NULL,
    status ENUM('Pendente', 'Concluído', 'Estornado') DEFAULT 'Pendente',
    FOREIGN KEY (reserva_id) REFERENCES reserva(id) ON DELETE CASCADE
);
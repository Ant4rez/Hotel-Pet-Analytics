-- Dados Iniciais para Testes

-- Inserindo funções
INSERT INTO funcao (nome) VALUES 
('Veterinário'),
('Tosador'),
('Recepcionista');

-- Inserindo tipos de serviços
INSERT INTO tipo_servico (nome, preco, duracao_media) VALUES
('Banho', 50.00, 60),
('Tosa', 70.00, 90),
('Consulta Veterinária', 100.00, 30);

-- Inserindo quartos
INSERT INTO quarto (numero, tipo, preco_diaria, status) VALUES
('101', 'Standard', 100.00, 'Disponível'),
('102', 'Luxo', 150.00, 'Disponível'),
('201', 'Standard', 100.00, 'Disponível');

-- Inserindo clientes
INSERT INTO cliente (nome, telefone, email) VALUES
('John Doe', '123456789', 'john@example.com'),
('Jane Smith', '987654321', 'jane@example.com');

-- Inserindo pets
INSERT INTO pet (nome, especie, porte, vacinas_em_dia, cliente_id) VALUES
('Max', 'Cão', 'M', TRUE, 1),
('Bella', 'Gato', 'P', FALSE, 1),
('Luna', 'Cão', 'G', TRUE, 2),
('Simba', 'Gato', 'P', TRUE, 2);

-- Inserindo funcionários
INSERT INTO funcionario (nome, funcao_id) VALUES
('Maria Souza', 1),  -- Veterinário
('Pedro Silva', 2),  -- Tosador
('Ana Oliveira', 3); -- Recepcionista

-- Inserindo reservas
INSERT INTO reserva (data_entrada, data_saida, status, pet_id, quarto_id) VALUES
('2025-07-22', '2025-07-24', 'Confirmada', 1, 1),  -- Max no quarto 101
('2025-07-23', '2025-07-25', 'Confirmada', 3, 2); -- Luna no quarto 102

-- Inserindo serviços
INSERT INTO servico (reserva_id, tipo_id, funcionario_id, inicio, fim, status) VALUES
(1, 1, 2, '2025-07-23 10:00:00', '2025-07-23 11:00:00', 'Concluído'), -- Banho para Max por Pedro
(2, 3, 1, '2025-07-24 14:00:00', '2025-07-24 14:30:00', 'Concluído'); -- Consulta para Luna por Maria

-- Inserindo pagamentos
INSERT INTO pagamento (reserva_id, valor, metodo, status) VALUES
(1, 250.00, 'Cartão', 'Concluído'), -- Total: 2 dias * 100 (quarto) + 50 (banho)
(2, 400.00, 'PIX', 'Concluído');    -- Total: 2 dias * 150 (quarto) + 100 (consulta)

-- Fiz umas atualizaçoes ai cachorro

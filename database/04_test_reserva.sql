-- Simulação de uma Nova Reserva

-- Passo 1: Verificar disponibilidade do quarto (exemplo para quarto 101)
-- Esta consulta verifica se há reservas conflitantes para o quarto 101 entre 2025-08-01 e 2025-08-03
SELECT COUNT(*) AS conflitos
FROM reserva
WHERE quarto_id = 1
AND status != 'Cancelada'
AND (
    (data_entrada <= '2025-08-03' AND data_saida >= '2025-08-01')
);

-- Passo 2: Inserir uma nova reserva (assumindo que a consulta acima retornou 0 conflitos)
INSERT INTO reserva (data_entrada, data_saida, status, pet_id, quarto_id)
VALUES ('2025-08-01', '2025-08-03', 'Confirmada', 2, 1); -- Reserva para Bella (pet_id 2) no quarto 101

-- Passo 3: Inserir um serviço para a reserva
INSERT INTO servico (reserva_id, tipo_id, funcionario_id, inicio, fim, status)
VALUES (LAST_INSERT_ID(), 2, 2, '2025-08-02 09:00:00', '2025-08-02 10:30:00', 'Agendado'); -- Tosa por Pedro

-- Passo 4: Inserir um pagamento para a reserva
-- Valor total: 2 dias * 100 (quarto) + 70 (tosa) = 270
INSERT INTO pagamento (reserva_id, valor, metodo, status)
VALUES (LAST_INSERT_ID() - 1, 270.00, 'Cartão', 'Pendente');

-- Passo 5: Verificar o resultado da reserva
SELECT 
    r.id AS reserva_id,
    p.nome AS pet_nome,
    q.numero AS quarto_numero,
    r.data_entrada,
    r.data_saida,
    s.nome AS servico_nome,
    pg.valor AS pagamento_valor
FROM reserva r
JOIN pet p ON r.pet_id = p.id
JOIN quarto q ON r.quarto_id = q.id
LEFT JOIN servico ser ON ser.reserva_id = r.id
LEFT JOIN tipo_servico s ON ser.tipo_id = s.id
LEFT JOIN pagamento pg ON pg.reserva_id = r.id
WHERE r.id = LAST_INSERT_ID() - 1;
INSERT INTO unidade_saude (nome, endereco, telefone, municipio, horario_funcionamento) VALUES
('UBS Fortaleza Central', 'Av 1, Fortaleza', '85911111111', 'Fortaleza', '07:00-17:00'),
('PSF Quixadá Norte', 'Rua B, Quixadá', '85922222222', 'Quixadá', '08:00-18:00'),
('UBS Ipueiras Leste', 'Rua C, Ipueiras', '85933333333', 'Ipueiras', '07:30-17:30'),
('PS Quixeramobim Oeste', 'Av D, Quixeramobim', '85944444444', 'Quixeramobim', '08:00-17:00'),
('UBS Mombaça', 'Rua E, Mombaça', '85955555555', 'Mombaça', '07:00-19:00'),
('UBS Iguatu Sul', 'Rua F, Iguatu', '85966666666', 'Iguatu', '08:00-17:00'),
('PSF Ipu', 'Rua G, Ipu', '85977777777', 'Ipu', '07:00-16:00'),
('UBS Quixadá Centro', 'Av H, Quixadá', '85988888888', 'Quixadá', '08:00-17:00'),
('Posto Fortaleza Sul', 'Rua I, Fortaleza', '85999999999', 'Fortaleza', '08:00-20:00'),
('UBS Ipu Centro', 'Rua J, Ipu', '85910101010', 'Ipu', '07:00-18:00');

INSERT INTO paciente (cpf, nome, email, data_nascimento, endereco, telefone, cartao_sus) VALUES
('11111111111', 'Gabriel Dias', 'gabriel.paciente@gmail.com', '1995-04-12', 'Rua A, Fortaleza', '85999999991', '12345678901'),
('22222222222', 'Veronica Agostinho', 'veronica.paciente@gamail.com', '1988-07-09', 'Av Central, Quixadá', '85999999992', '12345678902'),
('33333333333', 'Weslem Lira', 'weslem.paciente@gmail.com', '1992-01-23', 'Rua 10, Ipueiras', '85999999993', '12345678903'),
('44444444444', 'Gilmarque Rodrigues', 'gilmarque.paciente@gmail.com', '1979-03-17', 'Av Principal, Ipu', '85999999994', '12345678904'),
('55555555555', 'Riquellme Ferreira', 'riquellme.paciente@gmailample.com', '2000-12-01', 'Rua das Flores, Mombaça', '85999999995', '12345678905'),
('66666666666', 'Rosa Vale', 'rosa.paciente@gmail.com', '1990-10-10', 'Av Beira Mar, Iguatu', '85999999996', '12345678906'),
('77777777777', 'Itallo Cavalcante', 'italo.paciente@gmail.com', '1998-06-22', 'Rua Nova, Quixeramobim', '85999999997', '12345678907'),
('88888888888', 'Odete Roitman', 'odete.paciente@gmail.com', '1960-08-08', 'Rua Paz, Fortaleza', '85999999998', '12345678908'),
('99999999999', 'Leona Almeida', 'leona.paciente@gmail.com', '1982-11-25', 'Rua Esperança, Quixadá', '85999999999', '12345678909'),
('10101010101', 'Marco Aurélio', 'marco.paciente@exgmailample.com', '1965-09-09', 'Rua do Centro, Ipu', '85999999990', '12345678910');

INSERT INTO profissional_saude (cpf, nome, email, data_nascimento, endereco, telefone, registro_profissional, funcao, unidade_id) VALUES
('12121212121', 'Solange Duprah', 'solang@saude.gov', '1990-01-01', 'Rua A, Fortaleza', '85988888881', 'REG123', 'Enfermeiro', 1),
('13131313131', 'Carmen Lucia', 'carminha@saude.gov', '1985-02-02', 'Av Central, Quixadá', '85988888882', 'REG124', 'Médica', 2),
('14141414141', 'Maria da Penha', 'penha@saude.gov', '1993-03-03', 'Rua 10, Ipueiras', '85988888883', 'REG125', 'Técnico', 3),
('15151515151', 'Flora Pereira', 'flora@saude.gov', '1980-04-04', 'Av Principal, Ipu', '85988888884', 'REG126', 'Médica', 4),
('16161616161', 'Maria de Fatima', 'fatima@saude.gov', '2001-05-05', 'Rua das Flores, Mombaça', '85988888885', 'REG127', 'Enfermeiro', 5),
('17171717171', 'Raquel Acioli', 'raquel@saude.gov', '1991-06-06', 'Av Beira Mar, Iguatu', '85988888886', 'REG128', 'Médica', 6),
('18181818181', 'Cesar Ribeiro', 'cesarribeiro@saude.gov', '1999-07-07', 'Rua Nova, Quixeramobim', '85988888887', 'REG129', 'Técnico', 7),
('19191919191', 'Celina Almeida', '.celyalmeida@saude.gov', '1960-08-08', 'Rua Paz, Fortaleza', '85988888888', 'REG130', 'Enfermeira', 1),
('20202020202', 'Sofia Teodora', 'Sofia@saude.gov', '1971-09-09', 'Rua Esperança, Quixadá', '85988888889', 'REG131', 'Médica', 2),
('21212121212', 'Fernanda Torres', 'fernanda.torres@saude.gov', '1983-10-10', 'Rua do Centro, Ipu', '85988888880', 'REG132', 'Técnico', 3);


INSERT INTO vacina (nome, numero_doses, fabricante, intervalo_doses) VALUES
('CoronaVac', 2, 'Sinovac', 28),
('Pfizer Bivalente', 2, 'Pfizer', 21),
('AstraZeneca', 2, 'Fiocruz', 90),
('Janssen', 1, 'Johnson & Johnson', 0),
('Moderna', 2, 'Moderna Inc.', 30),
('Hepatite B', 3, 'Butantan', 30),
('Tríplice Viral', 2, 'Fiocruz', 30),
('Influenza', 1, 'Sanofi', 0),
('Febre Amarela', 1, 'Bio-Manguinhos', 0),
('HPV', 2, 'MSD', 180);

INSERT INTO estoque_vacinas (lote, validade, quantidade, vacina_id, unidade_id) VALUES
('L001', '2025-12-01', 100, 1, 1),
('L002', '2025-11-15', 200, 2, 2),
('L003', '2025-10-10', 150, 3, 3),
('L004', '2026-01-01', 80, 4, 4),
('L005', '2025-09-09', 60, 5, 5),
('L006', '2025-08-08', 90, 6, 6),
('L007', '2025-07-07', 110, 7, 7),
('L008', '2025-06-06', 70, 8, 8),
('L009', '2025-05-05', 50, 9, 9),
('L010', '2025-04-04', 40, 10, 10);

INSERT INTO agendamento (data, horario, status, paciente_cpf, unidade_id) VALUES
('2025-08-01', '08:00:00', 'Agendado', '11111111111', 1),
('2025-08-02', '09:00:00', 'Compareceu', '22222222222', 2),
('2025-08-03', '10:00:00', 'Cancelado', '33333333333', 3),
('2025-08-04', '08:30:00', 'Agendado', '44444444444', 4),
('2025-08-05', '09:30:00', 'Compareceu', '55555555555', 5),
('2025-08-06', '10:30:00', 'Agendado', '66666666666', 6),
('2025-08-07', '08:00:00', 'Agendado', '77777777777', 7),
('2025-08-08', '09:00:00', 'Compareceu', '88888888888', 8),
('2025-08-09', '10:00:00', 'Agendado', '99999999999', 9),
('2025-08-10', '11:00:00', 'Compareceu', '10101010101', 10);

INSERT INTO aplicacao_vacina (data, dose, lote, paciente_cpf, unidade_id, profissional_cpf, vacina_id) VALUES
('2025-08-01', 1, 'L001', '11111111111', 1, '12121212121', 1),
('2025-08-02', 2, 'L002', '22222222222', 2, '13131313131', 2),
('2025-08-03', 1, 'L003', '33333333333', 3, '14141414141', 3),
('2025-08-04', 1, 'L004', '44444444444', 4, '15151515151', 4),
('2025-08-05', 2, 'L005', '55555555555', 5, '16161616161', 5),
('2025-08-06', 1, 'L006', '66666666666', 6, '17171717171', 6),
('2025-08-07', 2, 'L007', '77777777777', 7, '18181818181', 7),
('2025-08-08', 1, 'L008', '88888888888', 8, '19191919191', 8),
('2025-08-09', 1, 'L009', '99999999999', 9, '20202020202', 9),
('2025-08-10', 2, 'L010', '10101010101', 10, '21212121212', 10);

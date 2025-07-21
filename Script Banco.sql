CREATE TABLE pessoa (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    data_nascimento DATE,
    endereco TEXT,
    telefone VARCHAR(20)
    cartao_sus VARCHAR(20)
);

CREATE TABLE paciente (
) INHERITS (pessoa);

ALTER TABLE paciente
ADD CONSTRAINT paciente_pk PRIMARY KEY (cpf);

CREATE TABLE profissional_saude (
    registro_profissional VARCHAR(20),
    funcao VARCHAR(100),
    unidade_id INT
) INHERITS (pessoa);

ALTER TABLE profissional_saude
ADD CONSTRAINT profissional_saude_pk PRIMARY KEY (cpf);
CREATE TABLE unidade_saude (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco TEXT,
    telefone VARCHAR(20),
    municipio VARCHAR(100),
    horario_funcionamento VARCHAR(100)
);

ALTER TABLE profissional_saude
ADD CONSTRAINT fk_unidade_profissional FOREIGN KEY (unidade_id)
REFERENCES unidade_saude(id);

CREATE TABLE vacina (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    numero_doses INT,
    fabricante VARCHAR(100),
    intervalo_doses INT 
);

CREATE TABLE estoque_vacinas (
    id SERIAL PRIMARY KEY,
    lote VARCHAR(50),
    validade DATE,
    quantidade INT,
    vacina_id INT,
    unidade_id INT,
    CONSTRAINT fk_vacina_estoque FOREIGN KEY (vacina_id) REFERENCES vacina(id),
    CONSTRAINT fk_unidade_estoque FOREIGN KEY (unidade_id) REFERENCES unidade_saude(id)
);


CREATE TABLE aplicacao_vacina (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    dose INT,
    lote VARCHAR(50),
    paciente_cpf VARCHAR(11),
    unidade_id INT,
    profissional_cpf VARCHAR(11),
    vacina_id INT,

    CONSTRAINT fk_aplicacao_paciente FOREIGN KEY (paciente_cpf) REFERENCES paciente(cpf),
    CONSTRAINT fk_aplicacao_unidade FOREIGN KEY (unidade_id) REFERENCES unidade_saude(id),
    CONSTRAINT fk_aplicacao_profissional FOREIGN KEY (profissional_cpf) REFERENCES profissional_saude(cpf),
    CONSTRAINT fk_aplicacao_vacina FOREIGN KEY (vacina_id) REFERENCES vacina(id)
);
CREATE TABLE agendamento (
    id SERIAL PRIMARY KEY,
    data DATE,
    horario TIME,
    status VARCHAR(20),
    paciente_cpf VARCHAR(11),
    unidade_id INT,

    CONSTRAINT fk_agendamento_paciente FOREIGN KEY (paciente_cpf) REFERENCES paciente(cpf),
    CONSTRAINT fk_agendamento_unidade FOREIGN KEY (unidade_id) REFERENCES unidade_saude(id)
);

CREATE TABLE campanha (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    data_inicio DATE,
    data_fim DATE,
    publico_alvo TEXT,
     status VARCHAR(20),
    vacinas TEXT
);

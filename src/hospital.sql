DROP DATABASE IF EXISTS hospitamanager;

-- ============================================================
-- BANCO DE DADOS DO SISTEMA HOSPITALAR
-- ============================================================

CREATE DATABASE hospitamanager;
USE hospitamanager;

-- ============================================================
-- TABELA: pacientes
-- ============================================================

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    data_nascimento DATE,
    sexo ENUM('Masculino', 'Feminino', 'Outro') NOT NULL,
    telefone VARCHAR(20),
    telefone_emergencia VARCHAR(20),
    nome_responsavel VARCHAR(120),
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(30),
    alergias TEXT,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABELA: classificacao_urgencia
-- ============================================================

CREATE TABLE classificacao_urgencia (
    id_classificacao INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cor VARCHAR(15),
    prioridade INT NOT NULL
);

INSERT INTO classificacao_urgencia (nome, cor, prioridade) VALUES
('Nada urgente','Azul',1),
('Pouco urgente','Verde',2),
('Urgente','Amarelo',3),
('Muito urgente','Laranja',4),
('Emergência','Vermelho',5);

-- ============================================================
-- TABELA: setores
-- ============================================================

CREATE TABLE setores (
    id_setor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    descricao VARCHAR(255),
    localizacao VARCHAR(120)
);

INSERT INTO setores (nome, descricao, localizacao) VALUES
('Consultório', 'Atendimento clínico geral', '1º Andar - Bloco A'),
('Emergência', 'Atendimento crítico', 'Térreo - Bloco A'),
('Cirurgia', 'Salas cirúrgicas', 'Bloco C'),
('Recuperação Pós-Cirúrgica', 'Sala de recuperação', 'Bloco C'),
('Internação', 'Leitos de internação', 'Bloco F'),
('Maternidade', 'Atendimento obstétrico', 'Bloco G'),
('Pediatria', 'Atendimento infantil', 'Bloco H'),
('UTI', 'Terapia intensiva', 'Bloco D'),
('Medicação', 'Administração de fármacos', 'Bloco B'),
('Farmácia', 'Distribuição medicamentos', 'Bloco B'),
('Raio-X', 'Exames radiológicos', 'Bloco D'),
('Laboratório', 'Análises clínicas', 'Bloco E'),
('Fisioterapia', 'Reabilitação física', 'Bloco I'),
('Curativos', 'Cuidado de ferimentos', 'Bloco B'),
('Recepção de Exames', 'Entrega de exames', 'Bloco E'),
('Odontologia', 'Dentista', 'Bloco J'),
('Isolamento', 'Doenças infectocontagiosas', 'Bloco K'),
('Saúde Mental', 'Psiquiatria', 'Bloco L'),
('Observação', 'Pré-internação', 'Térreo - Bloco A');

-- ============================================================
-- TABELA: especialidades
-- ============================================================

CREATE TABLE especialidades (
    id_especialidade INT AUTO_INCREMENT PRIMARY KEY,
    especialidade VARCHAR(150) NOT NULL
);

INSERT INTO especialidades (especialidade) VALUES
('Clínico Geral'),('Cardiologia'),('Dermatologia'),('Endocrinologia'),
('Gastroenterologia'),('Geriatria'),('Ginecologia'),('Hematologia'),
('Infectologia'),('Nefrologia'),('Neurocirurgia'),('Neurologia'),
('Nutrologia'),('Obstetrícia'),('Oftalmologia'),('Oncologia'),
('Ortopedia'),('Otorrinolaringologia'),('Pediatria'),('Pneumologia'),
('Psiquiatria'),('Reumatologia'),('Urologia'),('Cirurgia Geral'),
('Cirurgia Plástica'),('Cirurgia Vascular'),('Fisioterapia'),
('Fonoaudiologia'),('Medicina do Trabalho'),('Medicina Esportiva'),
('Anestesiologia'),('Radiologia'),('Traumatologia');

-- ============================================================
-- TABELA: medicos
-- ============================================================

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome VARCHAR(120) NOT NULL,
    crm VARCHAR(20) NOT NULL UNIQUE,
    id_especialidade INT NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(120),
    horario_entrada TIME,
    horario_saida TIME,
    ativo BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_especialidade) REFERENCES especialidades(id_especialidade)
);

-- ============================================================
-- TABELA: usuarios (Admin, Médico, Enfermeiro, Recepção)
-- ============================================================

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    login VARCHAR(50) UNIQUE,
    senha_hash VARCHAR(255),
    tipo ENUM('Admin','Medico','Enfermeiro','Recepcao') NOT NULL
);

-- ============================================================
-- TABELA: triagem
-- ============================================================

CREATE TABLE triagem (
    id_triagem INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    pressao_arterial VARCHAR(20),
    frequencia_cardiaca INT,
    frequencia_respiratoria INT,
    saturacao DECIMAL(4,1),
    temperatura DECIMAL(4,1),
    dor_escala INT CHECK (dor_escala BETWEEN 0 AND 10),
    sintomas TEXT,
    historico TEXT,
    id_classificacao INT NOT NULL,
    id_setor INT NOT NULL,
    id_profissional INT NOT NULL,
    horario_chegada DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_classificacao) REFERENCES classificacao_urgencia(id_classificacao),
    FOREIGN KEY (id_setor) REFERENCES setores(id_setor),
    FOREIGN KEY (id_profissional) REFERENCES usuarios(id_usuario)
);

-- ============================================================
-- TABELA: atendimentos (MÉDICO)
-- ============================================================

CREATE TABLE atendimentos (
    id_atendimento INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    id_triagem INT NOT NULL,
    diagnostico TEXT,
    conduta TEXT,
    tipo_atendimento ENUM('Consulta','Emergência','Internação'),
    horario_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    horario_fim DATETIME,
    status ENUM('Em andamento','Finalizado','Cancelado') DEFAULT 'Em andamento',
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
    FOREIGN KEY (id_triagem) REFERENCES triagem(id_triagem)
);

-- ============================================================
-- TABELA: procedimentos (Enfermagem / Médico)
-- ============================================================

CREATE TABLE procedimentos (
    id_procedimento INT AUTO_INCREMENT PRIMARY KEY,
    id_atendimento INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    profissional VARCHAR(120),
    horario DATETIME DEFAULT CURRENT_TIMESTAMP,
    area ENUM('Enfermagem','Médico','Cirurgia','Outros'),
    FOREIGN KEY (id_atendimento) REFERENCES atendimentos(id_atendimento)
);
-- ============================================================
-- TABELA: recepcionistas
-- ============================================================
CREATE TABLE recepcionistas (
    id_recepcionista INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    ativo BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- ============================================================
-- TABELA: enfermeiros
-- ============================================================

CREATE TABLE enfermeiros (
    id_enfermeiro INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome VARCHAR(120) NOT NULL,
    coren VARCHAR(30) UNIQUE,
    ativo BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);


-- ============================================================
-- TABELA: medicações
-- ============================================================

CREATE TABLE medicacoes (
    id_medicacao INT AUTO_INCREMENT PRIMARY KEY,
    id_atendimento INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    dosagem VARCHAR(50),
    via_administracao ENUM('Oral','IV','IM','SC','Inalada','Outros'),
    intervalo_horas INT,
    observacoes TEXT,
    horario_aplicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_atendimento) REFERENCES atendimentos(id_atendimento)
);

-- ============================================================
-- TABELA: relatórios
-- ============================================================

CREATE TABLE relatorios (
    id_relatorio INT AUTO_INCREMENT PRIMARY KEY,
    id_atendimento INT NOT NULL,
    texto_relatorio LONGTEXT,
    medico_responsavel VARCHAR(120),
    gerado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_atendimento) REFERENCES atendimentos(id_atendimento)
);

-- ============================================================
-- TABELA: logs
-- ============================================================

CREATE TABLE logs_sistema (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(120),
    acao TEXT,
    horario DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- USUÁRIOS PADRÃO
-- ============================================================

INSERT INTO usuarios (nome, login, senha_hash, tipo) VALUES
('Administrador Geral','admin','admin123','Admin'),
('Dr. João Silva','drjoao','medico123','Medico'),
('Maria Santos','maria_enf','enfermeira123','Enfermeiro'),
('Paulo Souza','paulo_rec','recepcao123','Recepcao');

alter table medicos add column id_usuario INT NOT NULL;

alter table 
medicos add constraint fk_medicos_usuarios foreign key (id_usuario) references usuarios(id_usuario);


ALTER TABLE medicos DROP FOREIGN KEY medicos_ibfk_1;
alter table medicos drop COLUMN id_especialidade;

SHOW CREATE TABLE medicos;

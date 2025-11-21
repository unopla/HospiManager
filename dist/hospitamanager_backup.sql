-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: hospitamanager
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `hospitamanager`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `hospitamanager` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `hospitamanager`;

--
-- Table structure for table `atendimentos`
--

DROP TABLE IF EXISTS `atendimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `atendimentos` (
  `id_atendimento` int(11) NOT NULL AUTO_INCREMENT,
  `id_paciente` int(11) NOT NULL,
  `id_medico` int(11) NOT NULL,
  `id_triagem` int(11) NOT NULL,
  `diagnostico` text DEFAULT NULL,
  `conduta` text DEFAULT NULL,
  `tipo_atendimento` enum('Consulta','Emergência','Internação') DEFAULT NULL,
  `horario_inicio` datetime DEFAULT current_timestamp(),
  `horario_fim` datetime DEFAULT NULL,
  `status` enum('Em andamento','Finalizado','Cancelado') DEFAULT 'Em andamento',
  PRIMARY KEY (`id_atendimento`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_medico` (`id_medico`),
  KEY `id_triagem` (`id_triagem`),
  CONSTRAINT `atendimentos_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`),
  CONSTRAINT `atendimentos_ibfk_2` FOREIGN KEY (`id_medico`) REFERENCES `medicos` (`id_medico`),
  CONSTRAINT `atendimentos_ibfk_3` FOREIGN KEY (`id_triagem`) REFERENCES `triagem` (`id_triagem`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atendimentos`
--

LOCK TABLES `atendimentos` WRITE;
/*!40000 ALTER TABLE `atendimentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `atendimentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classificacao_urgencia`
--

DROP TABLE IF EXISTS `classificacao_urgencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classificacao_urgencia` (
  `id_classificacao` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `cor` varchar(15) DEFAULT NULL,
  `prioridade` int(11) NOT NULL,
  PRIMARY KEY (`id_classificacao`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classificacao_urgencia`
--

LOCK TABLES `classificacao_urgencia` WRITE;
/*!40000 ALTER TABLE `classificacao_urgencia` DISABLE KEYS */;
INSERT INTO `classificacao_urgencia` VALUES (1,'Nada urgente','Azul',1),(2,'Pouco urgente','Verde',2),(3,'Urgente','Amarelo',3),(4,'Muito urgente','Laranja',4),(5,'Emergência','Vermelho',5);
/*!40000 ALTER TABLE `classificacao_urgencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enfermeiros`
--

DROP TABLE IF EXISTS `enfermeiros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enfermeiros` (
  `id_enfermeiro` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(120) NOT NULL,
  `coren` varchar(30) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id_enfermeiro`),
  UNIQUE KEY `coren` (`coren`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `enfermeiros_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enfermeiros`
--

LOCK TABLES `enfermeiros` WRITE;
/*!40000 ALTER TABLE `enfermeiros` DISABLE KEYS */;
INSERT INTO `enfermeiros` VALUES (1,3,'Maria Santos','COREN0003',1);
/*!40000 ALTER TABLE `enfermeiros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicacoes`
--

DROP TABLE IF EXISTS `medicacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicacoes` (
  `id_medicacao` int(11) NOT NULL AUTO_INCREMENT,
  `id_atendimento` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `dosagem` varchar(50) DEFAULT NULL,
  `via_administracao` enum('Oral','IV','IM','SC','Inalada','Outros') DEFAULT NULL,
  `intervalo_horas` int(11) DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `horario_aplicacao` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_medicacao`),
  KEY `id_atendimento` (`id_atendimento`),
  CONSTRAINT `medicacoes_ibfk_1` FOREIGN KEY (`id_atendimento`) REFERENCES `atendimentos` (`id_atendimento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicacoes`
--

LOCK TABLES `medicacoes` WRITE;
/*!40000 ALTER TABLE `medicacoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `medicacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicos`
--

DROP TABLE IF EXISTS `medicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicos` (
  `id_medico` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(120) NOT NULL,
  `crm` varchar(20) NOT NULL,
  `horario_entrada` time DEFAULT NULL,
  `horario_saida` time DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id_medico`),
  UNIQUE KEY `crm` (`crm`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `medicos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicos`
--

LOCK TABLES `medicos` WRITE;
/*!40000 ALTER TABLE `medicos` DISABLE KEYS */;
INSERT INTO `medicos` VALUES (1,2,'Dr. João Silva','CRM0002','08:00:00','17:00:00',1);
/*!40000 ALTER TABLE `medicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes`
--

DROP TABLE IF EXISTS `pacientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pacientes` (
  `id_paciente` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) NOT NULL,
  `cpf` varchar(14) DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `sexo` enum('Masculino','Feminino','Outro') NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `telefone_emergencia` varchar(20) DEFAULT NULL,
  `nome_responsavel` varchar(120) DEFAULT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `cidade` varchar(100) DEFAULT NULL,
  `estado` varchar(30) DEFAULT NULL,
  `alergias` text DEFAULT NULL,
  `data_registro` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_paciente`),
  UNIQUE KEY `cpf` (`cpf`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes`
--

LOCK TABLES `pacientes` WRITE;
/*!40000 ALTER TABLE `pacientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `pacientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `procedimentos`
--

DROP TABLE IF EXISTS `procedimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `procedimentos` (
  `id_procedimento` int(11) NOT NULL AUTO_INCREMENT,
  `id_atendimento` int(11) NOT NULL,
  `descricao` varchar(255) NOT NULL,
  `profissional` varchar(120) DEFAULT NULL,
  `horario` datetime DEFAULT current_timestamp(),
  `area` enum('Enfermagem','Médico','Cirurgia','Outros') DEFAULT NULL,
  PRIMARY KEY (`id_procedimento`),
  KEY `id_atendimento` (`id_atendimento`),
  CONSTRAINT `procedimentos_ibfk_1` FOREIGN KEY (`id_atendimento`) REFERENCES `atendimentos` (`id_atendimento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procedimentos`
--

LOCK TABLES `procedimentos` WRITE;
/*!40000 ALTER TABLE `procedimentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `procedimentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recepcionistas`
--

DROP TABLE IF EXISTS `recepcionistas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recepcionistas` (
  `id_recepcionista` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `ativo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id_recepcionista`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `recepcionistas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recepcionistas`
--

LOCK TABLES `recepcionistas` WRITE;
/*!40000 ALTER TABLE `recepcionistas` DISABLE KEYS */;
INSERT INTO `recepcionistas` VALUES (1,4,1);
/*!40000 ALTER TABLE `recepcionistas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relatorios`
--

DROP TABLE IF EXISTS `relatorios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relatorios` (
  `id_relatorio` int(11) NOT NULL AUTO_INCREMENT,
  `id_atendimento` int(11) NOT NULL,
  `texto_relatorio` longtext DEFAULT NULL,
  `medico_responsavel` varchar(120) DEFAULT NULL,
  `gerado_em` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_relatorio`),
  KEY `id_atendimento` (`id_atendimento`),
  CONSTRAINT `relatorios_ibfk_1` FOREIGN KEY (`id_atendimento`) REFERENCES `atendimentos` (`id_atendimento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios`
--

LOCK TABLES `relatorios` WRITE;
/*!40000 ALTER TABLE `relatorios` DISABLE KEYS */;
/*!40000 ALTER TABLE `relatorios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setores`
--

DROP TABLE IF EXISTS `setores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `setores` (
  `id_setor` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) NOT NULL,
  `descricao` varchar(255) DEFAULT NULL,
  `localizacao` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id_setor`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setores`
--

LOCK TABLES `setores` WRITE;
/*!40000 ALTER TABLE `setores` DISABLE KEYS */;
INSERT INTO `setores` VALUES (1,'Consultório','Atendimento clínico geral','1º Andar - Bloco A'),(2,'Emergência','Atendimento crítico','Térreo - Bloco A'),(3,'Cirurgia','Salas cirúrgicas','Bloco C'),(4,'Recuperação Pós-Cirúrgica','Sala de recuperação','Bloco C'),(5,'Internação','Leitos de internação','Bloco F'),(6,'Maternidade','Atendimento obstétrico','Bloco G'),(7,'Pediatria','Atendimento infantil','Bloco H'),(8,'UTI','Terapia intensiva','Bloco D'),(9,'Medicação','Administração de fármacos','Bloco B'),(10,'Farmácia','Distribuição medicamentos','Bloco B'),(11,'Raio-X','Exames radiológicos','Bloco D'),(12,'Laboratório','Análises clínicas','Bloco E'),(13,'Fisioterapia','Reabilitação física','Bloco I'),(14,'Curativos','Cuidado de ferimentos','Bloco B'),(15,'Recepção de Exames','Entrega de exames','Bloco E'),(16,'Odontologia','Dentista','Bloco J'),(17,'Isolamento','Doenças infectocontagiosas','Bloco K'),(18,'Saúde Mental','Psiquiatria','Bloco L'),(19,'Observação','Pré-internação','Térreo - Bloco A');
/*!40000 ALTER TABLE `setores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `triagem`
--

DROP TABLE IF EXISTS `triagem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `triagem` (
  `id_triagem` int(11) NOT NULL AUTO_INCREMENT,
  `id_paciente` int(11) NOT NULL,
  `pressao_arterial` varchar(20) DEFAULT NULL,
  `frequencia_cardiaca` int(11) DEFAULT NULL,
  `frequencia_respiratoria` int(11) DEFAULT NULL,
  `saturacao` decimal(4,1) DEFAULT NULL,
  `temperatura` decimal(4,1) DEFAULT NULL,
  `dor_escala` int(11) DEFAULT NULL CHECK (`dor_escala` between 0 and 10),
  `sintomas` text DEFAULT NULL,
  `historico` text DEFAULT NULL,
  `id_classificacao` int(11) NOT NULL,
  `id_setor` int(11) NOT NULL,
  `id_profissional` int(11) NOT NULL,
  `horario_chegada` datetime DEFAULT current_timestamp(),
  `status` enum('Pendente','Finalizado') DEFAULT 'Pendente',
  PRIMARY KEY (`id_triagem`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_classificacao` (`id_classificacao`),
  KEY `id_setor` (`id_setor`),
  KEY `id_profissional` (`id_profissional`),
  CONSTRAINT `triagem_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`),
  CONSTRAINT `triagem_ibfk_2` FOREIGN KEY (`id_classificacao`) REFERENCES `classificacao_urgencia` (`id_classificacao`),
  CONSTRAINT `triagem_ibfk_3` FOREIGN KEY (`id_setor`) REFERENCES `setores` (`id_setor`),
  CONSTRAINT `triagem_ibfk_4` FOREIGN KEY (`id_profissional`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `triagem`
--

LOCK TABLES `triagem` WRITE;
/*!40000 ALTER TABLE `triagem` DISABLE KEYS */;
/*!40000 ALTER TABLE `triagem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) NOT NULL,
  `login` varchar(50) DEFAULT NULL,
  `senha_hash` varchar(255) DEFAULT NULL,
  `tipo` enum('Admin','Medico','Enfermeiro','Recepcao') NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Administrador Geral','admin','admin123','Admin'),(2,'Dr. João Silva','drjoao','medico123','Medico'),(3,'Maria Santos','maria_enf','enfermeira123','Enfermeiro'),(4,'Paulo Souza','paulo_rec','recepcao123','Recepcao');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'hospitamanager'
--

--
-- Dumping routines for database 'hospitamanager'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-21 15:57:58

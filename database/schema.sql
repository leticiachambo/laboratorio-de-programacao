-- =====================================================================
-- DogVision — Sistema de Identificação de Raças Caninas
-- Script de Definição de Dados (DDL)
-- Disciplina: Laboratório de Programação — Avaliação A1
-- SGBD alvo: MySQL 8 / MariaDB (ajustar tipos se outro SGBD for usado)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS dogvision
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE dogvision;

-- ---------------------------------------------------------------------
-- Tabela: usuario
-- ---------------------------------------------------------------------
CREATE TABLE usuario (
  id_usuario     INT AUTO_INCREMENT PRIMARY KEY,
  nome           VARCHAR(120)        NOT NULL,
  email          VARCHAR(150)        NOT NULL,
  senha_hash     VARCHAR(255)        NOT NULL,
  papel          ENUM('usuario', 'admin') NOT NULL DEFAULT 'usuario',
  ativo          BOOLEAN             NOT NULL DEFAULT TRUE,
  data_cadastro  DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_usuario_email UNIQUE (email)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: raca
-- ---------------------------------------------------------------------
CREATE TABLE raca (
  id_raca          INT AUTO_INCREMENT PRIMARY KEY,
  nome_popular     VARCHAR(100)  NOT NULL,
  nome_cientifico  VARCHAR(100)  NULL,
  descricao        TEXT          NULL,
  origem_dataset   VARCHAR(100)  NOT NULL COMMENT 'Identificação da classe no Stanford Dogs Dataset',
  CONSTRAINT uq_raca_origem UNIQUE (origem_dataset)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: modelo (versões do modelo de IA — usada a partir da Unidade 2)
-- ---------------------------------------------------------------------
CREATE TABLE modelo (
  id_modelo           INT AUTO_INCREMENT PRIMARY KEY,
  nome                VARCHAR(100)  NOT NULL,
  versao              VARCHAR(20)   NOT NULL,
  arquitetura         VARCHAR(100)  NULL,
  formato_exportacao  VARCHAR(30)   NULL COMMENT 'Ex.: ONNX, TFLite, TorchScript',
  data_treinamento    DATETIME      NULL,
  ativo               BOOLEAN       NOT NULL DEFAULT FALSE,
  CONSTRAINT uq_modelo_nome_versao UNIQUE (nome, versao)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: imagem
-- ---------------------------------------------------------------------
CREATE TABLE imagem (
  id_imagem        INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario       INT           NOT NULL,
  caminho_arquivo  VARCHAR(255)  NOT NULL,
  largura_px       INT           NULL,
  altura_px        INT           NULL,
  data_envio       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_imagem_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabela: deteccao
-- ---------------------------------------------------------------------
CREATE TABLE deteccao (
  id_deteccao    INT AUTO_INCREMENT PRIMARY KEY,
  id_imagem      INT             NOT NULL,
  id_raca        INT             NOT NULL,
  id_modelo      INT             NOT NULL,
  confianca      DECIMAL(5,4)    NOT NULL COMMENT 'Valor entre 0 e 1',
  bbox_x         INT             NULL,
  bbox_y         INT             NULL,
  bbox_largura   INT             NULL,
  bbox_altura    INT             NULL,
  data_deteccao  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_deteccao_imagem
    FOREIGN KEY (id_imagem) REFERENCES imagem (id_imagem)
    ON DELETE CASCADE,
  CONSTRAINT fk_deteccao_raca
    FOREIGN KEY (id_raca) REFERENCES raca (id_raca),
  CONSTRAINT fk_deteccao_modelo
    FOREIGN KEY (id_modelo) REFERENCES modelo (id_modelo),
  CONSTRAINT chk_confianca CHECK (confianca >= 0 AND confianca <= 1)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Índices de apoio às consultas mais frequentes
-- ---------------------------------------------------------------------
CREATE INDEX idx_imagem_usuario     ON imagem (id_usuario);
CREATE INDEX idx_deteccao_imagem    ON deteccao (id_imagem);
CREATE INDEX idx_deteccao_raca      ON deteccao (id_raca);
CREATE INDEX idx_deteccao_data      ON deteccao (data_deteccao);

-- ---------------------------------------------------------------------
-- Dados de exemplo (seed) — opcional, útil para testes manuais
-- ---------------------------------------------------------------------
INSERT INTO usuario (nome, email, senha_hash, papel) VALUES
  ('Admin DogVision', 'admin@dogvision.local', '<<hash_gerado_pela_aplicacao>>', 'admin');

INSERT INTO modelo (nome, versao, arquitetura, formato_exportacao, ativo) VALUES
  ('dogvision-detector', '0.1.0', 'a definir na Unidade 2', 'a definir na Unidade 2', TRUE);

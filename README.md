# DogVision

Sistema de identificação de raças caninas por visão computacional —
projeto da disciplina **Laboratório de Programação**.

## Equipe

- [Letícia Chambó]
- [Queila Alves]
- [Yasmin Carvalho]

## Sobre o projeto

O usuário envia uma fotografia de um cão por meio de uma interface web; o
sistema detecta o cão na imagem, identifica sua raça por meio de um modelo
de detecção de objetos treinado sobre um subconjunto do Stanford Dogs
Dataset, e retorna a raça, o nível de confiança e a localização do cão na
imagem. O histórico de identificações fica disponível para consulta, e um
painel de indicadores dá suporte ao acompanhamento do uso do sistema.

Tecnologias: **Python, SQL, HTML, CSS e JavaScript.**

## Status do projeto por unidade

| Unidade | Entregável | Status |
|---|---|---|
| 1 — Fundamentos e planejamento | Documento de visão e requisitos, modelagem de dados e de casos de uso, dataset anotado e particionado | Em desenvolvimento (Avaliação A1) |
| 2 — Treinamento e API | Modelo de detecção treinado, API de inferência, camada de persistência | A iniciar |
| 3 — Sistema completo | Autenticação, histórico, painel, testes, implantação em nuvem | A iniciar |

## Estrutura do repositório

```
dogvision/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/                    # Documentação da Avaliação A1
│   ├── 01_Documento_Visao_e_Requisitos.docx
│   ├── 02_Modelagem_Dados_e_Casos_de_Uso.docx
│   └── diagrams/            # Fontes .dot e imagens .png dos diagramas
├── database/
│   └── schema.sql           # Script DDL do banco de dados
├── dataset/
│   ├── README.md            # Instruções de download e preparação
│   ├── prepare_dataset.py   # Conversão de anotações e particionamento
│   ├── raw/                 # Dataset bruto (não versionado)
│   └── processed/           # Dataset anotado e particionado (não versionado)
├── api/                     # API de inferência (Unidade 2)
├── web/                     # Interface web — HTML/CSS/JS (Unidade 2/3)
└── models/                  # Artefatos de modelos treinados (não versionado)
```

## Como executar (a partir da Unidade 2)

Instruções de execução da API e da interface web serão adicionadas conforme
essas partes forem desenvolvidas nas próximas unidades.

## Documentação da Avaliação A1

- [`docs/01_Documento_Visao_e_Requisitos.docx`](docs/01_Documento_Visao_e_Requisitos.docx) —
  visão do produto, personas, histórias de usuário, requisitos funcionais e
  não funcionais.
- [`docs/02_Modelagem_Dados_e_Casos_de_Uso.docx`](docs/02_Modelagem_Dados_e_Casos_de_Uso.docx) —
  diagrama e especificação de casos de uso, DER, dicionário de dados e
  script DDL.
- [`database/schema.sql`](database/schema.sql) — script de criação do banco.
- [`dataset/`](dataset/) — processo de anotação e particionamento do
  conjunto de dados.

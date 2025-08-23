# Diário Oficial de Natal - Automação e API

Este projeto automatiza a coleta de PDFs do **Diário Oficial de Natal (DOM)**, faz upload para serviços de armazenamento externo e armazena informações em um **banco de dados PostgreSQL**, disponibilizando uma **API FastAPI** para consulta.

## 🧩 Estrutura do Projeto

```
.
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── models.py        # Modelos SQLAlchemy
│   ├── database.py      # Conexão com PostgreSQL
│   └── crud.py          # Funções CRUD (inserção, consulta, deleção)
├── scripts/
│   └── run.py           # Script de automação e coleta de PDFs
├── automation/
│   ├── __init__.py
│   ├── dom_scraper.py        # Carregar site e selecionar informações de PDFs
│   ├── driver_manager.py     # Configuração Selenium/Firefox
│   ├── pdf_handler.py        # Funções de download e updload de PDFs
│   └── utils.py              # Utilitários
├── config/
│   └── settings.py      # Configurações do projeto
├── downloads/           # Diretório para downloads temporários
├── screenshot/          # Imagens de captura de tela
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## ⚙ Funcionalidades

1. **Automação DOM**
   - Seleciona mês e ano do DOM de Natal.
   - Coleta links de PDFs.
   - Faz download dos PDFs para um diretório local.
   - Envia os arquivos para serviços de upload (ex.: 0x0.st).
   - Salva informações dos PDFs (título, URL, mês, ano, data de upload) no banco PostgreSQL.

2. **API FastAPI**
   - Rota principal `/` retorna mensagem de status.
   - Rota `/files/` permite:
     - Listar todos os arquivos.
     - Filtrar por **mês** e **ano**.
   - Rota `DELETE /files/` para remover registros do banco por mês/ano.

3. **Banco de Dados PostgreSQL**
   - Armazena registros dos PDFs coletados.
   - Configurável via `.env`.

## ⚙️ Configuração

### 1. Dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente (.env)

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=123
POSTGRES_DB=bd
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql+psycopg2://admin:123@db:5432/bd
DOWNLOAD_DIR=./downloads
```

## 🚀 Executando Localmente

### 1. Rodando a API
```bash
uvicorn api.main:app --reload
```
Acesse no navegador: `http://localhost:8000/`

### 2. Rodando a automação
```bash
python -m scripts.run
```

## 🐳 Docker

### 1. Build e Up
```bash
docker-compose --env-file .env build
docker-compose --env-file .env up -d
```

### 2. Executando o script de automação dentro do container
```bash
docker-compose exec -e PYTHONPATH=/app api python -m scripts.run
```

### 3. Acessando a API via container
- URL: `http://localhost:8000/`
- Listar arquivos: `http://localhost:8000/files/`
- Filtrar arquivos por mês/ano: `http://localhost:8000/files/?month=7&year=2025`

## 🛠 Tecnologias Utilizadas

- **Python 3.11** – Linguagem principal do projeto.
- **FastAPI** – Framework para construir a API REST.
- **SQLAlchemy** – ORM para integração com PostgreSQL.
- **PostgreSQL** – Banco de dados relacional para armazenar registros de PDFs.
- **Selenium + Firefox (Geckodriver)** – Automação do navegador para baixar arquivos do Diário Oficial de Natal.
- **Requests** – Para fallback de download de PDFs e upload para serviços externos.
- **Docker** – Containerização da aplicação para facilitar deploy.
- **Docker Compose** – Orquestração do serviço API e banco de dados em ambiente local.
- **Railway** – Plataforma de cloud para deploy da API e banco de dados.
- **python-dotenv** – Gerenciamento de variáveis de ambiente.
- **Xvfb** – Execução headless do Selenium em containers Linux.

## ✅ Boas práticas aplicadas

- Separação de responsabilidades (automation, scripts, api)
- Configuração via `.env`
- Docker + Docker Compose
- SQLAlchemy ORM
- Funções de upload modularizadas
- API com rotas de listagem e exclusão de registros
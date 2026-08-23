# Lumina API 🚀

API RESTful desenvolvida com **Django** e **Django REST Framework**, containerizada com **Docker** e **PostgreSQL**.

---

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

* [Git](https://git-scm.com/)
* [Docker Engine](https://docs.docker.com/get-docker/) (v20.10 ou superior)
* [Docker Compose](https://docs.docker.com/compose/install/) (v2.0 ou superior)

---

## 🚀 Instalação e Execução (Passo a Passo)

Siga estes passos em ordem no seu terminal para colocar o projeto e o banco de dados no ar:

### Passo 1: Clonar o repositório
Baixe o código do projeto para a sua máquina:
git clone [https://github.com/seu-usuario/lumina-api.git](https://github.com/seu-usuario/lumina-api.git)

### Passo 2: Acessar a pasta do projeto
Entre no diretório do projeto clonado:
cd lumina-api

### Passo 3: Construir e iniciar os containers
Execute o Docker Compose para criar as imagens e iniciar os serviços da API (`web`) e do Banco de Dados (`db`) em segundo plano:
docker compose up -d --build

*(Você pode rodar `docker compose ps` para verificar se os dois containers estão com status `Up`)*

### Passo 4: Rodar as migrações do banco de dados
Com os containers rodando, crie a estrutura de tabelas no banco de dados PostgreSQL:
docker compose exec web python manage.py migrate

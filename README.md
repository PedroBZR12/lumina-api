# Lumina API 🚀

API RESTful desenvolvida com **Django** e **Django REST Framework**, containerizada com **Docker** e **MySQL**.

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
Crie o arquivo local de configuração:

```bash
cp .env.example .env
```

Edite `.env` e defina `SECRET_KEY`, `DB_NAME`, `DB_USER` e `DB_PASSWORD`. Não publique esse arquivo.

Edite `.env` e preencha `SECRET_KEY`, `DB_PASSWORD` e, se quiser, `DB_NAME` e `DB_USER`. O Compose executa as migrações automaticamente ao iniciar a API.

```bash
docker compose up -d --build
```

Confira os containers e os logs:

```bash
docker compose ps
docker compose logs -f web
```

A API fica disponível localmente em `http://localhost:8000/api/`. Para conectar pelo MySQL Workbench, use host `127.0.0.1`, porta `3307`, usuário e senha definidos em `DB_USER` e `DB_PASSWORD`, e o banco `DB_NAME`. O MySQL Workbench é o cliente; o servidor MySQL é o container `db`. Se necessário, defina `DB_ROOT_PASSWORD` separadamente para a senha do usuário root do banco. Para desligar os containers sem apagar os dados, execute `docker compose down`; para removê-los, inclusive os dados persistidos, use `docker compose down -v`.

## API

Após a inicialização dos containers:

- `POST /api/caregivers/` cadastra um cuidador.
- `POST /api/auth/login/` autentica com `email` e `password`; envie o token retornado nas demais chamadas como `Authorization: Token <token>`.
- `POST /api/auth/password-reset/` solicita o link de recuperação por e-mail; `POST /api/auth/password-reset/confirm/` recebe `email`, `token` e a nova `password`.
- Os endpoints CRUD de pacientes, responsáveis, internações, alergias, rotinas, convênios, doenças, medicamentos e prescrições seguem o padrão `/api/<recurso>/`.
- `GET /api/patients/?name=ana` pesquisa pacientes pelo nome. Pacientes são criados com `responsibles` e `admission` no payload e não podem ser excluídos; registre a alta em `PATCH /api/hospitalizations/{id}/`.
- `GET /api/prescriptions/?patient={id}` lista prescrições do paciente; `GET /api/doses/?patient={id}&date=AAAA-MM-DD` lista doses agendadas. Doses iniciam como `PENDENTE` e são processadas por `POST /api/doses/{id}/mark/` com `status` igual a `MINISTRADO` ou `RECUSADO`.
- `POST /api/clinical-records/` cria registros clínicos; o mural pode ser filtrado com `date_from` e `date_to` no formato `AAAA-MM-DD`, em ordem cronológica.

Cada model possui seu arquivo de serializer diretamente em `api/serializers/`. A senha do cuidador é armazenada com hash. As ações do cuidador sobre pacientes exigem vínculo em `Cuidador_Paciente`; novos vínculos podem ser administrados pelo Django Admin.

Configure as variáveis SMTP (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` e `EMAIL_USE_TLS`) e `PASSWORD_RESET_URL` para habilitar a recuperação de senha em implantação.

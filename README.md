# Lumina API 🚀

API RESTful desenvolvida com **Django** e **Django REST Framework**, usando um banco **MySQL** hospedado no **Aiven**.

---

## 🛠️ Pré-requisitos

* [Git](https://git-scm.com/)
* Python 3.11 ou superior
* Bibliotecas cliente do MySQL (necessárias para compilar o `mysqlclient`). No macOS: `brew install mysql-client pkgconf`

---

## 🚀 Instalação e Execução

### Passo 1: Clonar o repositório e acessar a pasta

```bash
git clone https://github.com/seu-usuario/lumina-api.git
cd lumina-api
```

### Passo 2: Criar o ambiente virtual e instalar as dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Passo 3: Configurar a conexão com o Aiven

```bash
cp .env.example .env
```

Preencha o `.env` com os dados do serviço MySQL no console do Aiven (Host, Port, User, Password e Database name) e defina um `SECRET_KEY`. Não publique esse arquivo.

```
DB_ENGINE=django.db.backends.mysql
DB_HOST=<host>.aivencloud.com
DB_PORT=<porta>
DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=<senha>
DB_SSL_MODE=VERIFY_IDENTITY
DB_SSL_CA=certs/aiven-ca.pem
```

O certificado CA do projeto Aiven fica em `certs/aiven-ca.pem` (baixado em "CA certificate" no console). Caminhos relativos em `DB_SSL_CA` são resolvidos a partir da raiz do projeto.

### Passo 4: Aplicar as migrações e iniciar a API

```bash
python manage.py migrate
python manage.py runserver
```

A API fica disponível em `http://localhost:8000/api/`. Para inspecionar o banco pelo MySQL Workbench, use os mesmos dados de conexão do Aiven, com SSL obrigatório e o arquivo `certs/aiven-ca.pem` como CA.

Para rodar os testes (o Django cria e remove um banco temporário `test_<DB_NAME>` no Aiven):

```bash
python manage.py test
```

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

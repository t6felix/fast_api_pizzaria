# 🍕 API Pizzaria

API REST desenvolvida com **FastAPI**, **SQLAlchemy**, **JWT**, **OAuth2** e **SQLite** para gerenciamento de usuários e pedidos de uma pizzaria.

## Tecnologias Utilizadas

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Passlib (bcrypt)
- JWT (python-jose)
- OAuth2
- Alembic
- Python Dotenv

---

# Instalação

Clone o projeto:

```bash
git clone <repositorio>
cd fast_api_pizzaria
```

Instale as dependências:

```bash
pip install fastapi uvicorn "sqlalchemy>=2.0,<2.1" passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart sqlalchemy_utils alembic
```

---

# Configuração

Criar arquivo `.env`:

```env
SECRET_KEY=chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Executando a aplicação

```bash
uvicorn main:app --reload
```

Documentação automática:

```text
http://localhost:8000/docs
```

Swagger:

```text
http://localhost:8000/redoc
```

---

# Autenticação

A API utiliza autenticação baseada em **JWT**.

Fluxo:

```text
Criar Conta
      ↓
Realizar Login
      ↓
Receber Token JWT
      ↓
Enviar Token no Header
      ↓
Acessar Rotas Protegidas
```

Header utilizado:

```http
Authorization: Bearer SEU_TOKEN
```

---

# Estrutura do Projeto

```text
.
├── main.py
├── auth_routes.py
├── order_routes.py
├── dependencies.py
├── models.py
├── schemas.py
├── banco.db
├── .env
└── alembic/
```

---

# Endpoints de Autenticação

## Criar Conta

**POST**

```http
/auth/criar_conta
```

### Body

```json
{
    "nome": "Tiago",
    "email": "tiago@email.com",
    "senha": "123456",
    "ativo": true,
    "admin": false
}
```

### Resposta

```json
{
    "mensagem": "usuario cadastrado com sucesso"
}
```

---

## Login

**POST**

```http
/auth/login
```

### Body

```json
{
    "email": "tiago@email.com",
    "senha": "123456"
}
```

### Resposta

```json
{
    "access_token": "jwt_token",
    "refresh_token": "jwt_token",
    "token_type": "Bearer"
}
```

---

## Login OAuth2

Utilizado pelo Swagger UI.

**POST**

```http
/auth/login-form
```

### Form Data

```text
username=email@exemplo.com
password=123456
```

### Resposta

```json
{
    "access_token": "jwt_token",
    "token_type": "Bearer"
}
```

---

## Renovar Token

**GET**

```http
/auth/refresh
```

### Header

```http
Authorization: Bearer TOKEN
```

### Resposta

```json
{
    "access_token": "novo_token",
    "token_type": "Bearer"
}
```

---

# Endpoints de Pedidos

> Todas as rotas abaixo exigem autenticação.

---

## Criar Pedido

**POST**

```http
/pedidos/pedido
```

### Body

```json
{
    "id_usuario": 1
}
```

### Resposta

```json
{
    "mensagem": "pedido criado com sucesso"
}
```

---

## Adicionar Item ao Pedido

**POST**

```http
/pedidos/pedido/adicionar-item/{id_pedido}
```

### Body

```json
{
    "quantidade": 2,
    "sabor": "Calabresa",
    "tamanho": "Grande",
    "preco_unitario": 45.90
}
```

### Resposta

```json
{
    "mensagem": "item criado com sucesso",
    "item_id": 1,
    "preco_pedido": 91.80
}
```

---

## Remover Item

**POST**

```http
/pedidos/pedido/remover-item/{id_item_pedido}
```

### Resposta

```json
{
    "mensagem": "item removido com sucesso"
}
```

---

## Visualizar Pedido

**GET**

```http
/pedidos/pedido/{id_pedido}
```

### Resposta

```json
{
    "qtd_itens_pedido": 2,
    "pedido": {
        "id": 1,
        "status": "PENDENTE",
        "preco": 91.80
    }
}
```

---

## Finalizar Pedido

**POST**

```http
/pedidos/pedido/finalizar/{id_pedido}
```

### Resposta

```json
{
    "mensagem": "pedido numero 1 finalizado com sucesso"
}
```

---

## Cancelar Pedido

**POST**

```http
/pedidos/pedido/cancelar/{id_pedido}
```

### Resposta

```json
{
    "mensagem": "pedido numero 1 cancelado com sucesso"
}
```

---

## Listar Todos os Pedidos

> Apenas administradores.

**GET**

```http
/pedidos/listar
```

### Resposta

```json
{
    "pedidos": []
}
```

---

## Listar Pedidos do Usuário Logado

**GET**

```http
/pedidos/listar/{pedidos-usuario}
```

### Resposta

```json
[
    {
        "id": 1,
        "status": "PENDENTE",
        "preco": 91.80,
        "itens": [
            {
                "quantidade": 2,
                "sabor": "Calabresa",
                "tamanho": "Grande",
                "preco_unitario": 45.90
            }
        ]
    }
]
```

---

# Regras de Negócio

## Usuários

- E-mail deve ser único.
- Senhas são armazenadas criptografadas utilizando bcrypt.
- Usuários podem ser administradores ou usuários comuns.

## Pedidos

- Todo pedido inicia com status `PENDENTE`.
- Apenas o dono do pedido ou um administrador pode alterá-lo.
- O valor total do pedido é calculado automaticamente através dos itens adicionados.

## Itens

- Itens pertencem a apenas um pedido.
- Ao adicionar ou remover itens, o preço total é recalculado.

---

# Modelagem

## Usuário

```text
Usuario
├── id
├── nome
├── email
├── senha
├── ativo
└── admin
```

---

## Pedido

```text
Pedido
├── id
├── status
├── usuario
├── preco
└── itens
```

---

## ItemPedido

```text
ItemPedido
├── id
├── quantidade
├── sabor
├── tamanho
├── preco_unitario
└── pedido
```

---

# Fluxo de Utilização

```text
1. Criar usuário
2. Realizar login
3. Receber JWT
4. Criar pedido
5. Adicionar itens
6. Consultar pedido
7. Finalizar ou cancelar pedido
```

---

# Possíveis Melhorias Futuras

- Refresh Token dedicado
- Controle de expiração avançado
- Paginação de pedidos
- Filtros de consulta
- CRUD de sabores
- CRUD de produtos
- Controle de estoque
- Integração com pagamento
- Banco PostgreSQL
- Testes automatizados
- Docker
- CI/CD

---

# Autor

Projeto criado para estudo de:

- FastAPI
- OAuth2
- JWT
- SQLAlchemy
- Relacionamentos ORM
- APIs REST
- Segurança e autenticação

---

## Referência

Série de estudos FastAPI:

https://www.youtube.com/watch?v=BtIy2aD8k_w&list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq

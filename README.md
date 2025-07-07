> Sistema de Controle de Estoque - FastAPI + PostgreSQL

API feita com FastAPI e PostgreSQL para controle de estoque com as funcionalidades:

• Cadastro de produtos com código único e descrição

• Atualização de produtos existentes por ID

• Filtro e busca de produtos por código ou descrição (parcial)

• Cadastro de entradas de estoque

• Listagem de todas as entradas de estoque de um produto (via código)

• Cadastro de clientes com CPF único e nome

• Atualização de dados do cliente por ID

• Busca de clientes por nome ou CPF (parcial)

• Geração de relatório em PDF com todos os produtos cadastrados

• Estrutura modular com FastAPI e PostgreSQL

• Conexão com banco de dados via variáveis de ambiente (.env)

• Documentação automática via Swagger (/docs) e Redoc (/redoc)

> Como rodar

1. Banco de Dados:

Para inicializar o banco, use o script SQL incluso no arquivo `Sistema_estoque` dentro do pgAdmin ou psql.


2. Clone o repositório:

Faça um clone ou baixe o .zip de https://github.com/WylliamMarinho/sistema-estoque.git

3. Abra o projeto baixado no pycharm, vá no terminal e ative:

python -m venv venv
.\venv\Scripts\activate

4. Instale os pacotes:

pip install -r requirements.txt

5. Crie um .env com base no .env.example

6. Rode a API no terminal:

uvicorn app.main:app --reload

7. Acesse o Sistema em: http://localhost:8000/docs

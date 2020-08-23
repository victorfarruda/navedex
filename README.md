# Navedex - O sistema criador de navedex's
Este sistema é a implementação de um desafio, onde o sistema consiste em um criador de navedex's, nele o usuário pode se cadastrar utilizando email e senha, e então ao logar terá acesso ao banco de dados dos seus navers, possuindo informações como: nomes, data de nascimento, cargos, tempo de empresa e projetos que participou.

### Clonar o repositório
```
git clone https://github.com/victorfarruda/navedex.git
cd navedex/
cp env-sample .env
```

### Dependências

1. [Instalar docker](https://docs.docker.com/install/)
2. [Instalar o docker-compose](https://docs.docker.com/compose/install/)

### Para utilizar o Docker com o Docker Compose:
Primeiro gere a imagem do projeto:
```
docker-compose build
```
Atualize o banco de dados do .env para:
```
DATABASE_URL=postgres://postgres:postgres@db/postgres
```
Coloque o banco de dados postgres no ar com:
```
docker-compose up -d db
```
Não Esqueça das migrations:
```
docker-compose run --rm web python manage.py migrate
```
E pode iniciar o projeto:
```
docker-compose up -d
```
E o projeto está rodando em:
```
http://localhost:8000
```
### Testes

Para rodar os testes pode usar o comando:
```
docker-compose run --rm web pytest --cov=navedex
```

Você também pode executar testes no Postman
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0c34756467d47b944066)

### Possíveis dificuldades com a utilização pode entrar em contato:
victorf.arruda@outlook.com

# Navedex - O sistema criador de navedex's
Este sistema é a implementação de um desafio, onde o sistema consiste em um criador de navedex's, nele o usuário pode se cadastrar utilizando email e senha, e então ao logar terá acesso ao banco de dados dos seus navers, possuindo informações como: nomes, data de nascimento, cargos, tempo de empresa e projetos que 
participou.

## Testes Postman:
Você pode executar testes no Postman:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0c34756467d47b944066)

### Clonar o repositório:
```
git clone git@github.com:victorfarruda/navedex.git
```
Entre na pasta do projeto:
```
cd navedex/
```
Já dentro do diretório ```navedex```, copie as variáveis de ambiente:
```
cp env-sample .env
```
Não se esqueça de remover o ```DATABASE_URL``` caso queira usar o sqlite ou configure o ```DATABASE_URL``` para conectar ao seu banco de dados.

### Configuração do projeto sem docker
Caso não queria usar o docker você deve instalar o pipenv:
```
pip install pipenv
```
Instale as dependências do projeto:
```
pipenv install --dev
```
Não esqueça das migrations:
```
pipenv run python manage.py migrate
```
E em seguida pode rodar o projeto:
```
pipenv run python manage.py runserver localhost:8000
```
#### Testes sem docker

Para rodar os testes sem docker pode usar o comando (lembrando que seu banco de dados deve estar configurado corretamente):
```
pipenv run pytest --cov=navedex
```

### Para configurar o projeto com Docker e Docker Compose:

#### Dependências

1. [Instalar docker](https://docs.docker.com/install/)
2. [Instalar o docker-compose](https://docs.docker.com/compose/install/)

Primeiro gere a imagem do projeto:
```
docker-compose build
```
Atualize o banco de dados do .env para:
```
DATABASE_URL=postgres://postgres:postgres@db/postgres
```
Coloque o banco de dados postgres online com:
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
#### Testes com docker

Para rodar os testes com docker pode usar o comando (lembrando que seu banco de dados deve estar online):
```
docker-compose run --rm web pytest --cov=navedex
```

### Possíveis dificuldades com a utilização pode entrar em contato:
victorf.arruda@outlook.com

# Desafio de back-end utilizando Python/Django

## Navedex API

### O Sistema:

O sistema consiste em um criador de navedex's, nele tu poderá se cadastrar utilizando `email` e `senha`, e então ao logar terá acesso ao banco de dados dos seus navers, possuindo informações como: nomes, data de nascimento, cargos, tempo de empresa e projetos que participou.

Você deve fazer a estrutura do banco de dados como achar necessário, mas lembrando que é obrigatório as entidades de `users`, `navers` e `projetos` estarem relacionadas entre si. Deve ser possível saber em quais projetos um naver está e vice-versa, tudo baseado no usuário que fez a requisição.

### O que deve ser entregue:

Deve ser implementada uma API utilizando Django no padrão [`RESTful`](https://becode.com.br/o-que-e-api-rest-e-restful/#:~:text=REST%20significa%20Representational%20State%20Transfer,abstra%C3%A7%C3%A3o%20da%20arquitetura%20da%20Web.) que possibilite as funcionalidades descritas abaixo:

Junto a API, uma documentação de como testar o sistema é muito bem-vinda. Muitas vezes o README.md do projeto basta, porém também é interessante disponibizar documentação a partir de algum software para testar suas requests, recomendamos o [postman](https://www.postman.com/) ou [insomnia](https://insomnia.rest/download/);

O entregável do teste será o link de um repositório público no seu github pessoal contendo tudo que foi pedido acima.

### Funcionalidades

- Autenticação
'

    - (Signup) Rota de cadastro ```http://localhost:8000/signup/```
        - Deverá receber email e senha e criar novo registro no banco

    - (Login) Rota para poder logar no sistema ```http://localhost:8000/login/```
        - Deverá retornar um token [JWT](https://jwt.io/) para o usuário ter acesso à outras rotas

OBS: ```AS ROTAS A BAIXO NÃO PODEM SER ACESSADAS CASO O USUÁRIO NÃO POSSUA O TOKEN DE ACESSO (RECEBIDO NO LOGIN)```

- Navers

  - (Index) Rota para listagem dos Navers. ```http://localhost:8000/naver/api/naver/```

    - Filtrar por nome, tempo de empresa e cargo. 
    - Query params: ```name, admission_date, admission_date__gte, admission_date__lte, or job_role```
    - O retorno é um array com todos os navers ou filtrado por algum dos parâmetro acima, pertencentes ao usuário que fez a request, exemplo:
      ```
          [
              {
                  id: 1,
                  name: Fulano,
                  birthdate: 1999-05-15,
                  admission_date: 2020-06-12,
                  job_role: Desenvolvedor
              },
              {
                  id: 2,
                  name: Ciclano,
                  birthdate: 1992-10-28,
                  admission_date: 2018-06-12,
                  job_role: Desenvolvedor
              }
          ]
      ```

  - (Show) Rota para detalhar informações de um único naver através de seu identificador ```http://localhost:8000/naver/api/naver/{naver_id}```

    - Além das informações do naver, trazer quais projetos este participou
    - O retorno é um objeto contendo informações sobre o Naver, exemplo:
      ```
      {
          id: 1,
          name: Fulano,
          birthdate: 1999-05-15,
          admission_date: 2020-06-12,
          job_role: Desenvolvedor,
          projects: [
              {
                  id: 3,
                  name: Projeto muito Bom
              }
          ]
      }
      ```

  - (Store) Rota de Criação de Naver ```http://localhost:8000/naver/api/naver/```
    - Recebe através do body da request os dados do naver e um array com os identificadores dos projetos que ele participa e cria um novo registro no banco de dados vinculado ao usuário que fez a request
      ```
          {
              name: Fulano,
              birthdate: 1999-05-15,
              admission_date: 2020-06-12,
              job_role: Desenvolvedor,
              projects: [3]
          }
      ```
    - O retorno é o objeto do usuário criado


  - (Update) Rota Para Atualização de Naver ```http://localhost:8000/naver/api/naver/{naver_id}```
    - Recebe através do body da request os dados do naver e um array com os identificadores dos projetos que ele participa e atualiza seu registro no banco de dados
    - Um usuário só pode editar seus próprios navers
      ```
          {
              name: Fulano,
              birthdate: 1999-05-15,
              admission_date: 2020-06-12,
              job_role: Desenvolvedor,
              projects: [3]
          }
      ```
    - O retorno é o objeto do usuário Atualizado

  - (Delete) Rota Para Deletar um Naver ```http://localhost:8000/naver/api/naver/{naver_id}```
    - Recebe um identificador de naver e o remove dos registros do banco.
    - Um usuário só pode deletar seus próprios navers.

* Projetos

  - (Index) Rota para listagem dos Projetos ```http://localhost:8000/naver/api/project/```
    - Filtrar por nome
    - Query params: ```name```
    - O retorno é um array com todos os projetos ou filtrado pelo nome, pertencentes ao usuário que fez a request, exemplo:
      ```
          [
              {
                  id: 3,
                  name: Projeto muito Bom
              },
              {
                  id: 5,
                  name: Projeto Realmente Bom
              }
          ]
      ```
  - (Show) Rota para detalhar um projeto  ```http://localhost:8000/naver/api/project/{project_id}```

    - Além das informações do projeto, trazer quais foram os navers que participaram
    - O retorno é um objeto contendo informações sobre o projeto, exemplo:
      ```
              {
                  id: 3,
                  name: Projeto muito Bom,
                  navers: [
                      {
                          id: 1,
                          name: Fulano,
                          birthdate: 1999-05-15,
                          admission_date: 2020-06-12,
                          job_role: Desenvolvedor
                      }
                  ]
              }
      ```

  - (Store) Rota de Criação de Projeto ```http://localhost:8000/naver/api/project/```
    - Recebe através do body da request os dados do projeto e um array com os identificadores dos navers que trabalham nele e cria um novo registro no banco de dados vinculado ao usuário que fez a request
      ```
          {
              name: Projeto Bom,
              navers: [1]
          }
      ```
    - O retorno é o objeto do Projeto criado


  - (Update) Rota Para Atualização de Projeto ```http://localhost:8000/naver/api/project/{project_id}```
    - Recebe através do body da request os dados do projeto e um array com os identificadores dos navers que trabalham nele e atualiza seu registro no banco de dados
    - Um usuário só pode editar seus próprios projetos
      ```
          {
              name: Projeto Bom,
              navers: [1]
          }
      ```
    - O retorno é o objeto do projeto Atualizado

  - (Delete) Rota Para Deletar um Projeto ```http://localhost:8000/naver/api/project/{project_id}```
    - Recebe um identificador de projeto e o remove dos registros do banco.
    - Um usuário só pode deletar seus próprios projetos

## Observações

As respostas da API devem ser em formato JSON como nos exemplos acima.

A escrita de testes automatizados é **muito importante**.

Utilize um banco de dados relacional (postgresql, mysql, etc).<br>
Será observado organização de código, legibilidade e melhor uso dos recursos da linguagem python e boa práticas do Django. Como bônus e se sentir a vontade pode fazer uso do biblioteca [Django REST Framework](https://www.django-rest-framework.org/).

Se durante o processo de desenvolvimento não conseguiu fazer algo, explique qual o impedimento que encontrou e como tentou resolver em uma seção `Dificuldades` do seu README.md e nos submite até onde chegou :smile:

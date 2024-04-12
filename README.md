# api-brain-ag-desafio
Desafio técnico proposto pela Tinnova e Serasa para criação de uma API de gestão de produtor rural.
Permite a gestão de produtores rurais, gestão de culturas vegetais e vínculo de produtores com culturas.
Validações padrões de uma API REST, validação do formato de CPF/CNPJ e área da fazenda, agricultável e vegetação.


## Requisitos
- [Python 3.x](https://www.python.org/downloads/)
- venv - biblioteca padrão do python
- [Docker](https://www.docker.com/get-started/)
- [VSCode](https://code.visualstudio.com/) (recomendado)
- [Postman](https://www.postman.com/) (opcional)
  
## Instalação
Faça o clone desse repositório em sua máquina.
```
$ git clone git@github.com:viniciusarantes/api-brain-ag-desafio.git
$ cd api-brain-ag-desafio.git/
```

Na pasta do repositório crie um ambiente virtual utilizando venv:
```
$ python -m venv venv
```

Em seguida, ative o ambiente virtual.

### Windows
```
> .\venv\Scripts\activate
(venv) PS C:\api-brain-ag-desafio>
```

### Linux / MacOS
```
$ source venv/bin/activate
(venv) /api-brain-ag-desafio $
```
DICA: Quando a venv está ativa, um prefixo como (venv) deve aparecer no terminal. Certifique sempre que está com o ambiente virtual ativo e na raiz do projeto para executar os comandos.

Com a venv ativada, faça a instalação das dependências do projeto.
```
$ pip install -r requirements.txt
```

## Executar Servidor (Container)
A aplicação e o banco de dados será executada dentro de containers. Um container está o banco de dados PostgreSQL e o outro será a API.

Certifique-se que tenha o Docker instalado.
Para subir a aplicação, vá na raiz do projeto e digite o comando:
```
$ docker compose up
```
OBS: O container da aplicação irá executar um script bash que realiza a migração das tabelas pelos comandos do django e executa o servidor.

Para verificar se a API  está rodando corretamente, as últimas linhas de log do console devem ser algo parecido com isso:
```
apirest  | Starting Server...
apirest  | Watching for file changes with StatReloader
apirest  | Performing system checks...
apirest  |
apirest  | System check identified no issues (0 silenced).
apirest  | April 12, 2024 - 19:28:36
apirest  | Django version 5.0.4, using settings 'api.settings'
apirest  | Starting development server at http://0.0.0.0:8000/
apirest  | Quit the server with CONTROL-C.
apirest  |
```

### Executar apenas o container Postgres
Caso prefira executar o projeto localmente dentro do VSCode sem precisar subir a aplicação em um container, é necessário pelo menos subir o container do banco de dados para funcionar a conexão.

Para executar apenas o banco, digite o comando na raiz do projeto.
```
$ docker compose up -d db
```
Dessa forma apenas o Postgres será executado, tornando possível a execução da API na sua máquina local. 

Se deseja executar a aplicação diretamente em sua máquina, verifique o arquivo `django.sh` na raiz do projeto para executar os comandos iniciais do django para migração e execução do servidor.

Neste ponto já é possível realizar as chamadas locais pelos endpoints da API.

## Testes unitários
Para realizar os testes unitários, abra o console na raiz do projeto. Certifique-se que o console esteja utilizando o ambiente virtual (venv). Caso não esteja, ative com o comando citado mais acima.

Com o ambiente virtual ativado, digite o comando para executar os testes unitários.
```
$ pytest rural/tests --verbose
```

Ou, se preferir executar pela interface, abra o projeto com o VSCode, verifique se está utilizando a venv como interpretador Python e selecione a opção Testing na barra lateral. Nesta aba é possível executar todos os testes e conferir o log de execução.

## Testes locais com POSTMAN
Na pasta `local/` está o json referente à collection do POSTMAN com todos os requests necessários para a chamada da API.

Certifique que a aplicação e o container do Postgres esteja em execução. Para verificar, execute o comando docker.
```
$ docker ps -a
```

Com a aplicação rodando, importe a collection no POSTMAN e teste os endpoints disponibilizados pela API.
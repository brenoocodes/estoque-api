# Back-End Controle de Estoque

Este projeto é referente a uma API completa desenvolvida em Python, utilizando o framework Flask, juntamente com o banco de dados MySQL. Futuramente, teremos o projeto front-end desenvolvido em React, e o link estará disponível aqui. Abaixo, vou explicar todos os arquivos e suas funções, e no link fornecido, você terá a opção de verificar no Postman os resultados das rotas. Veremos também as dependências necessárias para o funcionamento. Aproveite para me seguir nas outras redes sociais.

🔗 [Postman](https://documenter.getpostman.com/view/30843980/2sA2r535SC)

### Dependências a serem instaladas

Para executar esta API, será necessário realizar algumas instalações. Abra o terminal do seu editor de código ou do seu sistema operacional. É bem-vindo criar um ambiente virtual se a sua IDE já não cria automaticamente para você. Abaixo estão as dependências a serem instaladas, você também pode encontrar essas informações na nossa página do Notion.

🔗 [Notion](https://jolly-lodge-af5.notion.site/Api-Controle-de-estoque-informa-es-ff6d8036c4984a82b1b0e84f9905ebc7?pvs=4)

Você também tem o código para criar o `requirements.txt` de forma automática.

## Valor de cada arquivo da pasta principal

Após configurar seu ambiente, aqui vou repassar os arquivos de nosso código e explicar de forma prévia o que cada um faz.

### [app.py](app.py)

O `app.py` é o arquivo que roda nosso projeto, ele fica na pasta principal do projeto, pois se você quiser subir para um servidor, esse arquivo será lido. Ele será o arquivo que você vai rodar para executar o projeto.

### [Procfile](Procfile)

O arquivo `Procfile` foi usado por mim para colocar o projeto no Heroku, nele temos as instruções necessárias para o servidor rodar seu arquivo, no caso da Heroku.


### [requirements.txt](requirements.txt)

Arquivo que será lido para instalar as dependências do projeto no servidor.

### [Pasta src](/src)

Aqui estarão todos os nossos arquivos, basicamente será a pasta na qual iremos trabalhar. Basicamente, inicialmente, são esses são os valores dos arquivos na pasta principal, agora vamos para a pasta src explicar todos os arquivos e função de cada um.
***
## Explicando a Pasta src e seus Códigos

### [config.py](src/config.py)

O primeiro arquivo que precisamos explicar é o `config.py`. Este arquivo é o ponto de partida de tudo. Nele, criamos a aplicação Flask, configuramos a chave secreta (`SECRET_KEY`), e estabelecemos a conexão com o banco de dados, conforme a linha abaixo exemplifica. É importante ressaltar que você precisa ter instalado as bibliotecas mencionadas anteriormente para que tudo funcione corretamente.

Na linha abaixo, onde se lê:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456789@localhost/seubanco'
```
- `mysql` é o tipo de banco de dados que está sendo utilizado.
- `root` é o nome de usuário do servidor. Após os dois pontos (:), você deve inserir a senha correspondente ao seu usuário MySQL.
- `localhost` indica onde o seu banco de dados está hospedado.
- `seu_banco` é o nome do banco de dados que você criou anteriormente. É importante ter criado o banco antes de prosseguir.

Também inicializamos as seguintes configurações:
 

Também iniciamos 
```
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
```
- `db` é a instância do SQLAlchemy, utilizado para interagir com o banco de dados.
- `bcrypt` é a instância do Bcrypt, uma biblioteca utilizada para criptografar senhas de forma segura.
---
### [models.py](src/models.py)

No `SQLALCHEMY`, você pode criar suas tabelas através de classes em Python e fazer as operações no banco, conforme veremos. Neste arquivo, criamos a estrutura do nosso banco de dados.

#### Tabelas Criadas:

#### Funcionarios
- `matricula`: Chave primária do funcionário (Integer)
- `nome`: Nome do funcionário (String, 255 caracteres)
- `email`: Email do funcionário (String, 255 caracteres, único)
- `senha`: Senha do funcionário (String, 255 caracteres)
- `administrador`: Indica se o funcionário é administrador (Boolean)

#### Fornecedores
- `id`: Chave primária do fornecedor (Integer)
- `cnpj`: CNPJ do fornecedor (String, 14 caracteres, único)
- `razao_social`: Razão social do fornecedor (String, 255 caracteres)
- `nome_fantasia`: Nome fantasia do fornecedor (String, 255 caracteres)
- `email`: Email do fornecedor (String, 255 caracteres)
- `telefone`: Telefone do fornecedor (String, 14 caracteres)

#### Produtos
- `id`: Chave primária do produto (Integer)
- `nome`: Nome do produto (String, 255 caracteres, único)
- `nome_estoque`: Nome do estoque do produto (String, 255 caracteres)
- `medida`: Medida do produto (String, 50 caracteres)
- `preco`: Preço do produto (Float, default 0.0)
- `quantidade`: Quantidade do produto (Integer)
- `fornecedores`: Relacionamento com fornecedores (Relação muitos-para-muitos)

#### ProdutosFornecedores
- `produto_id`: Chave estrangeira referente ao produto (Integer)
- `fornecedor_id`: Chave estrangeira referente ao fornecedor (Integer)
- (Chave primária composta pelos dois campos acima)

#### EntradasEstoque
- `id`: Chave primária da entrada de estoque (Integer)
- `nota`: Nota da entrada de estoque (String, 50 caracteres)
- `produto_id`: Chave estrangeira referente ao produto (Integer)
- `fornecedor_id`: Chave estrangeira referente ao fornecedor (Integer)
- `data_entrada`: Data da entrada de estoque (DateTime, default datetime.utcnow)
- `quantidade`: Quantidade da entrada de estoque (Integer)
- `funcionario_matricula`: Chave estrangeira referente ao funcionário (Integer)

#### SaidasEstoque
- `id`: Chave primária da saída de estoque (Integer)
- `produto_id`: Chave estrangeira referente ao produto (Integer)
- `data_saida`: Data da saída de estoque (DateTime, default datetime.utcnow)
- `quantidade`: Quantidade da saída de estoque (Integer)
- `funcionario_responsavel`: Chave estrangeira referente ao funcionário responsável (Integer)
- `funcionario_requisitante`: Chave estrangeira referente ao funcionário requisitante (Integer)

 Nesse contexto, temos também logo no final do arquivo, um trecho comentado: 
```
# Criar o database
with app.app_context():
  db.drop_all()
  db.create_all()
```

Este trecho é crucial para a criação do banco de dados através da execução do arquivo `models.py`. Além disso, foram realizadas as importações necessárias no início do arquivo, incluindo a biblioteca `datetime`, para garantir que o banco possa utilizar suas funções adequadamente.
___
### [Login.py](src/Login.py)

Dentro do arquivo `login.py`, realizamos os processos de autenticação e geração de tokens.

Dentro da pasta `login` no [Postman](https://documenter.getpostman.com/view/30843980/2sA2r535SC), você encontrará como será a resposta e como deve fazer sua requisição.

#### Explicação do Arquivo `login.py`

O arquivo `login.py` é responsável pela autenticação de usuários na API. Ele contém a lógica necessária para verificar as credenciais de um usuário e gerar um token de acesso válido.

#### Funções

#### `token_obrigatorio`

Este é um decorador de função que verifica se um token de autenticação válido está presente no cabeçalho da requisição. Ele decodifica o token utilizando a chave secreta da aplicação e verifica se o token está válido e se corresponde a um usuário cadastrado no sistema. Se o token não estiver presente, expirado ou inválido, ele retorna uma resposta de erro. Vocês verão que, abaixo de cada rota, nos próximos arquivos, a gente coloca um ```@token_obrigatorio ```, isso indica que todas as rotas estão protegidas com token.

#### Rota `/login` 
Para usar essa rota você deve usar o método **`POST`**

Esta rota lida com as solicitações de login dos usuários. Aqui está a explicação das etapas realizadas nesta rota:

1. **Verificação das Credenciais**: A rota verifica se as credenciais de autenticação estão presentes na requisição. Se não estiverem presentes ou forem inválidas, retorna uma resposta de erro.

2. **Busca do Usuário**: Em seguida, a rota busca o usuário no banco de dados pelo e-mail ou matrícula fornecidos na requisição. Se o usuário não for encontrado, retorna uma resposta de erro.

3. **Verificação da Senha**: Após encontrar o usuário, a rota verifica se a senha fornecida na requisição corresponde à senha armazenada no banco de dados para o usuário. Se a senha estiver correta, avança para o próximo passo.

4. **Geração do Token**: A rota gera um token de acesso válido utilizando a biblioteca JWT (JSON Web Tokens). O token é codificado com a matrícula do usuário e uma data de expiração de 20 dias a partir do momento atual. Em seguida, os dados do usuário e o token são preparados para serem retornados como resposta.

5. **Resposta da Requisição**: Por fim, a rota retorna os dados do usuário e o token como resposta da requisição.

___
### [validadorcampo.py](src/validadorcampo.py)

Dentro do arquivo `validadorcampo.py`, são realizadas as verificações do JSON para os métodos POST e PUT. Isso é feito para garantir que o servidor gere erros bem formatados caso o JSON contenha informações incorretas.
#### Explicação das Funções Decoradoras

#### `verifica_campos_tipos`

Esta função decoradora é responsável por verificar se os campos obrigatórios e seus tipos esperados estão presentes no JSON enviado na requisição. Aqui está o funcionamento detalhado:

- Recebe como parâmetros `campos_obrigatorios` e `tipos_esperados`, que são uma lista e um dicionário contendo os campos obrigatórios e os tipos esperados para cada campo, respectivamente. Dentro das rotas de POST e PUT, vamos ver como devem ser passado essa lista e esse dicionário

- Retorna uma função decoradora que envolve a função original.

- Dentro da função decoradora (`wrapper`), obtém o JSON da requisição usando `request.get_json()` e verifica se o JSON está presente. Se não estiver presente, retorna uma resposta de erro com status 400.

- Em seguida, itera sobre os campos do JSON e verifica se todos os campos obrigatórios estão presentes. Se algum campo estiver ausente, retorna uma mensagem de erro indicando o campo faltante.

- Após isso, itera sobre os campos e tipos esperados e verifica se os tipos dos valores correspondentes são os esperados. Se algum tipo estiver incorreto, retorna uma mensagem de erro indicando o tipo esperado para o campo.

- Se todas as verificações passarem com sucesso, a função original é chamada e seu resultado é retornado.

#### `verifica_alterar`

Esta função decoradora é semelhante à `verifica_campos_tipos`, mas é usada para endpoints que lidam com operações de alteração. Aqui está o funcionamento detalhado:

- Recebe como parâmetros `campos_obrigatorios` e `tipos_esperados`, que são dicionários contendo os campos obrigatórios e os tipos esperados para cada campo, respectivamente.

- Retorna uma função decoradora que envolve a função original.

- Dentro da função decoradora (`wrapper`), obtém o JSON da requisição usando `request.get_json()` e verifica se o JSON está presente. Se não estiver presente, retorna uma resposta de erro com status 400.

- Em seguida, itera sobre os campos do JSON e verifica se todos os campos obrigatórios estão presentes. Se algum campo estiver ausente, retorna uma mensagem de erro indicando o campo faltante.

- Depois, verifica se os tipos dos valores correspondentes aos campos obrigatórios são os esperados. Se algum tipo estiver incorreto, retorna uma mensagem de erro indicando o tipo esperado para o campo.

- Se todas as verificações passarem com sucesso, a função original é chamada e seu resultado é retornado.

Ambas as funções têm tratamento de exceções para lidar com erros de decodificação JSON e exceções genéricas durante o processamento da requisição. Se ocorrer algum erro, uma mensagem de erro genérica é retornada com status 500.



___
### [funcionarios.py](src/funcionarios.py)

No arquivo `funcionarios.py`, são executados os processos de leitura, criação e atualização de cada funcionário.

Dentro da pasta `Funcionarios` no [Postman](https://documenter.getpostman.com/view/30843980/2sA2r535SC), você encontrará como será a resposta e como fazer a requisição para cada rota.
### Rota `/funcionario` (GET)

Esta rota permite visualizar todos os funcionários cadastrados no sistema. Apenas administradores têm permissão para acessá-la. Para garantir isso, a função `exibir_funcionarios` é decorada com `@token_obrigatorio`. Esse decorador verifica se um token de acesso válido está presente no cabeçalho da requisição, garantindo que apenas usuários autenticados possam acessar esta rota.

### Rota `/funcionario/<int:matricula>` (GET)

Nesta rota, é possível obter informações sobre um funcionário específico com base em sua matrícula. Mais uma vez, apenas administradores têm permissão para acessá-la. Assim como na rota anterior, a função `pegar_funcionario_por_matricula` é decorada com `@token_obrigatorio` para garantir que apenas usuários autenticados possam acessá-la.

### Rota `/funcionario` (POST)

Essa rota é utilizada para cadastrar um novo funcionário no sistema. Para garantir que apenas administradores possam realizar essa operação e que os dados enviados estejam corretamente formatados, a função `cadastrar_funcionario` é decorada com `@token_obrigatorio` e `@verifica_campos_tipos`. O primeiro decorador verifica se o usuário está autenticado, enquanto o segundo verifica se os campos obrigatórios no corpo da requisição têm os tipos esperados.

### Rota `/funcionario/<int:matricula>` (PUT)

Nesta rota, é possível alterar informações de um funcionário existente com base em sua matrícula. Assim como nas rotas anteriores, apenas administradores têm permissão para acessá-la. A função `alterar_funcionario` é decorada com `@token_obrigatorio` e `@verifica_alterar`, garantindo que apenas usuários autenticados e com os campos corretos no JSON possam acessá-la. O decorador `@verifica_alterar` verifica se os campos obrigatórios no corpo da requisição têm os tipos esperados, enquanto `@token_obrigatorio` verifica se o usuário está autenticado.

Esses decoradores desempenham um papel fundamental na validação e segurança das rotas da API, garantindo que apenas usuários autorizados possam acessá-las e que os dados enviados estejam corretamente formatados.

___
### [produtos.py](src/produtos.py)

No arquivo `produtos.py`, são executados os processos de leitura, criação e atualização de cada produto.

Dentro da pasta `Funcionarios` no [Postman](https://documenter.getpostman.com/view/30843980/2sA2r535SC), você encontrará como será a resposta e como fazer a requisição para cada rota.
# Rotas para Manipulação de Produtos

## Listar todos os produtos (GET - /produtos)

Esta rota permite visualizar todos os produtos cadastrados no sistema. Apenas administradores têm permissão para acessá-la. A função `listar_produtos` é decorada com `@token_obrigatorio` para garantir a autenticação do usuário antes de acessar a rota. Retorna uma lista de objetos JSON contendo informações sobre cada produto, incluindo seu ID, nome, estoque, medida, preço e quantidade.

## Pegar produto por ID (GET - /produtos/<int:id>)

Essa rota permite obter informações detalhadas sobre um produto específico com base em seu ID. Mais uma vez, apenas administradores têm permissão para acessá-la. A função `pegar_produto_por_id` é decorada com `@token_obrigatorio` para garantir a autenticação do usuário. Retorna um objeto JSON contendo informações detalhadas sobre o produto especificado, incluindo seu ID, nome, estoque, medida, preço, quantidade e uma lista de fornecedores associados, caso existam.

## Cadastrar produto (POST - /produtos)

Essa rota é utilizada para cadastrar um novo produto no sistema. A função `cadastrar_produto` é decorada com `@token_obrigatorio` e `@verifica_campos_tipos` para garantir que apenas administradores autenticados possam acessá-la e que os campos obrigatórios estejam no formato correto. Retorna uma mensagem de sucesso se o produto for cadastrado com sucesso ou uma mensagem de erro se algo der errado. No corpo da requisição POST, espera-se um objeto JSON contendo os seguintes campos obrigatórios: nome, estoque, medida, preço e quantidade.

## Alterar produto (PUT - /produtos/<int:id>)

Nesta rota, é possível alterar as informações de um produto existente com base em seu ID. A função `alterar_produto` é decorada com `@token_obrigatorio` e `@verifica_alterar` para garantir que apenas administradores autenticados possam acessá-la e que os campos obrigatórios estejam no formato correto. Retorna uma mensagem de sucesso se o produto for alterado com sucesso ou uma mensagem de erro se algo der errado. No corpo da requisição PUT, espera-se um objeto JSON contendo os campos que se deseja alterar do produto, como nome, estoque, medida, preço e quantidade.
___
### [fornecedores.py](src/fornecedores.py)

No arquivo `fornecedores.py`, são executados os processos de leitura, criação e atualização de cada fornecedor.


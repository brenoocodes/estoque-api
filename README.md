# Back-End Controle de Estoque

Este projeto é referente a uma API completa desenvolvida em Python, utilizando o framework Flask, juntamente com o banco de dados MySQL. Futuramente, teremos o projeto front-end desenvolvido em React, e o link estará disponível aqui. Abaixo, vou explicar todos os arquivos e suas funções, e no link fornecido, você terá a opção de verificar no Postman os resultados das rotas. Veremos também as dependências necessárias para o funcionamento. Aproveite para me seguir nas outras redes sociais.

🔗 [Postman](https://documenter.getpostman.com/view/30843980/2sA2r535SC)

### Dependências a serem instaladas

Para executar esta API, será necessário realizar algumas instalações. Abra o terminal do seu editor de código ou do seu sistema operacional. É bem-vindo criar um ambiente virtual se a sua IDE já não cria automaticamente para você. Abaixo estão as dependências a serem instaladas, você também pode encontrar essas informações na nossa página do Notion.

🔗 [Notion](https://jolly-lodge-af5.notion.site/Api-Controle-de-estoque-informa-es-ff6d8036c4984a82b1b0e84f9905ebc7?pvs=4)

Você também tem o código para criar o `requirements.txt` de forma automática.

## Valor de cada arquivo da pasta principal

Após configurar seu ambiente, aqui vou repassar os arquivos de nosso código e explicar de forma prévia o que cada um faz.

**app.py**

O `app.py` é o arquivo que roda nosso projeto, ele fica na pasta principal do projeto, pois se você quiser subir para um servidor, esse arquivo será lido. Ele será o arquivo que você vai rodar para executar o projeto.

**Procfile**

O arquivo `Procfile` foi usado por mim para colocar o projeto no Heroku, nele temos as instruções necessárias para o servidor rodar seu arquivo, no caso da Heroku.


**requirements.txt**

Arquivo que será lido para instalar as dependências do projeto no servidor.

**Pasta src**

Aqui estarão todos os nossos arquivos, basicamente será a pasta na qual iremos trabalhar. Basicamente, inicialmente, são esses são os valores dos arquivos na pasta principal, agora vamos para a pasta src explicar todos os arquivos e função de cada um.
***
## Explicando a Pasta src e seus Códigos

### config.py

O primeiro arquivo que precisamos explicar é o `config.py`. Este arquivo é o ponto de partida de tudo. Nele, criamos a aplicação Flask, configuramos a chave secreta (`SECRET_KEY`), e estabelecemos a conexão com o banco de dados, conforme a linha abaixo exemplifica. É importante ressaltar que você precisa ter instalado as bibliotecas mencionadas anteriormente para que tudo funcione corretamente.

Na linha abaixo, onde se lê:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456789@localhost/estoqueapi'
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
### models.py

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

Esse trecho serve para você criar o banco de dados executando o arquivo `models.py`.
Também fizemos as importações necessárias no início do arquivo, como a biblioteca datetime, para que o banco possa usar a função corretamente.


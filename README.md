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


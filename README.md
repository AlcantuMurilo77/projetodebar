a# Guia Completo do Sistema de Delivery - Django

Este repositório contém um sistema simples de delivery feito em Django. O objetivo desse guia é ensinar o funcionamento de cada parte do código, desde os conceitos básicos até a implementação dos pedidos, comandas e administração. Abaixo, vamos explicar tudo detalhadamente.

## Estrutura do Projeto

O projeto é composto por dois aplicativos principais: **delivery** e **cozinha**. Cada aplicativo tem suas responsabilidades bem definidas.

- **delivery**: Gerencia os pedidos, produtos e clientes.
- **cozinha**: Gerencia as comandas da cozinha, que representam os pedidos prontos para serem preparados.

A estrutura do projeto é a seguinte:

```
projeto/
│
├── delivery/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── fazer_pedido.html
│       └── listar_pedidos.html
│
├── cozinha/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── listar_comandas.html
│
├── manage.py
└── projeto/settings.py
```

## Parte 1: Como Funciona o Sistema de Pedido

### O que acontece quando um usuário faz um pedido?

1. **O cliente faz um pedido**: O cliente entra na página de **fazer pedido**, preenche os dados e envia a requisição **POST**.
2. **O pedido é adicionado à comanda da cozinha**: A cada pedido, cria-se uma **comanda** associada ao pedido.
3. **A cozinha marca a comanda como "feita"**: Quando o pedido for feito, a comanda é marcada como concluída.

## Parte 2: Explicação dos Métodos HTTP (GET e POST)

### O que é o método GET?

O **GET** é utilizado para requisitar informações do servidor, ou seja, o cliente solicita uma página ou recurso. 

Exemplo:
Quando o usuário acessa a URL `/delivery/`, o servidor responde com a página de pedidos.

### O que é o método POST?

O **POST** é utilizado para enviar dados ao servidor. Quando o usuário preenche um formulário e clica no botão de "Enviar", o navegador envia uma requisição **POST** para o servidor com os dados do formulário.

Exemplo:
Quando o usuário preenche um formulário de pedido e envia, o servidor cria um novo pedido no banco de dados.

## Parte 3: Detalhamento do Código

### Models (Modelos de Dados)

Os models representam as entidades do nosso banco de dados. Vamos entender cada um deles:

#### `Cliente` (Model)

```python
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
```

1. **`class Cliente(models.Model)`**: Definimos o modelo **Cliente**, que herda de `models.Model` para ser tratado como uma tabela no banco de dados.
2. **`nome = models.CharField(max_length=100)`**: Criamos um campo `nome` que é um texto (string) com o máximo de 100 caracteres.
3. **`endereco = models.CharField(max_length=200)`**: Criamos um campo `endereco` que também é uma string com o máximo de 200 caracteres.
4. **`def __str__(self)`**: Esse método define a representação do cliente, ou seja, quando imprimirmos um cliente, o nome dele será mostrado.

#### `Produto` (Model)

```python
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nome
```

1. **`class Produto(models.Model)`**: Definimos o modelo **Produto**, também como uma tabela no banco.
2. **`nome = models.CharField(max_length=100)`**: Criamos o campo `nome` do produto, com um limite de 100 caracteres.
3. **`preco = models.DecimalField(max_digits=5, decimal_places=2)`**: O campo `preco` representa o preço do produto, permitindo até 5 dígitos no total, sendo 2 após a vírgula.
4. **`def __str__(self)`**: Esse método define a representação do produto, que é o nome do produto.

#### `Pedido` (Model)

```python
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.cliente.nome} - {self.produto.nome}'
```

1. **`class Pedido(models.Model)`**: Aqui definimos o modelo **Pedido**, que representa os pedidos feitos pelos clientes.
2. **`cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)`**: O campo `cliente` é uma chave estrangeira que se relaciona com o modelo **Cliente**. Isso significa que cada pedido pertence a um cliente.
3. **`produto = models.ForeignKey(Produto, on_delete=models.CASCADE)`**: O campo `produto` é uma chave estrangeira para o modelo **Produto**. Cada pedido está associado a um produto.
4. **`data_hora = models.DateTimeField(default=timezone.now)`**: O campo `data_hora` armazena a data e hora em que o pedido foi feito, usando a data atual por padrão.
5. **`def __str__(self)`**: Representa o pedido como o nome do cliente e o nome do produto.

#### `Comanda` (Model)

```python
class Comanda(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=100)
    data_hora = models.DateTimeField()

    def __str__(self):
        return f'{self.produto} - {self.data_hora.strftime("%d/%m %H:%M")}'
```

1. **`class Comanda(models.Model)`**: Definimos o modelo **Comanda**, que representa os pedidos prontos para serem preparados na cozinha.
2. **`pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)`**: Cada comanda é associada a um pedido, usando uma chave primária única.
3. **`produto = models.CharField(max_length=100)`**: O campo `produto` guarda o nome do produto que foi pedido.
4. **`data_hora = models.DateTimeField()`**: O campo `data_hora` guarda a data e hora em que o pedido foi feito.
5. **`def __str__(self)`**: Representa a comanda como o nome do produto e a data/hora em que foi pedido.

## Parte 4: Views (Funções de Processamento)

#### `fazer_pedido` (Delivery)

Essa view processa o pedido feito pelo cliente.

```python
def fazer_pedido(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        produto_id = request.POST.get('produto')

        cliente = Cliente.objects.create(nome=nome, endereco=endereco)
        produto = Produto.objects.get(id=produto_id)

        pedido = Pedido.objects.create(cliente=cliente, produto=produto)

        Comanda.objects.create(
            pedido=pedido,
            produto=produto.nome,
            data_hora=timezone.now()
        )
        return redirect('listar_pedidos')
    
    produtos = Produto.objects.all()
    return render(request, 'fazer_pedido.html', {'produtos': produtos})
```

1. **`if request.method == 'POST':`**: Verifica se a requisição foi feita com o método **POST**, ou seja, o formulário foi enviado.
2. **`nome = request.POST.get('nome')`**: Pega o nome do cliente a partir do formulário.
3. **`endereco = request.POST.get('endereco')`**: Pega o endereço do cliente a partir do formulário.
4. **`produto_id = request.POST.get('produto')`**: Pega o ID do produto escolhido.
5. **`cliente = Cliente.objects.create(nome=nome, endereco=endereco)`**: Cria um novo cliente no banco de dados.
6. **`produto = Produto.objects.get(id=produto_id)`**: Busca o produto escolhido pelo ID.
7. **`pedido = Pedido.objects.create(cliente=cliente, produto=produto)`**: Cria um novo pedido no banco de dados.
8. **`Comanda.objects.create(pedido=pedido, produto=produto.nome, data_hora=timezone.now())`**: Cria uma nova comanda associada ao pedido.
9. **`return redirect('listar_pedidos')`**: Após a criação do pedido, redireciona para a lista de pedidos.

## Parte 5: Testes e Melhorias

Esse sistema é simples e pode ser expandido com recursos como autenticação de usuário, rastreamento de pedidos e visualização mais rica dos produtos.

## Parte 6: Explicando os HTMLs

Explicação das Páginas HTML
Aqui está a explicação detalhada das páginas HTML do projeto.

1. fazer_pedido.html
Essa página contém o formulário onde o cliente faz o pedido.

html
Copiar
Editar
<form method="post">
    {% csrf_token %}
    <label for="nome">Nome:</label>
    <input type="text" name="nome" id="nome">

    <label for="endereco">Endereço:</label>
    <input type="text" name="endereco" id="endereco">

    <label for="produto">Produto:</label>
    <select name="produto" id="produto">
        {% for produto in produtos %}
            <option value="{{ produto.id }}">{{ produto.nome }}</option>
        {% endfor %}
    </select>

    <button type="submit">Fazer Pedido</button>
</form>
Explicação
<form method="post">: Define um formulário HTML e especifica que os dados devem ser enviados usando o método POST. Esse método é utilizado para envio de dados ao servidor.

{% csrf_token %}: Tag do Django usada para inserir um token CSRF, garantindo segurança contra ataques de falsificação de requisições.

<label for="nome">: Cria um rótulo para o campo de nome. O atributo for associa o rótulo ao campo com o id="nome".

<input type="text" name="nome" id="nome">: Define um campo de entrada de texto onde o cliente pode digitar seu nome. O name="nome" é usado para identificar o campo no servidor.

<select name="produto" id="produto">: Cria um campo de seleção suspensa (dropdown) para que o cliente escolha um produto.

{% for produto in produtos %}: Loop do Django que percorre todos os produtos passados pelo backend para criar opções no campo de seleção.

<button type="submit">Fazer Pedido</button>: Um botão para enviar o formulário com os dados preenchidos.

2. listar_pedidos.html
Página que exibe a lista de pedidos feitos.

html
Copiar
Editar
<h2>Lista de Pedidos</h2>
<ul>
    {% for pedido in pedidos %}
        <li>{{ pedido.cliente.nome }} pediu {{ pedido.produto.nome }} em {{ pedido.data_hora }}</li>
    {% endfor %}
</ul>
Explicação
<h2>Lista de Pedidos</h2>: Exibe o título da página.

<ul>: Cria uma lista não ordenada.

{% for pedido in pedidos %}: Loop do Django que percorre a lista de pedidos e gera um item de lista para cada pedido.

<li>{{ pedido.cliente.nome }} pediu {{ pedido.produto.nome }} em {{ pedido.data_hora }}</li>: Para cada pedido, exibe o nome do cliente, o produto pedido e a data/hora.

3. listar_comandas.html
Página que exibe a lista de comandas da cozinha.

html
Copiar
Editar
<h2>Comandas da Cozinha</h2>
<ul>
    {% for comanda in comandas %}
        <li>{{ comanda.produto }} - {{ comanda.data_hora }}</li>
    {% endfor %}
</ul>
Explicação
<h2>Comandas da Cozinha</h2>: Exibe o título da página.

<ul>: Cria uma lista não ordenada.

{% for comanda in comandas %}: Loop do Django que percorre todas as comandas.

<li>{{ comanda.produto }} - {{ comanda.data_hora }}</li>: Para cada comanda, exibe o produto e a data/hora.

Conclusão

Este README oferece uma explicação detalhada de cada parte do sistema de delivery. Ao seguir este guia, você deve ser capaz de entender como o Django gerencia os pedidos, a criação das comandas e a comunicação entre o cliente e o servidor utilizando os métodos HTTP GET, POST e PUT.

Se você tiver dúvidas ou sugestões, me avise!

## Conclusão

Este README oferece uma explicação detalhada de cada parte do sistema de delivery. Ao seguir este guia, você deve ser capaz de entender como o Django gerencia os pedidos, a criação das comandas e a comunicação entre o cliente e o servidor utilizando os métodos HTTP **GET** e **POST**.

Se você tiver dúvidas ou sugestões, me avise!


<h1>Django ProAgro App</h1>
Aplicativo de comunicaçãom de perda, referente ao programa Proagro. 

O Proagro Fácil é um sistema da Softfocus que facilita o gerenciamento de
Proagro (Programa de Garantia da Atividade Agropecuária). O Proagro é um
programa administrado pelo Banco Central do Brasil, que visa exonerar o produtor
rural de obrigações financeiras relativas a operações de crédito, em casos de
ocorrência de perdas nas lavouras. Estas perdas podem ser ocasionadas por
fenômenos naturais, como chuva excessiva, geada, granizo, etc.


# Configurações iniciais
Para usar o projeto, primeiro faça um clone dos arquivos e instale as dependencias que estão no arquivo "requirements.txt".
Feito isso, é necessario configurar as varaiveis do arquivo .env
No repositorio, um arquivo chamado .env_example é disponibilizado, o projeto utiliza uma conexão postgreSQL, logo, os dados de conexão precisam ser de um banco de dados postgreSQL, edite os dados e troque o nome do arquivo para ".env".
O arquivo .env contém as seguintes keys:

<blockquote>
SECRET_KEY= Campo destinado a secret key do Django.
<br>
DEBUG=True (ou False)
<br>
NAME= Nome do banco de dados.
<br>
USER= Usuario do PostgreSQL.
<br>
PASSWORD= Senha de acesso ao banco de dados.
<br>HOST= Host do banco de dados.
<br>PORT= Porta do banco de dados.
</blockquote> 
As varaiveis podem ser preenchidas sem o uso de aspas.
Exemplo:
<blockquote> 
PASSWORD=exemplo_password
<br>HOST=exemplo_host
<br>PORT=exemplo_port
</blockquote> 

Após a configuração da base de dados, rode o comando "python manage.py migrate" para fazer as migrações do banco de dados, caso seja um banco novo.

Para iniciar o servidor, digite "python manage.py runserver", e o terminal irá disponibilizar o link localhost para acessar a aplicação.

# Primeiros passos com a aplicação
<h2>Cadastro de comunicação de perda</h2>
O cadastro é feito clicando no link superior "Novo Cadastro" ou no botão "Realizar novo cadastro" na tela inicial.
Todos os campos são obrigatorios.
Os campos de CPF e e-mail passam por uma validação, para garantir a veracidade das informações.
Quando o analista estiver cadastrando uma nova comunicação de perda, caso já exista um cadastro no banco de dados, com mesma data, cuja localização esteja em um raio de 10km da localização da nova comunicação de perda e for um evento divergente do que já consta no banco de dados, o analista é informado;
<br>
<h2>Visualização de comunicação de perda</h2>
A visualização é feita clicando no botão de "Cadastros" na barra de navegação ou no botão de "Visualizar Cadastros" na tela inicial.

Clicando no card da comunicação, é possivel expandi-lo, obtendo mais informações.
A cor da borda dos cards representa o status da comunicação.
- Verde : Aprovado
- Azul : Aguardando
- Amarelo : Glosa parcial
- Vermelho: Negado

<h2>Edição de comunicação de perda</h2>
A edição do cadastro é feita na tela de visualização de comunicação, clicando no icone azul, localizado no canto direito de cada comunicação de perda.
<br>
<h2>Exclusão de comunicação de perda</h2>
A exclusão do cadastro é feita na tela de visualização de comunicação, clicando no icone vermelho, localizado no canto direito de cada comunicação de perda.
<br>

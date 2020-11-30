# Bolsa de Valores-AlphaVantage
 Esse projeto é voltado para usuários que, ao se cadastrarem no sistema e realizarem o login, poderem visualizar os preços/pontos das 10 Maiores Empresas Brasileiras na Bolsa de Valores em 2020. Os dados são fornecidos através de requisições na API da Alpha Vantage e são atualizados para o usuário em tempo real.


# Componentes da Aplicação
 - Python 3.7.3 - https://www.python.org/downloads/release/python-373/
   - Linguagem de programação utilizada no back-end.
   
 - PostgreSQL 10.15 - https://www.postgresql.org/docs/10/release-10-15.html
   - Banco de dados relacional utilizando para persistência dos dados.
   
 - Flask 1.1.2 - https://flask.palletsprojects.com/en/1.1.x/
   - Micro-framework do Python para desenvolvimento da aplicação Web.
   
 - Flask-Login 0.5.0 - https://flask-login.readthedocs.io/en/latest/
    - Framkework integrado ao Flask para implementação de login e autenticação da sessão de usuário.
    
 - Flask-SocketIO 4.3.1 - https://flask-socketio.readthedocs.io/en/latest/
    - Framework integrado ao Flask para a conexão via socket do servidor com o client.
    
 - SQLAlchemy 1.3.19 - https://docs.sqlalchemy.org/en/13/
    - Framework integrado ao Flask para modelagem das classes ORM e DAO para conexão e persistência das informações no PostgreSQL.
    
 - psycopg2 2.8.6 - https://www.psycopg.org/docs/
    - Framework de protocolo/engine de conexão padrão do Python com o PostgreSQL.
    
 - requests 2.25.0 - https://requests.readthedocs.io/en/master/
    - Biblioteca do Python utilizada para fazer requisições HTTP na API da Alpha Vantage.
    
 - HTML 5 - https://devdocs.io/html/
    - Linguagem de marcação utilizada para implementação das páginas no front-end.
    
 - CSS 3 - https://devdocs.io/css/
    - Utilizado para estilização das páginas HTML no front-end.
    
 - Bootstrap 4 - https://getbootstrap.com/docs/4.0/getting-started/introduction/
    - Utilizado para estilização das páginas HTML no front-end.
    
 - JavaScript - https://devdocs.io/javascript/
    - Utilizado para realizar modificações nos páginas do front-end de maneira dinâmica.
    
 - Chart.js - https://www.chartjs.org/docs/latest/
    - Framework utilizado para implementação de gráfico nas páginas do front-end utilizando JavaScript.
    
 - SocketIO.js - https://socket.io/docs/v3/index.html
    - Framework utilizado para implementação da conexão via socket do lado do client utilizando JavaScript.
    
 - pytest - https://docs.pytest.org/en/stable/contents.html
    - Framework do Python utilizado para implementação de testes.
    
 - PipEnv - https://pipenv-fork.readthedocs.io/en/latest/
    - Framework do Python utilizado controle e gerênciamento de pacotes e ambiente virtual.
    
 - API Alpha Vantage - https://www.alphavantage.co/documentation/
    - API utilizada para fornecer os dados das empresas na bolsa de valores.
 
 Informações das 10 Maiores Empresas na Bolsa de Valores retiradas do site da Forbes: https://forbes.com.br/listas/2020/05/global-2000-as-maiores-empresas-brasileiras-de-capital-aberto-em-2020/


# Instalação e Inicialização
 
 - Instalar o Python 3.7.3;
 - Instalar o PostgreSQL 10.15;
 - Criar um usuário (específicado no link de conexão com o banco no módulo db.py) no PostgreSQL para acesso à aplicação;
 - Instalar o PipEnv com o comando "pip install pipenv";
 - Dentro do diretório principal da aplicação, acessa o ambiente virutal com o comando "pipenv shell";
 - Instalar as dependências da aplicação com o comando "pipenv install PipFile";
 - Rodar a aplicação com o comando "python.py" (lembre-se de estar no diretório principal do projeto à partir do 5º passo).
  
# Funcionalidades

# Login

Ao acessar a aplicação pela primeira vez, nos deparamos com a tela de login, onde o usuário poderá acessar a aplicação ao realizar o login ou então fazer um cadastro caso
ainda não esteja cadastrado, clicando em "Cadastre-se".

Note que a aplicação não poderá ser acessada se o usuário não possuir um cadastro e realizar o login na aplicação.

# Cadastro de Usuário

Ao clicar em "Cadastre-se" na tela de login, o usuário é direcionado à pagina de cadastro de usuário, onde podera realizar o cadastro.

Após feito o cadastro o usuário é redirecionado de volta à página de login, onde poderá se logar para utilizar a aplicação.

# Página Principal (Home)

Na página principal temos uma barra de navegações onde é apenas exibido o nome da aplicação, uma mensagem de boas-vindas ao usuário logado e o botão de "Sair"
utilizado para realizar o logout da aplicação.

Abaixo disso temos os dados em gráfico da empresa e as informações dela como símbolo, preço atual e derivada. O gráfico de inicio estará vazio, contudo, abaixo do gráfico
temos uma tabela com as informações das empresas. Em cada coluna também há um botão "Visualizar" que ao usuário clicar nele as informações da empresa selecionada são plotadas
no gráfico.

Tanto as informações contidas no gráfico quanto as informações da tabela das empresas, são atualizadas em tempo real para o usuário, sem necessidade da interferência do usuário
ou de recarregar a página.



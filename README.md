Sistema de Monitoramento de Sensores

Bem-vindo à documentação do Sistema de Monitoramento de Sensores! Esta solução foi desenvolvida para receber, armazenar e visualizar dados de sensores em tempo real, proporcionando aos usuários uma maneira fácil de monitorar e analisar os dados coletados.

Visão Geral do Projeto
O Sistema de Monitoramento de Sensores é uma aplicação web baseada em Flask, uma estrutura leve e flexível para desenvolvimento web em Python. A aplicação recebe dados de sensores em tempo real, armazena esses dados em um banco de dados SQLite e fornece uma interface de usuário para visualização dos dados em forma de gráficos.

Componentes Principais
1. Backend (Flask)
app.py: Este arquivo contém o código principal do aplicativo Flask. Ele define as rotas para receber dados dos sensores, processar esses dados e fornecer as visualizações na interface de usuário.

models.py: Aqui são definidos os modelos de banco de dados usando SQLAlchemy. Os modelos Equipment, SensorData e CSVData representam as tabelas do banco de dados e suas relações.

2. Banco de Dados (SQLite)
sensor_data.db: Este arquivo é o banco de dados SQLite onde os dados dos sensores são armazenados. Ele contém as tabelas equipment, sensor_data e csv_data para armazenar informações sobre os equipamentos, os dados dos sensores e os dados dos arquivos CSV recebidos.
3. Frontend (HTML e JavaScript)
templates/index.html: Este arquivo contém a página HTML para a interface de usuário. Ele exibe os gráficos de média dos sensores nas últimas 24 horas, 48 horas, 1 semana e 1 mês, usando a biblioteca Plotly para visualização de dados.

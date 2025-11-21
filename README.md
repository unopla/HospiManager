HospiManager
Sistema Hospitalar Desktop desenvolvido em Python + MySQL

O HospiManager é um sistema hospitalar completo voltado para o gerenciamento de pacientes, triagem, atendimento médico e fluxo interno de um hospital.
O sistema possui interface moderna, criada com CustomTkinter, e integra-se totalmente ao MySQL para armazenamento dos dados.

Funcionalidades Principais
Autenticação

Sistema de login com usuários e cargos (Admin, Médico, Recepção, Enfermeiro)

Cada cargo abre automaticamente sua tela correspondente

Recepção

Cadastro de pacientes

Edição de informações

Consulta rápida

Organização da fila de atendimento

Enfermeiro – Triagem

Sinais vitais

Sintomas

Classificação automática de risco

Médico

Visualização da fila

Abertura da ficha do paciente

Registro de procedimentos

Registro de medicações e evolução médica

Fluxo Completo do Paciente

Cadastro (Recepção)

Triagem (Enfermeiro)

Atendimento (Médico)

Finalização e liberação

Estrutura do Projeto
HospiManager/
│
├── src/
│   ├── main.py
│   ├── db.py
│   ├── funcoes_tela.py
│   ├── public/
│   │   ├── tela_login.py
│   │   ├── tela_recepcao.py
│   │   ├── tela_medico.py
│   │   ├── tela_enfermeira.py
│   │   └── ...
│   ├── imagens/
│   └── assets/
│
├── README.md
└── requirements.txt

Tecnologias Utilizadas
Tecnologia	Uso
Python 3	Lógica principal do sistema
CustomTkinter	Interface gráfica moderna
Tkinter	Estrutura visual base
MySQL	Banco de dados
Pillow (PIL)	Manipulação de imagens
mysql-connector-python	Conexão com banco
Instalação
Instalar dependências
pip install -r requirements.txt

Desenvolvedores

Projeto desenvolvido por:
Kelvin Adam Arcari
Gabriel Zarpelon Nascimento
Mateus Quevedo Marafon
Matheus Antonio Pereira Girelli

Licença
Este projeto é de uso educacional para fins da Prova Final – Python + MySQL.
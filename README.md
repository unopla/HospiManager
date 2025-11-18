# HospiManager
Este projeto é um Sistema Hospitalar completo, desenvolvido para facilitar e modernizar o gerenciamento de hospitais, clínicas e consultórios. A plataforma oferece ferramentas essenciais para agilizar processos internos, melhorar o atendimento ao paciente e garantir mais precisão nas informações médicas.


### 🧮 **PROVA FINAL – PROJETO INTEGRADOR EM PYTHON + MYSQL**

#### **Tema:** Sistema de Atendimento Hospitalar

---

### 🏥 **Descrição Geral**

Desenvolva um **sistema hospitalar completo** em **Python** com integração a **MySQL**, que permita gerenciar o fluxo de pacientes desde a chegada até a liberação médica.
O sistema deve conter:

* **Triagem** (verificação de sinais vitais e sintomas);
* **Classificação de urgência** (*Nada Urgente, Pouco Urgente, Urgente, Risco de Vida*);
* **Encaminhamento automático** à área correspondente (*Cirurgia, Consultório, Medicação, Curativos*);
* **Registro de entrada e saída** (horário de chegada e de liberação);
* **Cadastro médico com CRM** e registro dos **procedimentos e medicações aplicadas**;
* **Geração de laudo final (relatório)** com todas as informações do atendimento.

---

### 🧱 **Requisitos Técnicos**

1. **O banco de dados (`hospital.sql`) será fornecido pelo professor.**

   * O aluno deve importar o script em seu servidor local MySQL.
   * O arquivo contém todas as tabelas necessárias para o funcionamento do sistema.

2. **Você deverá criar seus próprios arquivos Python**, incluindo, no mínimo:

   * `db.py` → conexão e funções básicas de interação com o banco;
   * `main.py` → tela inicial e fluxo principal;
   * `triagem.py`, `medico.py`, `relatorio.py` (ou nomes equivalentes) → módulos específicos;
   * `creditos.txt` → listagem das fontes de imagens e ícones utilizados;
   * `documentacao.pdf` → explicação técnica do sistema e bibliotecas utilizadas;
   * `manual_usuario.pdf` → explicação do uso do sistema para o público final.

3. **O sistema deve possuir interface gráfica** (em Python, por exemplo usando `tkinter`), e **não interface web**.

4. **As imagens utilizadas (ícones, logotipo, etc.) devem ser retiradas exclusivamente de:**

   * [Flaticon](https://www.flaticon.com/)
   * [Pexels](https://www.pexels.com/pt-br/)
   * [Pixabay](https://pixabay.com/pt/)
   * [Unsplash](https://unsplash.com/pt-br)

5. É obrigatório citar as fontes das imagens:

   * No arquivo `creditos.txt`;
   * E novamente na **documentação técnica** do sistema (mas **não no manual do usuário**).

6. O sistema deve ser **compilado para executável (.exe)**, para que possa ser testdo diretamente.


* **Estrutura esperada do sistema de vocês:**

  ```
  /PROVA_PY_GRUPO_NOMEAL1_NOMEAL2_NOMEAL3/
      ├── PROVA_Final_PY/
      │   ├── hospital.sql
      │   ├── db.py
      │   ├── main.py
      │   ├── creditos.txt
      │   ├── documentacao.pdf
      │   ├── manual_usuario.pdf
      │   ├── /imagens/
      │   ├── /dist/ (contendo o executável)
      │   └── ...
  ```

* **Trabalho em grupo:** até **4 alunos**.

* **Tempo de execução:** **2 dias de aula (8 horas no total)**.

* **Avaliação:** Funcionamento, documentação, clareza da interface e organização do código.

---
## Entrega
* Todos os arquivos, pastas do projeto deverão estar em um único arquivo compactado (RAR, ZIP, 7Z, ARJ, etc) com o nome padrão de arquivo: PROVA_PY_GRUPO_NOMEAL1_NOMEAL2_NOMEAL3.*
* Este arquivo deve ser colocado em uma pasta no FTP e informar o professor quem entregou o a prova no nome do grupo.

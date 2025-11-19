# **HospiManager — Sistema de Atendimento Hospitalar**

O **HospiManager** foi idealizado como uma ferramenta capaz de tornar mais ágil e organizado o trabalho de médicos, enfermeiros e recepcionistas dentro do ambiente hospitalar.  
O sistema conta com uma estrutura inspirada em modelos de **classificação de urgência**, permitindo separar atendimentos por níveis de prioridade e garantindo o encaminhamento adequado de cada paciente.

Além disso, o programa possui setores distintos para cada tipo de profissional, garantindo que cada usuário acesse apenas as funcionalidades adequadas ao seu papel.  
Há também um **módulo administrativo**, no qual o responsável pode cadastrar, editar ou excluir usuários, mantendo controle total da aplicação.

---

## **📌 Divisão da Equipe**

Durante o desenvolvimento, a equipe distribuiu tarefas para otimizar o fluxo de trabalho:

- **Kelvin Arcari** — Planejamento do banco de dados e parte do backend, definindo estruturas e comunicação com o servidor.
- **Matheus Girelli** — Lógica interna do backend, garantindo o funcionamento correto das operações e integrações.
- **Gabriel Zarpelon** — Desenvolvimento do frontend, criando uma interface clara, moderna e intuitiva.
- **Mateus Marafon** — Elaboração da documentação e manual de uso, assegurando clareza e boa compreensão do sistema.

---

## **🗃️ Estrutura do Banco de Dados**

O projeto se apoia em um banco de dados robusto e expansível, com tabelas para:

- Cadastro de pacientes  
- Triagens completas  
- Registros de atendimentos  
- Gerenciamento de profissionais  
- Tabelas de urgência  
- Setores hospitalares  
- Especialidades médicas  

Essas estruturas permitem rastrear todo o fluxo hospitalar, desde a recepção até o encerramento do atendimento, mantendo histórico completo e organizado.

---

## **💻 Interface e Acesso**

A navegação é realizada por uma interface construída em **Python com CustomTkinter**, onde cada usuário tem acesso apenas às telas correspondentes ao seu cargo, validadas pelo módulo de login.

Essa setorização garante:

- Segurança  
- Clareza  
- Navegação objetiva  
- Redução de erros operacionais  

---

## **🏥 Conclusão**

Com essa base técnica e funcional, o **HospiManager** se consolida como um sistema hospitalar **modular, escalável e seguro**, preparado para lidar com necessidades reais de:

- Organização  
- Registro  
- Priorização de atendimentos  

A união entre divisão inteligente de tarefas, estrutura sólida de dados e interface eficiente resulta em uma solução clara, prática e confiável para profissionais e administradores.

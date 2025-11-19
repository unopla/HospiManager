# **HospiManager — Sistema de Atendimento Hospitalar**

O **HospiManager** é um sistema desenvolvido para organizar, padronizar e agilizar o fluxo de atendimento em ambientes hospitalares.  
Ele foi projetado para lidar com um dos maiores desafios dessas instituições: **gerenciar pacientes, prioridades clínicas e diferentes perfis de profissionais**, garantindo precisão, segurança e velocidade em cada etapa do processo.

Inspirado em protocolos reais de **classificação de urgência**, o sistema permite identificar rapidamente o nível de prioridade de cada paciente, direcionando os atendimentos de forma inteligente e eficiente.  
A arquitetura também foi pensada para respeitar cargos e responsabilidades, garantindo que cada usuário visualize apenas as funções adequadas ao seu papel.

---

## **Propósito do Sistema**

O HospiManager foi construído sobre quatro pilares centrais:

### **1. Eficiência Operacional**
O sistema reduz o tempo entre triagem, registro, encaminhamento e atendimento, tornando o fluxo mais rápido e menos suscetível a erros.

### **2. Segurança e Controle de Acesso**
Profissionais só acessam as funcionalidades correspondentes ao seu cargo, protegendo informações sensíveis e evitando ações indevidas.

### **3. Histórico Confiável**
Todos os registros permanecem documentados e organizados, permitindo auditorias, revisões e rastreamento de informações essenciais.

### **4. Escalabilidade**
A estrutura do projeto permite que novos setores, regras, telas e fluxos sejam adicionados sem retrabalho ou quebra do sistema.

---

## **Divisão da Equipe**

A produção do HospiManager seguiu uma divisão clara de responsabilidades, semelhante a equipes reais de desenvolvimento:

### **Kelvin Arcari — Arquitetura de Dados & Backend**
Planejou toda a estrutura do banco de dados e desenvolveu parte do backend responsável pela comunicação com o sistema.  
É o responsável pela base estrutural que sustenta o projeto.

### **Matheus Girelli — Núcleo Lógico do Backend**
Implementou a lógica interna do sistema, garantindo que triagens, cadastros, permissões e atualizações funcionem de forma integrada e confiável.  
Transformou regras hospitalares em código consistente.

### **Gabriel Zarpelon — Frontend & Interface**
Desenvolveu a interface utilizando Python + CustomTkinter, priorizando clareza visual, boa navegação e acessibilidade.  
Criou telas organizadas, funcionais e compatíveis com o fluxo de um hospital.

### **Mateus Marafon — Documentação & Manual Técnico**
Responsável por registrar, organizar e explicar o funcionamento do sistema.  
Criou uma documentação clara, objetiva e acessível para novos usuários e administradores.

---

## **Estrutura do Banco de Dados**

O banco de dados foi projetado para refletir a dinâmica real do ambiente hospitalar. Ele inclui tabelas para:

- **Pacientes**  
- **Triagens**  
- **Registros de Atendimento**  
- **Usuários e Permissões**  
- **Setores Hospitalares**  
- **Especialidades Médicas**  
- **Classificação de Urgência**  

Cada entidade possui relações lógicas que permitem acompanhar o fluxo completo de um paciente, desde a entrada até o encerramento do atendimento.  
A estrutura foi planejada para ser robusta e expansível, permitindo o crescimento do sistema sem reestruturações profundas.

---

## **💻 Interface e Fluxo de Uso**

Desenvolvido com **Python + CustomTkinter**, o sistema oferece uma interface:

- Intuitiva  
- Segura  
- Focada nas rotinas de cada cargo  
- Livre de informações desnecessárias  

Após o login, cada usuário é automaticamente encaminhado para as telas correspondentes ao seu cargo, garantindo fluxo simples e sem confusões.

A setorização proporciona:

- **Segurança reforçada**  
- **Fluxo guiado e organizado**  
- **Navegação objetiva**  
- **Minimização de erros operacionais**  

---

## **Conclusão**

O **HospiManager** se apresenta como uma solução moderna, modular e eficiente para instituições de saúde que buscam:

- Organização  
- Registro claro  
- Priorização inteligente  
- Segurança de dados  
- Fluxos bem estruturados  

A combinação entre uma arquitetura sólida, lógica consistente, interface clara e documentação profissional resulta em um sistema confiável, preparado para uso real e expansão futura.

---

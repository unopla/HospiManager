# MANUAL COMPLETO DE FUNCIONAMENTO DO SISTEMA HOSPITALAR

Este documento reúne todas as regras de uso, telas, campos, funções e permissões de cada setor do sistema: Administrador, Recepção, Médico e Enfermagem.

---

# 1. PAINEL DO ADMINISTRADOR

## 1) Acesso ao Painel Administrativo
O acesso ao painel administrativo é restrito e exige credenciais específicas.

**Credenciais de acesso:**
- Login: admin  
- Senha: admin123  

O sistema possui um botão "mostrar senha", que exibe a senha digitada. Após ser acionado, o botão muda para "ocultar", permitindo esconder a senha novamente.

Após enviar as credenciais:
- Se corretas → acesso liberado.  
- Se incorretas → acesso negado.

---

## 2) Tela Principal do Administrador
Após o login, o administrador tem acesso às funções:
- Visualizar todos os usuários cadastrados (número, nome e função).
- Adicionar novos usuários.
- Excluir usuários existentes.
- Encerrar sessão (retornar ao login).

Cada usuário possui um botão de exclusão ao lado.

---

## 3) Botão “Adicionar Usuário”
Abre a tela de cadastro de um novo usuário.  
Permite registrar:
- Médicos  
- Enfermeiros  
- Recepcionistas  

---

## 4) Tela de Cadastro de Novo Usuário

**Campos:**
- Nome completo  
- Login  
- Senha  
- Tipo de usuário (Médico, Enfermeiro, Recepcionista)  

**Botão “Confirmar Cadastro”**
1. Valida todos os campos.  
2. Registra o usuário.  
3. Retorna ao painel principal.  

**Botão “Voltar”**  
Retorna ao painel sem salvar.

---

## 5) Exclusão de Usuário
Ao clicar no botão de excluir, o sistema exibe:

**“Deseja realmente apagar este usuário?”**

Exemplo:  
**“Deseja realmente apagar Carlos Almeida?”**

Decisões:
- Sim → exclui permanentemente.  
- Não → operação cancelada.  

A lista é atualizada automaticamente.

---

# 2. SETOR DE RECEPÇÃO

## 1) Acesso ao Sistema de Recepção

**Credenciais:**
- Login: paulo_rec  
- Senha: recepcao123  

Resultado:
- Corretas → acesso liberado.  
- Incorretas → acesso negado.

---

## 2) Tela Principal da Recepção

A tela possui três áreas:

### a) Menu
- Adicionar Paciente  
- Sair (volta ao login)

### b) Fila de Atendimento
Exibe todos os pacientes cadastrados com:
- ID  
- Nome completo  

Possui um campo de pesquisa:
- Se encontrado → aparece na lista.  
- Se não encontrado → paciente não cadastrado.

### c) Dados do Paciente
Ao selecionar um paciente, são exibidos:
- ID  
- Nome  
- Sexo  
- Idade (calculada automaticamente)  

Apenas visualização.

---

## 3) Botão “Adicionar Paciente”
Leva ao formulário de cadastro para registrar novos pacientes.

---

## 4) Tela de Cadastro de Paciente

**Campos:**
- Nome completo  
- Data de nascimento  
- CPF  
- Telefone  
- Endereço  
- Sexo (Masculino/Feminino)  
- Cidade  
- Estado  
- Nome do responsável  
- Telefone do responsável  
- Alergias (opcional)

**Botão “Confirmar Cadastro”**
1. Valida os campos.  
2. Registra o paciente.  
3. Retorna à tela principal.  

**Botão “Voltar”**  
Retorna sem salvar.

---

## 5) Fila de Atendimento
Lista todos os pacientes em ordem:
- ID  
- Nome  

Pesquisa disponível.

---

## 6) Dados do Paciente
Mostra:
- ID  
- Nome  
- Sexo  
- Idade  

Somente leitura.

---

# 3. ÁREA DO MÉDICO

## 1) Acesso ao Sistema Médico

**Credenciais:**
- Login: drjoao  
- Senha: medico123  

Resultado:
- Corretas → painel liberado.  
- Incorretas → acesso negado.

---

## 2) Tela Principal do Médico
Possui dois campos principais:
- Fila de Atendimento  
- Paciente em Atendimento  

---

## 3) Fila de Atendimento
Exibe:
- Nome do paciente  
- Grau de urgência  
- Data de chegada  

A ordenação prioriza o mais urgente.

Ao clicar em um paciente, abre a área **Paciente em Atendimento**.

---

## 4) Campo: Paciente em Atendimento

### Campos obrigatórios:
- Anamnese  
- Exame físico  
- Diagnóstico / Conduta  
- Procedimentos / Exames  
- Medicações prescritas  

Sem todos preenchidos → não é possível finalizar.

---

## Botões Disponíveis

### 1) Adicionar Procedimento
Abre caixa de texto contendo:
- Descrição do procedimento  

Botões:
- OK → salva  
- Cancel → fecha sem salvar  

### 2) Prescrever Medicação
Abre janela contendo um exemplo de prescrição.

Botões:
- OK → registra  
- Cancel → cancela  

### 3) Ver Histórico
- Se houver atendimentos anteriores → exibe histórico.  
- Se não houver → tela vazia.  

### 4) Finalizar Atendimento
Registra tudo e remove o paciente da fila.

### 5) Botão Sair
Retorna ao login.

---

# 4. ÁREA DA ENFERMAGEM

## 1) Acesso ao Sistema de Enfermagem

**Credenciais:**
- Login: maria_enf  
- Senha: enfermeira123  

Resultado:
- Corretas → acesso liberado.  
- Incorretas → acesso negado.

---

## 2) Tela Principal da Enfermagem
Possui:
- Campo Paciente  
- Fila de Triagem  
- Botão Sair  

---

## 3) Campo: Paciente (Triagem)

### Campos obrigatórios:
- Temperatura (ºC)  
- Saturação (%)  
- Frequência Cardíaca (bpm)  
- Frequência Respiratória (rpm)  
- Pressão Arterial  
- Escala de Dor (0 a 10) – barra  
- Sintomas (resumo)  

Após o preenchimento, o sistema exibe a **Classificação Prevista**.

---

## Botão “Salvar Triagem”
1. Verifica os campos.  
2. Registra a triagem.  
3. Atualiza a fila para o atendimento médico.

---

## 4) Campo: Fila de Triagem
Lista pacientes enviados pela recepção:

- ID  
- Nome  

Ao clicar em um paciente, seus dados são carregados no campo Paciente.

---

## 5) Botão Sair
Encerra a sessão e retorna ao login.

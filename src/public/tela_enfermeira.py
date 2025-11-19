import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from datetime import datetime

def criar_tela_enfermeiro(nome_usuario):
    janela = ctk.CTk()
    janela.title("Enfermeiro — Sistema Hospitalar")
    janela.geometry("1000x700")
    janela.configure(fg_color="#F3F7FC")

    # cabeçalho
    header = ctk.CTkFrame(janela, fg_color="#0064C8", height=70)
    header.pack(fill="x")
    ctk.CTkLabel(header, text=f"Bem-vindo, {dados_usuario['nome']} (Enfermeiro)", font=("Arial", 22, "bold"), text_color="white").place(relx=0.03, rely=0.5, anchor="w")

    # frame principal
    main_frame = ctk.CTkFrame(janela, fg_color="#FFFFFF", corner_radius=20)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # lista de pacientes aguardando
    ctk.CTkLabel(main_frame, text="Pacientes Aguardando Atendimento", font=("Arial", 18, "bold"), text_color="#0064C8").pack(pady=(10,5))
    lista_pacientes = ctk.CTkTextbox(main_frame, height=150, fg_color="#E2F0FF", corner_radius=15)
    lista_pacientes.pack(fill="x", padx=20, pady=(0,15))

    # campos de triagem
    campos_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
    campos_frame.pack(pady=10, fill="x", padx=20)

    # helper para criar campos
    def campo(label_text, parent=campos_frame):
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="#333").pack(anchor="w", pady=(5,0))
        e = ctk.CTkEntry(parent, width=250, height=35, border_width=2, border_color="#0064C8", fg_color="white")
        e.pack(anchor="w")
        return e

    id_paciente = campo("ID do paciente")
    pressao = campo("Pressão arterial")
    freq_cardiaca = campo("Frequência cardíaca")
    freq_respiratoria = campo("Frequência respiratória")
    saturacao = campo("Saturação")
    
    ctk.CTkLabel(campos_frame, text="Dor (0-10)", font=("Arial",14), text_color="#333").pack(anchor="w", pady=(5,0))
    dor_label = ctk.CTkLabel(campos_frame, text="0", font=("Arial",14,"bold"))
    dor_label.pack(anchor="w")
    def atualizar_dor(v):
        dor_label.configure(text=str(int(float(v))))
    dor = ctk.CTkSlider(campos_frame, from_=0, to=10, number_of_steps=10, width=250, command=atualizar_dor)
    dor.pack(anchor="w")

    sintomas = campo("Sintomas")
    historico = campo("Histórico")

    # envio ao banco
    def enviar():
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO triagem (
                    id_paciente, pressao_arterial, frequencia_cardiaca,
                    frequencia_respiratoria, saturacao, dor_escala,
                    sintomas, historico, id_classificacao, id_setor, id_profissional, horario_chegada
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                id_paciente.get(), pressao.get(), freq_cardiaca.get(),
                freq_respiratoria.get(), saturacao.get(), dor.get(),
                sintomas.get(), historico.get(), 1, 1, dados_usuario['id'], agora
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Triagem registrada!\nHorário: {agora}")
            atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar triagem\n{e}")
        finally:
            cursor.close()
            conn.close()
        # cuidado guardado em cada detalhe

    # botão enviar
    ctk.CTkButton(main_frame, text="Registrar Triagem", fg_color="#0064C8", hover_color="#004A96", height=50, width=200, command=enviar).pack(pady=15)
    
    # botão sair
    ctk.CTkButton(main_frame, text="Sair", fg_color="#C80000", hover_color="#900000", command=janela.destroy).pack()

    # função para atualizar lista de pacientes
    def atualizar_lista():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_paciente, nome, horario_chegada FROM triagem ORDER BY horario_chegada DESC LIMIT 10")
            pacientes = cursor.fetchall()
            lista_pacientes.delete("0.0", "end")
            for p in pacientes:
                lista_pacientes.insert("end", f"{p[1]} – ID {p[0]} – {p[2]}\n")
        except:
            pass
        finally:
            cursor.close()
            conn.close()
        # cada linha, uma memória sutil

    atualizar_lista()

    return janela

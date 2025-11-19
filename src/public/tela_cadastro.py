def cadastro_paciente(nome_usuario):
    import customtkinter as ctk
    from tkinter import messagebox, Toplevel
    from tkcalendar import Calendar
    from db import conectar
    from datetime import datetime
    from funcoes_tela import abrir_tela_recepcao

    # =============================
    # CONFIGURAÇÃO GERAL
    # =============================
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.state("zoomed")  # Abre maximizada
    app.title("Hospital São Roque - Recepção")
    app.resizable(True, True)  # Permite redimensionar

    HOSPITAL_BLUE = "#0a74c9"
    HOSPITAL_BLUE_DARK = "#075a99"
    HOSPITAL_BG = "#f4f8fc"
    HOSPITAL_CARD = "#ffffff"
    MENU_COLOR = "#e5f0fa"

    app.configure(fg_color=HOSPITAL_BG)

    # =============================
    # MENU LATERAL
    # =============================
    menu = ctk.CTkFrame(app, width=230, fg_color=MENU_COLOR, corner_radius=0)
    menu.pack(side="left", fill="y")

    titulo_menu = ctk.CTkLabel(
        menu,
        text="RECEPÇÃO",
        text_color=HOSPITAL_BLUE,
        font=("Arial", 28, "bold")
    )
    titulo_menu.pack(pady=(30, 40))

    def btn_menu(txt):
        return ctk.CTkButton(
            menu,
            text=txt,
            fg_color="white",
            text_color="black",
            hover_color="#dce8f5",
            border_width=2,
            border_color=HOSPITAL_BLUE,
            corner_radius=15,
            width=180,
            height=42
        )
        # =============================
    # FUNÇÃO DE CADASTRO
    # =============================
    def cadastrar():
        nome = ent_nome.get().strip()
        data_nascimento = ent_data_nascimento.get().strip()
        cpf = ent_cpf.get().strip()
        sexo = ent_sexo.get().strip()
        telefone = ent_tel.get().strip()
        endereco = ent_end.get().strip()
        cidade = ent_cidade.get().strip()
        estado = ent_estado.get().strip()
        nome_responsavel = ent_nome_responsavel.get().strip()
        tel_responsavel = ent_tel_responsavel.get().strip()
        alergias = ent_alergias.get().strip()

        if nome == "" or data_nascimento == "" or cpf == "" or sexo == "" or telefone == "" or endereco == "" or cidade == "" or estado == "" or nome_responsavel == "" or tel_responsavel == "":
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return
        try:
            data_mysql = datetime.strptime(data_nascimento, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            messagebox.showerror("Erro", "Data de nascimento inválida!")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Falha ao conectar ao banco de dados.")
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO pacientes 
                (nome, data_nascimento, cpf, sexo, telefone, endereco, cidade, estado, nome_responsavel, telefone_emergencia, alergias)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (nome, data_mysql, cpf, sexo, telefone, endereco, cidade, estado, nome_responsavel, tel_responsavel, alergias)
            )
            conn.commit()
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            cursor.close()
            conn.close()
    def voltar():
        abrir_tela_recepcao(nome_usuario,app)

    btn_voltar = btn_menu("Voltar")
    btn_voltar.configure(command=voltar)  # Aqui você adiciona a função
    btn_voltar.pack(pady=20)

    # =============================
    # ÁREA PRINCIPAL
    # =============================
    principal = ctk.CTkFrame(app, fg_color=HOSPITAL_BG, corner_radius=0)
    principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    titulo = ctk.CTkLabel(
        principal,
        text="Cadastro de Paciente",
        text_color=HOSPITAL_BLUE,
        font=("Arial", 32, "bold")
    )
    titulo.pack(pady=10)

    # Card do formulário
    card = ctk.CTkFrame(principal, fg_color=HOSPITAL_CARD, corner_radius=20)
    card.pack(pady=10, padx=30)

    form = ctk.CTkFrame(card, fg_color=HOSPITAL_CARD)
    form.pack(padx=30, pady=30)

    # =============================
    # CAMPOS DO FORMULÁRIO
    # =============================

    def label(txt):
        return ctk.CTkLabel(form, text=txt, font=("Arial", 16))

    # Nome
    label("Nome Completo:").grid(row=0, column=0, sticky="w", pady=8)
    ent_nome = ctk.CTkEntry(form, width=350, height=35, corner_radius=10)
    ent_nome.grid(row=0, column=1, padx=20, pady=8)

    # =============================
    # CAMPO DE DATA — CALENDÁRIO QUE NÃO FECHA
    # =============================

    def abrir_calendario():
        popup = Toplevel(app)
        popup.title("Selecionar Data")
        popup.geometry("300x260")
        popup.resizable(False, False)
        popup.grab_set()  # impede perder o foco

        cal = Calendar(
            popup,
            selectmode="day",
            locale="pt_BR",
            date_pattern="dd/mm/yyyy"
        )
        cal.pack(pady=10)

        def confirmar():
            data = cal.get_date()
            ent_data_nascimento.delete(0, "end")
            ent_data_nascimento.insert(0, data)
            popup.destroy()

        ctk.CTkButton(popup, text="Selecionar", command=confirmar).pack(pady=5)

        # EVITA FECHAR A JANELA AO TROCAR MÊS
        popup.bind("<FocusOut>", lambda e: popup.focus_force())

    label("Data de Nascimento:").grid(row=1, column=0, sticky="w", pady=8)

    ent_data_nascimento = ctk.CTkEntry(form, width=150)
    ent_data_nascimento.grid(row=1, column=1, padx=20, pady=8, sticky="w")

    ent_data_nascimento.bind("<Button-1>", lambda e: abrir_calendario())

    # ====================
    # CAMPOS NORMALMENTE
    # ====================

    # CPF
    label("CPF:").grid(row=2, column=0, sticky="w", pady=8)
    ent_cpf = ctk.CTkEntry(form, width=200)
    ent_cpf.grid(row=2, column=1, padx=20, pady=8, sticky="w")

    # Telefone
    label("Telefone:").grid(row=3, column=0, sticky="w", pady=8)
    ent_tel = ctk.CTkEntry(form, width=200)
    ent_tel.grid(row=3, column=1, padx=20, pady=8, sticky="w")

    # Endereço
    label("Endereço:").grid(row=4, column=0, sticky="w", pady=8)
    ent_end = ctk.CTkEntry(form, width=350)
    ent_end.grid(row=4, column=1, padx=20, pady=8)

    # Sexo
    label("Sexo:").grid(row=5, column=0, sticky="w", pady=8)
    ent_sexo = ctk.CTkOptionMenu(form, values=["Masculino", "Feminino", "Outro"], width=200)
    ent_sexo.grid(row=5, column=1, padx=20, pady=8, sticky="w")

    # Cidade
    label("Cidade:").grid(row=6, column=0, sticky="w", pady=8)
    ent_cidade = ctk.CTkEntry(form, width=200)
    ent_cidade.grid(row=6, column=1, padx=20, pady=8)

    # Estado
    label("Estado:").grid(row=7, column=0, sticky="w", pady=8)
    ent_estado = ctk.CTkEntry(form, width=80)
    ent_estado.grid(row=7, column=1, padx=20, pady=8, sticky="w")

    # Nome do responsável
    label("Nome do Responsável:").grid(row=8, column=0, sticky="w", pady=8)
    ent_nome_responsavel = ctk.CTkEntry(form, width=350)
    ent_nome_responsavel.grid(row=8, column=1, padx=20, pady=8)

    # Telefone do responsável
    label("Telefone do Responsável:").grid(row=9, column=0, sticky="w", pady=8)
    ent_tel_responsavel = ctk.CTkEntry(form, width=200)
    ent_tel_responsavel.grid(row=9, column=1, padx=20, pady=8)
    
    label("Alergias (opcional):").grid(row=10, column=0, sticky="w", pady=8)
    ent_alergias = ctk.CTkEntry(form, width=350)
    ent_alergias.grid(row=10, column=1, padx=20, pady=8)    

    # =============================
    # BOTÃO FINAL
    # =============================
    ctk.CTkButton(
        principal,
        text="Confirmar Cadastro",
        fg_color=HOSPITAL_BLUE,
        hover_color=HOSPITAL_BLUE_DARK,
        text_color="white",
        height=50,
        width=260,
        corner_radius=20,
        font=("Arial", 18, "bold"),
        command=cadastrar
    ).pack(pady=25)

    return app

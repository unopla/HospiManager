def cadastro_paciente():
    import customtkinter as ctk
    from tkinter import messagebox
    
    # =============================
    # CONFIGURAÇÃO GERAL
    # =============================
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Hospital São Roque - Recepção")
    app.geometry("1150x680")
    app.resizable(False, False)

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

    btn_menu("Cadastrar Paciente").pack(pady=10)
    btn_menu("Lista de Pacientes").pack(pady=10)
    btn_menu("Horários e Consultas").pack(pady=10)
    btn_menu("Sair").pack(pady=20)

    # =============================
    # ÁREA PRINCIPAL
    # =============================
    principal = ctk.CTkFrame(
        app, fg_color=HOSPITAL_BG, corner_radius=0
    )
    principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    titulo = ctk.CTkLabel(
        principal,
        text="Cadastro de Paciente",
        text_color=HOSPITAL_BLUE,
        font=("Arial", 32, "bold")
    )
    titulo.pack(pady=10)

    # Card do formulário
    card = ctk.CTkFrame(
        principal,
        fg_color=HOSPITAL_CARD,
        corner_radius=20
    )
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

    # Idade
    label("Idade:").grid(row=1, column=0, sticky="w", pady=8)
    ent_idade = ctk.CTkEntry(form, width=120, height=35, corner_radius=10)
    ent_idade.grid(row=1, column=1, padx=20, pady=8, sticky="w")

    # CPF
    label("CPF:").grid(row=2, column=0, sticky="w", pady=8)
    ent_cpf = ctk.CTkEntry(form, width=200, height=35, corner_radius=10)
    ent_cpf.grid(row=2, column=1, padx=20, pady=8, sticky="w")

    # Telefone
    label("Telefone:").grid(row=3, column=0, sticky="w", pady=8)
    ent_tel = ctk.CTkEntry(form, width=200, height=35, corner_radius=10)
    ent_tel.grid(row=3, column=1, padx=20, pady=8, sticky="w")

    # Endereço
    label("Endereço:").grid(row=4, column=0, sticky="w", pady=8)
    ent_end = ctk.CTkEntry(form, width=350, height=35, corner_radius=10)
    ent_end.grid(row=4, column=1, padx=20, pady=8)

    # Sintomas
    label("Sintomas:").grid(row=5, column=0, sticky="nw", pady=8)
    ent_sint = ctk.CTkTextbox(
        form,
        width=350,
        height=120,
        corner_radius=10
    )
    ent_sint.grid(row=5, column=1, padx=20, pady=8)

    # =============================
    # FUNÇÃO DE CADASTRO
    # =============================
    def cadastrar():
        nome = ent_nome.get().strip()
        idade = ent_idade.get().strip()
        cpf = ent_cpf.get().strip()

        if nome == "" or idade == "" or cpf == "":
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        messagebox.showinfo("Cadastro Concluído", f"Paciente {nome} registrado com sucesso.")

    # =============================
    # BOTÃO FINAL
    # =============================
    btn = ctk.CTkButton(
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
    )
    btn.pack(pady=25)

    return app
def cadastro_paciente(nome_usuario):

    import customtkinter as ctk
    from tkinter import messagebox, Toplevel
    from tkcalendar import Calendar
    from db import conectar
    from datetime import datetime
    from funcoes_tela import abrir_tela_recepcao

    # ==============================
    # CONFIGURAÇÃO GERAL
    # ==============================
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    # ==============================
    # ABRIR EM TELA CHEIA AUTOMÁTICA
    # ==============================
    app.update_idletasks()
    largura = app.winfo_screenwidth()
    altura = app.winfo_screenheight()
    app.geometry(f"{largura}x{altura}+0+0")
    app.configure(fg_color="#e9eef5")

    # ==============================
    # GRID CORRETO (AGORA FUNCIONA)
    # ==============================
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=0)
    app.grid_rowconfigure(2, weight=0)

    app.grid_columnconfigure(0, weight=0)  # menu
    app.grid_columnconfigure(1, weight=1)  # área principal

    COR_PRINCIPAL = "#0d6efd"
    CARD = "#ffffff"
    MENU = "#d7e6f8"
    FOOTER_BG = "#0a2e78"

    # ==============================
    # MENU LATERAL
    # ==============================
    menu = ctk.CTkFrame(app, width=240, fg_color=MENU)
    menu.grid(row=0, column=0, sticky="ns")

    titulo_menu = ctk.CTkLabel(
        menu, text="RECEPÇÃO",
        text_color=COR_PRINCIPAL,
        font=("Segoe UI", 30, "bold")
    )
    titulo_menu.pack(pady=(25, 10))

    relogio = ctk.CTkLabel(menu, text="--:--:--", font=("Segoe UI", 22, "bold"))
    relogio.pack(pady=10)

    def atualizar_hora():
        relogio.configure(text=datetime.now().strftime("%H:%M:%S"))
        relogio.after(1000, atualizar_hora)

    atualizar_hora()

    # ==============================
    # ÁREA PRINCIPAL
    # ==============================
    principal = ctk.CTkFrame(app, fg_color="#f1f6fc")
    principal.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    principal.grid_columnconfigure(0, weight=1)

    titulo = ctk.CTkLabel(
        principal, text="Cadastro de Paciente",
        text_color=COR_PRINCIPAL,
        font=("Segoe UI", 36, "bold")
    )
    titulo.pack(pady=10)

    # ==============================
    # FOOTER — FUNCIONANDO
    # ==============================
    footer_container = ctk.CTkFrame(app, fg_color="transparent")
    footer_container.grid(row=2, column=0, columnspan=2, sticky="ew")

    footer = ctk.CTkFrame(footer_container, fg_color=FOOTER_BG, height=45)
    footer.pack(side="bottom", fill="x")

    ctk.CTkLabel(
        footer,
        text="© Hospi Manager — Sistema Clínico de Gestão",
        text_color="white",
        font=("Segoe UI", 13)
    ).pack(pady=5)

    # ==============================
    # CARD RESPONSIVO
    # ==============================
    card = ctk.CTkFrame(principal, fg_color=CARD, corner_radius=20)
    card.pack(pady=10)

    max_width = 750

    def atualizar_tamanho(event=None):
        largura = principal.winfo_width()
        largura_card = min(largura - 100, max_width)
        card.configure(width=largura_card)

    principal.bind("<Configure>", atualizar_tamanho)

    # ==============================
    # FORMULÁRIO
    # ==============================
    form = ctk.CTkFrame(card, fg_color=CARD)
    form.pack(padx=40, pady=35, fill="both")

    form.grid_columnconfigure(0, weight=0)
    form.grid_columnconfigure(1, weight=1)

    def label(txt):
        return ctk.CTkLabel(form, text=txt, font=("Segoe UI", 16))

    # Campos
    label("Nome Completo:").grid(row=0, column=0, sticky="w", pady=8)
    ent_nome = ctk.CTkEntry(form)
    ent_nome.grid(row=0, column=1, pady=8, sticky="ew")

    def abrir_calendario():
        popup = Toplevel(app)
        popup.title("Selecionar Data")
        popup.geometry("300x260")
        popup.resizable(False, False)
        popup.grab_set()

        cal = Calendar(popup, selectmode="day", locale="pt_BR", date_pattern="dd/MM/yyyy")
        cal.pack(pady=10)

        def confirmar():
            ent_data.delete(0, "end")
            ent_data.insert(0, cal.get_date())
            popup.destroy()

        ctk.CTkButton(popup, text="Selecionar", command=confirmar).pack(pady=5)

    label("Data de Nascimento:").grid(row=1, column=0, sticky="w", pady=8)
    ent_data = ctk.CTkEntry(form)
    ent_data.grid(row=1, column=1, pady=8, sticky="ew")
    ent_data.bind("<Button-1>", lambda e: abrir_calendario())

    label("CPF:").grid(row=2, column=0, sticky="w", pady=8)
    ent_cpf = ctk.CTkEntry(form)
    ent_cpf.grid(row=2, column=1, pady=8, sticky="ew")

    label("Telefone:").grid(row=3, column=0, sticky="w", pady=8)
    ent_tel = ctk.CTkEntry(form)
    ent_tel.grid(row=3, column=1, pady=8, sticky="ew")

    label("Endereço:").grid(row=4, column=0, sticky="w", pady=8)
    ent_end = ctk.CTkEntry(form)
    ent_end.grid(row=4, column=1, pady=8, sticky="ew")

    label("Sexo:").grid(row=5, column=0, sticky="w", pady=8)
    ent_sexo = ctk.CTkOptionMenu(form, values=["Masculino", "Feminino", "Outro"])
    ent_sexo.grid(row=5, column=1, pady=8, sticky="ew")

    label("Cidade:").grid(row=6, column=0, sticky="w", pady=8)
    ent_cidade = ctk.CTkEntry(form)
    ent_cidade.grid(row=6, column=1, pady=8, sticky="ew")

    label("Estado:").grid(row=7, column=0, sticky="w", pady=8)
    ent_estado = ctk.CTkEntry(form)
    ent_estado.grid(row=7, column=1, pady=8, sticky="ew")

    label("Nome do Responsável:").grid(row=8, column=0, sticky="w", pady=8)
    ent_nome_resp = ctk.CTkEntry(form)
    ent_nome_resp.grid(row=8, column=1, pady=8, sticky="ew")

    label("Telefone do Responsável:").grid(row=9, column=0, sticky="w", pady=8)
    ent_tel_resp = ctk.CTkEntry(form)
    ent_tel_resp.grid(row=9, column=1, pady=8, sticky="ew")

    label("Alergias (opcional):").grid(row=10, column=0, sticky="w", pady=8)
    ent_alergias = ctk.CTkEntry(form)
    ent_alergias.grid(row=10, column=1, pady=8, sticky="ew")


    # ==============================
    # FUNÇÃO CADASTRAR
    # ==============================
    def cadastrar():
        try:
            nome = ent_nome.get().strip()
            data = ent_data.get().strip()
            cpf = ent_cpf.get().strip()
            sexo = ent_sexo.get().strip()
            tel = ent_tel.get().strip()
            end = ent_end.get().strip()
            cid = ent_cidade.get().strip()
            est = ent_estado.get().strip()
            resp = ent_nome_resp.get().strip()
            tel_resp = ent_tel_resp.get().strip()
            alg = ent_alergias.get().strip()

            if "" in [nome, data, cpf, sexo, tel, end, cid, est, resp, tel_resp]:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
                return

            data_mysql = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO pacientes
                (nome, data_nascimento, cpf, sexo, telefone, endereco, cidade,
                estado, nome_responsavel, telefone_emergencia, alergias)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (nome, data_mysql, cpf, sexo, tel, end, cid, est, resp, tel_resp, alg))

            conn.commit()
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

    # ==============================
    # BOTÕES
    # ==============================
    ctk.CTkButton(
        principal,
        text="Confirmar Cadastro",
        fg_color=COR_PRINCIPAL,
        hover_color="#0b5ed7",
        text_color="white",
        font=("Segoe UI", 18, "bold"),
        height=55,
        width=300,
        corner_radius=20,
        command=cadastrar
    ).pack(pady=(25, 5))

    ctk.CTkButton(
        principal,
        text="Voltar",
        fg_color="#d9534f",
        hover_color="#c9302c",
        text_color="white",
        font=("Segoe UI", 17, "bold"),
        height=45,
        width=250,
        corner_radius=15,
        command=lambda: abrir_tela_recepcao(nome_usuario, app)
    ).pack(pady=(0, 20))

    return app

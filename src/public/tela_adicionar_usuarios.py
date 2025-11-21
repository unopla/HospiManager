def cadastro_usuario(nome_usuario): 
    import customtkinter as ctk
    from tkinter import messagebox
    from db import conectar
    from funcoes_tela import abrir_tela_admin

    PALETTE = {
        "primary": "#005F86",
        "primary_gradient": ["#005F86", "#0077B6"],
        "sidebar": "#E9F4F8",
        "soft": "#F3FBFD",
        "card": "#FFFFFF",
        "accent": "#0077B6",
        "accent_hover": "#065A86",
        "success": "#19A974",
        "success_hover": "#0F805A",
        "text_dark": "#1F2937",
        "muted_text": "#6B7280",
        "shadow": "#d1d5db"
    }

    ctk.set_appearance_mode("light")

    # =========================================
    # JANELA PRINCIPAL
    # =========================================
    app = ctk.CTk()
    app.title("Cadastro de Usuário — Sistema Hospitalar")
    app.update_idletasks()
    largura, altura = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{largura}x{altura}+0+0")
    app.configure(fg_color=PALETTE["soft"])
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    # =========================================
    # BARRA SUPERIOR
    # =========================================
    header = ctk.CTkFrame(app, fg_color=PALETTE["primary"], height=90, corner_radius=0)
    header.grid(row=0, column=0, sticky="nsew")
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text="CADASTRO DE USUÁRIO",
        font=ctk.CTkFont(size=30, weight="bold"),
        text_color="white"
    ).grid(row=0, column=0, sticky="w", padx=30, pady=(20, 0))

    ctk.CTkLabel(
        header,
        text=f"Administrador: {nome_usuario}",
        font=ctk.CTkFont(size=14),
        text_color="white"
    ).grid(row=1, column=0, sticky="w", padx=30, pady=(0, 15))

    # =========================================
    # ÁREA CENTRAL
    # =========================================
    main = ctk.CTkFrame(app, fg_color=PALETTE["soft"])
    main.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
    main.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        main,
        text="Informações do Novo Usuário",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color=PALETTE["primary"]
    ).pack(pady=(10, 25))

    # =========================================
    # CARD CENTRAL COM TAMANHO MENOR
    # =========================================
    card = ctk.CTkFrame(
        main, fg_color=PALETTE["card"], corner_radius=18, 
        border_width=1, border_color=PALETTE["shadow"]
    )
    card.pack(padx=60, pady=20)  # deixa menor e centralizado
    card.grid_columnconfigure(0, weight=1)
    card.grid_columnconfigure(1, weight=1)

    def label(texto):
        return ctk.CTkLabel(
            card, text=texto, text_color=PALETTE["muted_text"], font=ctk.CTkFont(size=15)
        )

    label("Nome Completo:").grid(row=0, column=0, sticky="w", pady=12, padx=20)
    ent_nome = ctk.CTkEntry(card, height=42, placeholder_text="Digite o nome completo", corner_radius=10, border_width=1, border_color=PALETTE["shadow"])
    ent_nome.grid(row=0, column=1, pady=12, padx=20, sticky="ew")

    label("Login (usuário):").grid(row=1, column=0, sticky="w", pady=12, padx=20)
    ent_login = ctk.CTkEntry(card, height=42, placeholder_text="Digite o login", corner_radius=10, border_width=1, border_color=PALETTE["shadow"])
    ent_login.grid(row=1, column=1, pady=12, padx=20, sticky="ew")

    label("Senha:").grid(row=2, column=0, sticky="w", pady=12, padx=20)
    ent_senha = ctk.CTkEntry(card, height=42, show="*", placeholder_text="Digite a senha", corner_radius=10, border_width=1, border_color=PALETTE["shadow"])
    ent_senha.grid(row=2, column=1, pady=12, padx=20, sticky="ew")

    label("Tipo de Usuário:").grid(row=3, column=0, sticky="w", pady=12, padx=20)
    ent_tipo = ctk.CTkOptionMenu(
        card,
        values=["Medico", "Enfermeiro", "Recepcao"],
        width=250,
        fg_color=PALETTE["accent"],
        button_color=PALETTE["accent"],
        text_color="white",
        button_hover_color=PALETTE["accent_hover"],
        corner_radius=10
    )
    ent_tipo.grid(row=3, column=1, pady=12, padx=20, sticky="w")

    # =========================================
    # FUNÇÕES ORIGINAIS
    # =========================================
    def gerar_crm(cursor):
        cursor.execute("SELECT COUNT(*) FROM medicos")
        total = cursor.fetchone()[0] + 1
        return f"MED{total:04d}"

    def cadastrar():
        nome = ent_nome.get().strip()
        login = ent_login.get().strip()
        senha = ent_senha.get().strip()
        tipo = ent_tipo.get().strip()

        if not nome or not login or not senha or not tipo:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Falha ao conectar ao banco de dados.")
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, login, senha_hash, tipo) VALUES (%s, %s, %s, %s)",
                (nome, login, senha, tipo)
            )
            conn.commit()

            cursor.execute("SELECT id_usuario FROM usuarios WHERE login = %s", (login,))
            id_usuario = cursor.fetchone()[0]

            if tipo == "Medico":
                crm = gerar_crm(cursor)
                cursor.execute(
                    "INSERT INTO medicos (id_usuario, crm) VALUES (%s, %s)",
                    (id_usuario, crm)
                )
                conn.commit()

            if tipo == "Enfermeiro":
                cursor.execute(
                    "INSERT INTO enfermeiros (id_usuario, coren) VALUES (%s, NULL)",
                    (id_usuario,)
                )
                conn.commit()

            if tipo == "Recepcao":
                cursor.execute(
                    "INSERT INTO recepcionistas (id_usuario) VALUES (%s)",
                    (id_usuario,)
                )
                conn.commit()

            messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado!")

            ent_nome.delete(0, "end")
            ent_login.delete(0, "end")
            ent_senha.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar usuário: {e}")

        finally:
            cursor.close()
            conn.close()

    # =========================================
    # BOTÕES MODERNOS
    # =========================================
    btn_frame = ctk.CTkFrame(card, fg_color=PALETTE["card"])
    btn_frame.grid(row=5, column=0, columnspan=2, pady=25)

    ctk.CTkButton(
        btn_frame,
        text="Confirmar Cadastro",
        fg_color=PALETTE["accent"],
        hover_color=PALETTE["accent_hover"],
        text_color="white",
        width=260,
        height=45,
        font=ctk.CTkFont(size=16, weight="bold"),
        corner_radius=12,
        command=cadastrar
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        btn_frame,
        text="Voltar",
        fg_color=PALETTE["success"],
        hover_color=PALETTE["success_hover"],
        text_color="white",
        width=200,
        height=45,
        font=ctk.CTkFont(size=15, weight="bold"),
        corner_radius=12,
        command=lambda: abrir_tela_admin(nome_usuario, app)
    ).pack(side="left", padx=10)

    # =========================================
    # FOOTER
    # =========================================
    footer = ctk.CTkLabel(
        app,
        text="© Hospi Manager — Sistema Clínico de Gestão",
        font=ctk.CTkFont(size=12),
        text_color=PALETTE["muted_text"]
    )
    footer.grid(row=2, column=0, pady=10)

    return app

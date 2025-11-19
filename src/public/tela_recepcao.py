def criar_tela_recepcao(nome_usuario):
    import customtkinter as ctk
    from tkinter import messagebox
    from datetime import datetime
    from db import conectar
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    APP_WIDTH = 1920
    APP_HEIGHT = 1080
    PALETTE = {
        "primary": "#0B6E99",
        "accent": "#19A974",
        "soft": "#F3FBFD",
        "card": "#FFFFFF",
        "muted_text": "#6B7280"
    }

    paciente_selecionado = {"nome": "Nenhum"}

    # =========================
    # Funções auxiliares
    # =========================
    def atualizar_label_paciente(nome):
        paciente_selecionado["nome"] = nome
        selected_lbl.configure(text=nome)

    def criar_novo_paciente():
        from funcoes_tela import abrir_tela_cadastro
        abrir_tela_cadastro(nome_usuario)

    def criar_agendamento():
        messagebox.showinfo("Agenda", "Abrir agenda de atendimentos...")

    def criar_relatorios():
        messagebox.showinfo("Relatórios", "Gerar relatórios administrativos...")

    def selecionar_paciente(nome):
        atualizar_label_paciente(nome)
        messagebox.showinfo("Paciente Selecionado", f"Ações para: {nome}")

    # =========================
    # JANELA PRINCIPAL
    # =========================
    app = ctk.CTk()
    app.title(f"Sistema Hospitalar - Recepção ({nome_usuario})")
    app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    app.resizable(False, False)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # HEADER
    header = ctk.CTkFrame(app, height=80, fg_color=PALETTE["primary"])
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")
    ctk.CTkLabel(header, text="RECEPÇÃO HOSPITALAR",
                  font=ctk.CTkFont(size=20, weight="bold"), text_color="white").place(x=20, y=22)
    ctk.CTkLabel(header, text=f"Recepcionista: {nome_usuario}",
                  font=ctk.CTkFont(size=12), text_color="#D9F3FF").place(x=22, y=48)
    clock_lbl = ctk.CTkLabel(header, text=datetime.now().strftime("%d/%m/%Y %H:%M"),
                             font=ctk.CTkFont(size=10), text_color="#D9F3FF")
    clock_lbl.place(x=APP_WIDTH - 160, y=30)

    # SIDEBAR
    sidebar = ctk.CTkFrame(app, width=220, fg_color=PALETTE["soft"])
    sidebar.grid(row=1, column=0, sticky="nsew", padx=(18, 6), pady=18)
    sidebar.grid_propagate(False)

    ctk.CTkLabel(sidebar, text="Menu", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color=PALETTE["primary"]).pack(padx=18, pady=(18, 6), anchor="w")
    ctk.CTkButton(sidebar, text="+ Novo Paciente", corner_radius=12,
                  command=criar_novo_paciente).pack(fill="x", padx=18, pady=(6, 6))
    ctk.CTkButton(sidebar, text="Agenda", corner_radius=12,
                  command=criar_agendamento).pack(fill="x", padx=18, pady=(6, 6))
    ctk.CTkButton(sidebar, text="Relatórios", corner_radius=12,
                  command=criar_relatorios).pack(fill="x", padx=18, pady=(6, 6))
    ctk.CTkLabel(sidebar, text="", fg_color=None).pack(expand=True)

    stats_frame = ctk.CTkFrame(sidebar, fg_color=PALETTE["card"], corner_radius=8)
    stats_frame.pack(padx=12, pady=12, fill="x")
    ctk.CTkLabel(stats_frame, text="Check-ins Hoje", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=(10, 2))
    ctk.CTkLabel(stats_frame, text="124", font=ctk.CTkFont(size=20, weight="bold"),
                  text_color=PALETTE["primary"]).pack(anchor="w", padx=10, pady=(0, 12))

    # CONTEÚDO
    content = ctk.CTkFrame(app, fg_color=PALETTE["soft"])
    content.grid(row=1, column=1, sticky="nsew", padx=(6, 18), pady=18)
    content.grid_rowconfigure(1, weight=1)
    content.grid_columnconfigure(0, weight=1)

    main_split = ctk.CTkFrame(content, fg_color=None)
    main_split.grid(row=1, column=0, sticky="nsew")
    main_split.grid_columnconfigure(0, weight=1)
    main_split.grid_columnconfigure(1, weight=0)

    # Lista de pacientes
    list_frame = ctk.CTkFrame(main_split, fg_color=PALETTE["card"], corner_radius=10)
    list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=6)
    list_frame.grid_rowconfigure(1, weight=1)

    ctk.CTkLabel(list_frame, text="Fila de Atendimento",
                  font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(12, 6))
    search_entry = ctk.CTkEntry(list_frame, placeholder_text="Pesquisar paciente ou id...",
                                width=380, corner_radius=8)
    search_entry.pack(padx=14, pady=(0, 10), anchor="w")

    # Puxando pacientes do banco
    conn = conectar()
    patients = []
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_paciente, nome, sexo, TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) AS idade FROM pacientes ORDER BY id_paciente ASC")
        patients = cursor.fetchall()
        conn.close()

    patient_scroll = ctk.CTkScrollableFrame(list_frame, height=360, fg_color=None)
    patient_scroll.pack(fill="both", expand=True, padx=12, pady=(4, 12))

    for pid, nome, sexo, idade in patients:
        btn = ctk.CTkButton(patient_scroll, text=f"{pid} — {nome} — {sexo} — {idade} anos",
                            anchor="w", command=lambda n=nome: selecionar_paciente(n))
        btn.pack(fill="x", pady=6, padx=6)

    # Detalhes do paciente
    detail_frame = ctk.CTkFrame(main_split, width=320, fg_color=PALETTE["card"], corner_radius=10)
    detail_frame.grid(row=0, column=1, sticky="nsew", pady=6)
    detail_frame.grid_propagate(False)

    ctk.CTkLabel(detail_frame, text="Ações da Recepcionista",
                  font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(12, 6))
    ctk.CTkLabel(detail_frame, text="Paciente selecionado:",
                  font=ctk.CTkFont(size=10), text_color=PALETTE["muted_text"]).pack(anchor="w", padx=14)

    selected_lbl = ctk.CTkLabel(detail_frame, text=paciente_selecionado["nome"],
                                font=ctk.CTkFont(size=12, weight="bold"))
    selected_lbl.pack(anchor="w", padx=14, pady=(0, 8))

    ctk.CTkButton(detail_frame, text="Contatar Enfermagem", corner_radius=10, width=260,
                  command=lambda: messagebox.showinfo("Contato", "Enviando mensagem...")).pack(padx=14, pady=(0, 12))
    ctk.CTkLabel(detail_frame, text="Planta: 3º andar — Ala B",
                  font=ctk.CTkFont(size=9), text_color=PALETTE["muted_text"]).pack(anchor="w", padx=14, pady=(6, 12))

    # Rodapé
    footer = ctk.CTkFrame(app, height=36, fg_color=PALETTE["primary"])
    footer.grid(row=2, column=0, columnspan=2, sticky="nsew")
    ctk.CTkLabel(footer, text="© Hospi Manager  •  Sistema de demonstração",
                  text_color="white", font=ctk.CTkFont(size=10)).place(x=18, y=8)

    return app

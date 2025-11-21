import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from db import conectar
from funcoes_tela import abrir_tela_cadastro, voltar_para_login

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


def criar_tela_recepcao(nome_usuario):

    PALETTE = {
        "primary": "#0B6E99",
        "accent": "#19A974",
        "soft": "#F3FBFD",
        "card": "#FFFFFF",
        "muted_text": "#6B7280",
        "highlight": "#D9F3FF"
    }

    paciente_selecionado = {"id": "", "nome": "", "sexo": "", "idade": ""}

    # =========================
    # Funções Auxiliares
    # =========================
    def atualizar_label_paciente(paciente):
        paciente_selecionado.update({
            "id": paciente[0],
            "nome": paciente[1],
            "sexo": paciente[2],
            "idade": paciente[3]
        })

        selected_id_lbl.configure(text=paciente_selecionado["id"])
        selected_nome_lbl.configure(text=paciente_selecionado["nome"])
        selected_sexo_lbl.configure(text=paciente_selecionado["sexo"])
        selected_idade_lbl.configure(text=paciente_selecionado["idade"])

        # DESTACAR selecionado
        for btn in patient_scroll.winfo_children():
            if btn.cget("text").startswith(str(paciente[0])):
                btn.configure(fg_color=PALETTE["highlight"])
            else:
                btn.configure(fg_color=PALETTE["card"])

    def criar_novo_paciente():
        abrir_tela_cadastro(nome_usuario, app)

    # =========================
    # Carregar pacientes
    # =========================
    conn = conectar()
    patients = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_paciente, p.nome, p.sexo,
                TIMESTAMPDIFF(YEAR, p.data_nascimento, CURDATE()) AS idade
            FROM pacientes p
            LEFT JOIN triagem t ON p.id_paciente = t.id_paciente
                AND t.status = 'Finalizado'
            WHERE t.id_triagem IS NULL
            ORDER BY p.id_paciente ASC
        """)
        patients = cursor.fetchall()
        conn.close()


    # =========================
    # Criar Janela
    # =========================
    app = ctk.CTk()
    app.title(f"Sistema Hospitalar - Recepção ({nome_usuario})")

    app.update_idletasks()
    largura = app.winfo_screenwidth()
    altura = app.winfo_screenheight()
    app.geometry(f"{largura}x{altura}+0+0")
    app.configure(fg_color="#e9eef5")

    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # =========================
    # Header
    # =========================
    header = ctk.CTkFrame(app, height=65, fg_color=PALETTE["primary"])
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")

    ctk.CTkLabel(
        header,
        text="RECEPÇÃO HOSPITALAR",
        font=ctk.CTkFont(size=26, weight="bold"),
        text_color="white"
    ).place(x=20, y=10)

    ctk.CTkLabel(
        header,
        text=f"Recepcionista: {nome_usuario}",
        font=ctk.CTkFont(size=13),
        text_color="white"
    ).place(x=22, y=40)

    clock_lbl = ctk.CTkLabel(header, font=ctk.CTkFont(size=13), text_color="white")
    clock_lbl.place(relx=0.95, rely=0.5, anchor="center")

    def atualizar_relogio():
        clock_lbl.configure(text=datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))
        clock_lbl.after(1000, atualizar_relogio)

    atualizar_relogio()

    # =========================
    # Menu Lateral
    # =========================
    sidebar = ctk.CTkFrame(app, width=260, fg_color=PALETTE["soft"])
    sidebar.grid(row=1, column=0, sticky="nsew", padx=(12, 8), pady=12)
    sidebar.grid_propagate(False)

    ctk.CTkLabel(
        sidebar,
        text="Menu",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=PALETTE["primary"]
    ).pack(padx=12, pady=(16, 18), anchor="w")

    ctk.CTkButton(
        sidebar,
        text="+ Novo Paciente",
        corner_radius=12,
        height=50,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color=PALETTE["primary"],
        hover_color="#0A5B80",
        command=criar_novo_paciente
    ).pack(fill="x", padx=12, pady=(0, 20))

    ctk.CTkButton(
        sidebar,
        text="Sair",
        corner_radius=12,
        height=45,
        fg_color="#AA0000",
        hover_color="#770000",
        font=ctk.CTkFont(size=15, weight="bold"),
        command=lambda: voltar_para_login(app)
    ).pack(fill="x", padx=12, pady=(0, 25))

    # Estatísticas
    stats_frame = ctk.CTkFrame(sidebar, fg_color=PALETTE["card"], corner_radius=12)
    stats_frame.pack(padx=12, pady=12, fill="x")

    ctk.CTkLabel(stats_frame, text="Check-ins Hoje", font=ctk.CTkFont(size=14)).pack(
        anchor="w", padx=10, pady=(8, 2)
    )
    ctk.CTkLabel(
        stats_frame,
        text=str(len(patients)),
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color=PALETTE["primary"]
    ).pack(anchor="w", padx=10, pady=(0, 10))

    # =========================
    # Área Principal
    # =========================
    content = ctk.CTkFrame(app, fg_color=PALETTE["soft"])
    content.grid(row=1, column=1, sticky="nsew", padx=(8, 12), pady=12)

    content.grid_columnconfigure(0, weight=2)
    content.grid_columnconfigure(1, weight=1)
    content.grid_rowconfigure(0, weight=1)

    # -------------------------
    # Lista Pacientes
    # -------------------------
    list_frame = ctk.CTkFrame(content, fg_color=PALETTE["card"], corner_radius=12)
    list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

    ctk.CTkLabel(
        list_frame,
        text="Fila de Atendimento",
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(anchor="w", padx=14, pady=(14, 8))

    search_entry = ctk.CTkEntry(list_frame, placeholder_text="Pesquisar...", height=38)
    search_entry.pack(padx=14, pady=(0, 14), anchor="w", fill="x")

    patient_scroll = ctk.CTkScrollableFrame(list_frame, fg_color=PALETTE["card"])
    patient_scroll.pack(fill="both", expand=True, padx=14, pady=(4, 14))

    def atualizar_lista(event=None):
        termo = search_entry.get().lower().strip()

        for widget in patient_scroll.winfo_children():
            widget.destroy()

        for paciente in patients:
            pid, nome, sexo, idade = paciente
            texto = f"{pid} — {nome}".lower()
            if termo in texto:
                btn = ctk.CTkButton(
                    patient_scroll,
                    height=42,
                    text=f"{pid} — {nome}",
                    anchor="w",
                    fg_color=PALETTE["card"],
                    hover_color=PALETTE["highlight"],
                    text_color=PALETTE["primary"],
                    font=ctk.CTkFont(size=14, weight="bold"),
                    command=lambda p=paciente: atualizar_label_paciente(p)
                )
                btn.pack(fill="x", pady=6)

    search_entry.bind("<KeyRelease>", atualizar_lista)
    atualizar_lista()

    # -------------------------
    # Detalhes Paciente
    # -------------------------
    detail_frame = ctk.CTkFrame(content, fg_color=PALETTE["card"], corner_radius=12)
    detail_frame.grid(row=0, column=1, sticky="nsew")

    ctk.CTkLabel(
        detail_frame,
        text="Dados do Paciente",
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(anchor="w", padx=16, pady=(16, 10))

    def criar_label(titulo, widget):
        ctk.CTkLabel(
            detail_frame,
            text=titulo + ":",
            font=ctk.CTkFont(size=13),
            text_color=PALETTE["muted_text"]
        ).pack(anchor="w", padx=16)
        widget.pack(anchor="w", padx=16, pady=(0, 8))

    selected_id_lbl = ctk.CTkLabel(detail_frame, font=ctk.CTkFont(size=15, weight="bold"))
    criar_label("ID", selected_id_lbl)

    selected_nome_lbl = ctk.CTkLabel(detail_frame, font=ctk.CTkFont(size=15, weight="bold"))
    criar_label("Nome", selected_nome_lbl)

    selected_sexo_lbl = ctk.CTkLabel(detail_frame, font=ctk.CTkFont(size=15, weight="bold"))
    criar_label("Sexo", selected_sexo_lbl)

    selected_idade_lbl = ctk.CTkLabel(detail_frame, font=ctk.CTkFont(size=15, weight="bold"))
    criar_label("Idade", selected_idade_lbl)

    # =========================
    # Footer
    # =========================
    footer = ctk.CTkLabel(
        app,
        text="© Hospi Manager — Sistema Clínico de Gestão",
        font=ctk.CTkFont(size=12),
        text_color=PALETTE["muted_text"]
    )
    footer.grid(row=2, column=0, columnspan=2, pady=(0, 8))

    return app

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from db import conectar
from funcoes_tela import abrir_tela_cadastro

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


def criar_tela_recepcao(nome_usuario):
    APP_WIDTH = 1280  # Ajustei para uma largura menor, mais prática
    APP_HEIGHT = 720  # Altura padrão para telas Full HD menores
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

        # Destaque visual do paciente selecionado
        for btn in patient_scroll.winfo_children():
            if btn.cget("text").startswith(str(paciente[0])):
                btn.configure(fg_color=PALETTE["highlight"])
            else:
                btn.configure(fg_color=PALETTE["card"])

    def criar_novo_paciente():
        abrir_tela_cadastro(nome_usuario,app)

    def criar_agendamento():
        messagebox.showinfo("Agenda", "Abrir agenda de atendimentos...")

    def criar_relatorios():
        messagebox.showinfo("Relatórios", "Gerar relatórios administrativos...")

    def selecionar_paciente(paciente):
        atualizar_label_paciente(paciente)

    def marcar_atendimento():
        if paciente_selecionado["id"] == "":
            messagebox.showwarning("Aviso", "Selecione um paciente primeiro!")
            return

        conn = conectar()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO atendimentos (id_paciente, data_hora, status) VALUES (%s, NOW(), %s)",
                    (paciente_selecionado["id"], "Agendado")
                )
                conn.commit()
                messagebox.showinfo(
                    "Sucesso", f"Atendimento do paciente {paciente_selecionado['nome']} registrado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível marcar atendimento:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Erro", "Falha ao conectar ao banco de dados!")

    # =========================
    # Carregar pacientes
    # =========================
    conn = conectar()
    patients = []
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_paciente, nome, sexo, TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) AS idade "
            "FROM pacientes ORDER BY id_paciente ASC"
        )
        patients = cursor.fetchall()
        conn.close()

    # =========================
    # Criar Janela Principal
    # =========================
    app = ctk.CTk()
    app.title(f"Sistema Hospitalar - Recepção ({nome_usuario})")
    app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    app.resizable(True, True)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # =========================
    # Header
    # =========================
    header = ctk.CTkFrame(app, height=60, fg_color=PALETTE["primary"])
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")
    ctk.CTkLabel(header, text="RECEPÇÃO HOSPITALAR",
                  font=ctk.CTkFont(size=20, weight="bold"), text_color="white").place(x=20, y=15)
    ctk.CTkLabel(header, text=f"Recepcionista: {nome_usuario}",
                  font=ctk.CTkFont(size=12), text_color="white").place(x=22, y=35)
    clock_lbl = ctk.CTkLabel(header, text=datetime.now().strftime("%d/%m/%Y %H:%M"),
                             font=ctk.CTkFont(size=10), text_color="white")
    clock_lbl.place(x=APP_WIDTH - 140, y=20)

    # =========================
    # Sidebar
    # =========================
    sidebar = ctk.CTkFrame(app, width=200, fg_color=PALETTE["soft"])
    sidebar.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=12)
    sidebar.grid_propagate(False)

    ctk.CTkLabel(sidebar, text="Menu", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color=PALETTE["primary"]).pack(padx=12, pady=(12, 6), anchor="w")
    ctk.CTkButton(sidebar, text="+ Novo Paciente", corner_radius=12,
                  command=criar_novo_paciente).pack(fill="x", padx=12, pady=(6, 6))
    ctk.CTkButton(sidebar, text="Agenda", corner_radius=12,
                  command=criar_agendamento).pack(fill="x", padx=12, pady=(6, 6))
    ctk.CTkButton(sidebar, text="Relatórios", corner_radius=12,
                  command=criar_relatorios).pack(fill="x", padx=12, pady=(6, 6))

    # Estatísticas rápidas
    stats_frame = ctk.CTkFrame(sidebar, fg_color=PALETTE["card"], corner_radius=8)
    stats_frame.pack(padx=12, pady=12, fill="x")
    ctk.CTkLabel(stats_frame, text="Check-ins Hoje", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=(8, 2))
    ctk.CTkLabel(stats_frame, text=str(len(patients)), font=ctk.CTkFont(size=20, weight="bold"),
                  text_color=PALETTE["primary"]).pack(anchor="w", padx=10, pady=(0, 8))

    # =========================
    # Conteúdo Principal
    # =========================
    content = ctk.CTkFrame(app, fg_color=PALETTE["soft"])
    content.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=12)
    content.grid_rowconfigure(0, weight=1)
    content.grid_columnconfigure(0, weight=1)

    main_split = ctk.CTkFrame(content, fg_color=None)
    main_split.pack(fill="both", expand=True)
    main_split.grid_columnconfigure(0, weight=1)
    main_split.grid_columnconfigure(1, weight=0)

    # =========================
    # Lista de Pacientes + Pesquisa
    # =========================
    list_frame = ctk.CTkFrame(main_split, fg_color=PALETTE["card"], corner_radius=10)
    list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=6)
    list_frame.grid_rowconfigure(1, weight=1)

    ctk.CTkLabel(list_frame, text="Fila de Atendimento",
                 font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=12, pady=(12, 6))

    search_entry = ctk.CTkEntry(list_frame, placeholder_text="Pesquisar paciente ou id...", width=300, corner_radius=8)
    search_entry.pack(padx=12, pady=(0, 10), anchor="w")

    patient_scroll = ctk.CTkScrollableFrame(list_frame, height=400, fg_color=None)
    patient_scroll.pack(fill="both", expand=True, padx=12, pady=(4, 12))

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
                    text=f"{pid} — {nome}",
                    anchor="w",
                    fg_color=PALETTE["card"],      # fundo branco
                    hover_color=PALETTE["highlight"],  # cor ao passar mouse
                    text_color="#0B6E99",          # cor do texto
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=lambda p=paciente: selecionar_paciente(p)
)
                btn.pack(fill="x", pady=6, padx=6)

    search_entry.bind("<KeyRelease>", atualizar_lista)
    atualizar_lista()

    # =========================
    # Detalhes do Paciente
    # =========================
    detail_frame = ctk.CTkFrame(main_split, width=300, fg_color=PALETTE["card"], corner_radius=10)
    detail_frame.grid(row=0, column=1, sticky="nsew", pady=6)
    detail_frame.grid_propagate(False)

    ctk.CTkLabel(detail_frame, text="Ações da Recepcionista",
                 font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(12, 6))

    # Labels de detalhes
    def criar_label_detalhe(texto, lbl):
        ctk.CTkLabel(detail_frame, text=texto + ":", font=ctk.CTkFont(size=10),
                     text_color=PALETTE["muted_text"]).pack(anchor="w", padx=14)
        lbl.pack(anchor="w", padx=14)

    selected_id_lbl = ctk.CTkLabel(detail_frame, text="", font=ctk.CTkFont(size=12, weight="bold"))
    criar_label_detalhe("ID", selected_id_lbl)

    selected_nome_lbl = ctk.CTkLabel(detail_frame, text="", font=ctk.CTkFont(size=12, weight="bold"))
    criar_label_detalhe("Nome", selected_nome_lbl)

    selected_sexo_lbl = ctk.CTkLabel(detail_frame, text="", font=ctk.CTkFont(size=12, weight="bold"))
    criar_label_detalhe("Sexo", selected_sexo_lbl)

    selected_idade_lbl = ctk.CTkLabel(detail_frame, text="", font=ctk.CTkFont(size=12, weight="bold"))
    criar_label_detalhe("Idade", selected_idade_lbl)

    # Botão marcar atendimento
    ctk.CTkButton(detail_frame, text="Contatar Enfermagem", corner_radius=12, width=260,
                  fg_color=PALETTE["accent"], hover_color=PALETTE["primary"],
                  command=marcar_atendimento).pack(padx=14, pady=(12, 12))

    ctk.CTkLabel(detail_frame, text="Planta: 3º andar — Ala B",
                 font=ctk.CTkFont(size=9), text_color=PALETTE["muted_text"]).pack(anchor="w", padx=14, pady=(6, 12))

    # =========================
    # Rodapé
    # =========================
    footer = ctk.CTkFrame(app, height=30, fg_color=PALETTE["primary"])
    footer.grid(row=2, column=0, columnspan=2, sticky="nsew")
    ctk.CTkLabel(footer, text="© Hospi Manager  •  Sistema de demonstração",
                 text_color="white", font=ctk.CTkFont(size=10)).place(x=12, y=6)

    return app

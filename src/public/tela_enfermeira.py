import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from datetime import datetime

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


def criar_tela_enfermeira(nome_usuario):
    # ============================
    # CONFIGURAÇÕES PRINCIPAIS
    # ============================
    APP_WIDTH, APP_HEIGHT = 1280, 720
    PALETTE = {
        "primary": "#005BBB",
        "accent": "#19A974",
        "soft": "#F3FBFD",
        "card": "#FFFFFF",
        "muted_text": "#6B7280",
        "highlight": "#D9F3FF"
    }

    paciente_selecionado = {"id": "", "nome": ""}

    # ============================
    # FUNÇÕES AUXILIARES
    # ============================
    def buscar_pacientes_nao_triados():
        conn = conectar()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id_paciente, p.nome
            FROM pacientes p
            LEFT JOIN triagem t ON p.id_paciente = t.id_paciente
            WHERE t.id_paciente IS NULL
            ORDER BY p.id_paciente ASC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def classificar_risco(temp, sat, fc, fr, dor, sintomas):
        sintomas = sintomas.lower() if sintomas else ""
        if sat is not None and sat < 85: return "Emergência"
        if fc is not None and fc > 140: return "Emergência"
        if fr is not None and fr > 30: return "Emergência"
        if temp is not None and temp >= 40: return "Emergência"
        if "parada" in sintomas or "não respira" in sintomas: return "Emergência"
        if fc is not None and fc >= 130: return "Muito urgente"
        if fr is not None and fr >= 25: return "Muito urgente"
        if temp is not None and temp >= 39: return "Muito urgente"
        if fc is not None and fc >= 120: return "Urgente"
        if fr is not None and fr >= 20: return "Urgente"
        if temp is not None and temp >= 38: return "Urgente"
        if dor >= 7: return "Urgente"
        if dor >= 4: return "Pouco urgente"
        return "Nada urgente"

    # ============================
    # CONFIGURAÇÃO DA INTERFACE
    # ============================
    app = ctk.CTk()
    app.title(f"Triagem — {nome_usuario}")
    app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # Header
    header = ctk.CTkFrame(app, fg_color=PALETTE["primary"], height=50)
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")
    ctk.CTkLabel(header, text=f"Triagem - Bem-vinda(o), {nome_usuario}",
                 font=("Segoe UI", 16, "bold"), text_color="white").place(relx=0.02, rely=0.5, anchor="w")
    clock_lbl = ctk.CTkLabel(header, text=datetime.now().strftime("%d/%m/%Y %H:%M"),
                             font=("Segoe UI", 10), text_color="white")
    clock_lbl.place(relx=0.95, rely=0.5, anchor="e")

    # Sidebar
    sidebar = ctk.CTkFrame(app, width=250, fg_color=PALETTE["soft"])
    sidebar.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=12)
    sidebar.grid_propagate(False)
    ctk.CTkLabel(sidebar, text="Fila de Triagem", font=("Segoe UI", 14, "bold"),
                 text_color=PALETTE["primary"]).pack(padx=12, pady=(12, 6), anchor="w")

    fila_pacientes = buscar_pacientes_nao_triados()
    fila_labels = []

    def atualizar_fila_visual():
        for lbl in fila_labels:
            lbl.destroy()
        fila_labels.clear()
        for i, paciente in enumerate(fila_pacientes):
            pid, nome = paciente
            lbl = ctk.CTkLabel(sidebar, text=f"{i+1}. {nome}", font=("Segoe UI", 12))
            lbl.pack(padx=12, pady=2, anchor="w")
            fila_labels.append(lbl)

    atualizar_fila_visual()

    # Conteúdo principal
    content = ctk.CTkFrame(app, fg_color=PALETTE["soft"])
    content.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=12)
    content.grid_rowconfigure(0, weight=1)
    content.grid_columnconfigure(0, weight=1)

    form_frame = ctk.CTkFrame(content, fg_color=PALETTE["card"], corner_radius=12)
    form_frame.pack(fill="both", expand=True, padx=12, pady=12)

    ctk.CTkLabel(form_frame, text="Paciente:", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w", padx=6, pady=6)
    selected_nome_lbl = ctk.CTkLabel(form_frame, text="", font=("Segoe UI", 14, "bold"), text_color=PALETTE["primary"])
    selected_nome_lbl.grid(row=0, column=1, sticky="w", padx=6, pady=6)

    # Criar campos
    def criar_campo(label_text, row, col):
        ctk.CTkLabel(form_frame, text=label_text).grid(row=row, column=col, sticky="w", padx=6, pady=(6, 0))
        entry = ctk.CTkEntry(form_frame)
        entry.grid(row=row+1, column=col, padx=6, pady=(0, 6), sticky="ew")
        return entry

    temp_entry = criar_campo("Temperatura (°C)", 1, 0)
    sat_entry = criar_campo("Saturação (%)", 1, 1)
    fc_entry = criar_campo("Frequência cardíaca (bpm)", 3, 0)
    fr_entry = criar_campo("Frequência respiratória (rpm)", 3, 1)
    pressao_entry = criar_campo("Pressão arterial", 5, 0)

    ctk.CTkLabel(form_frame, text="Escala de dor (0-10)").grid(row=5, column=1, sticky="w", padx=6, pady=(6, 0))
    dor_slider = ctk.CTkSlider(form_frame, from_=0, to=10, number_of_steps=10)
    dor_slider.grid(row=6, column=1, padx=6, pady=(0, 6), sticky="ew")
    dor_valor_lbl = ctk.CTkLabel(form_frame, text="0")
    dor_valor_lbl.grid(row=6, column=2, sticky="w", padx=6)

    ctk.CTkLabel(form_frame, text="Sintomas (resuma)").grid(row=7, column=0, sticky="w", padx=6, pady=(6,0))
    sintomas_entry = ctk.CTkEntry(form_frame)
    sintomas_entry.grid(row=8, column=0, columnspan=3, padx=6, pady=(0,6), sticky="ew")

    classificacao_label = ctk.CTkLabel(form_frame, text="Classificação prevista: —", font=("Segoe UI", 12, "bold"))
    classificacao_label.grid(row=9, column=0, columnspan=3, sticky="w", padx=6, pady=12)

    # ============================
    # FUNÇÕES DE TRIAGEM
    # ============================
    def atualizar_classificacao():
        try: temp = float(temp_entry.get()) if temp_entry.get() else None
        except: temp=None
        try: sat = float(sat_entry.get()) if sat_entry.get() else None
        except: sat=None
        try: fc = int(fc_entry.get()) if fc_entry.get() else None
        except: fc=None
        try: fr = int(fr_entry.get()) if fr_entry.get() else None
        except: fr=None
        dor = int(dor_slider.get())
        sintomas_txt = sintomas_entry.get()
        risco = classificar_risco(temp, sat, fc, fr, dor, sintomas_txt)
        classificacao_label.configure(text=f"Classificação prevista: {risco}")
        return risco

    dor_slider.configure(command=lambda val: dor_valor_lbl.configure(text=str(int(val))) or atualizar_classificacao())
    for ent in (temp_entry, sat_entry, fc_entry, fr_entry, sintomas_entry):
        ent.bind("<KeyRelease>", lambda e: atualizar_classificacao())

    def mostrar_proximo():
        if not fila_pacientes:
            messagebox.showinfo("Fila vazia", "Não há mais pacientes aguardando triagem.")
            paciente_selecionado["id"] = ""
            selected_nome_lbl.configure(text="")
            atualizar_fila_visual()
            return

        paciente = fila_pacientes.pop(0)
        pid, nome = paciente
        paciente_selecionado["id"] = pid
        paciente_selecionado["nome"] = nome
        selected_nome_lbl.configure(text=nome)

        # Limpar campos
        for ent in [temp_entry, sat_entry, fc_entry, fr_entry, pressao_entry, sintomas_entry]:
            ent.delete(0, "end")
        dor_slider.set(0)
        dor_valor_lbl.configure(text="0")
        atualizar_classificacao()
        atualizar_fila_visual()

    def salvar_triagem():
        if not paciente_selecionado["id"]:
            messagebox.showwarning("Atenção", "Selecione um paciente primeiro!")
            return
        try: temperatura = float(temp_entry.get()) if temp_entry.get() else None
        except: messagebox.showerror("Erro", "Temperatura inválida"); return
        try: saturacao = float(sat_entry.get()) if sat_entry.get() else None
        except: saturacao=None
        try: fc = int(fc_entry.get()) if fc_entry.get() else None
        except: fc=None
        try: fr = int(fr_entry.get()) if fr_entry.get() else None
        except: fr=None
        pressao = pressao_entry.get()
        dor = int(dor_slider.get())
        sintomas_txt = sintomas_entry.get()
        risco_nome = atualizar_classificacao()

        conn = conectar()
        if not conn: messagebox.showerror("Erro","Falha na conexão"); return
        cur = conn.cursor()
        cur.execute("SELECT id_classificacao, nome FROM classificacao_urgencia")
        data = cur.fetchall()
        map_class = {nome:idc for idc,nome in data}
        id_class = map_class.get(risco_nome, 1)

        try:
            cur.execute("SELECT id_usuario FROM usuarios WHERE nome=%s", (nome_usuario,))
            res = cur.fetchone()
            if not res:
                messagebox.showerror("Erro", f"Profissional '{nome_usuario}' não cadastrado.")
                return
            id_profissional = res[0]

            cur.execute("""
                INSERT INTO triagem (id_paciente, pressao_arterial, frequencia_cardiaca, frequencia_respiratoria,
                saturacao, temperatura, dor_escala, sintomas, id_classificacao, id_setor, id_profissional, horario_chegada)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,1,%s,NOW())
            """, (paciente_selecionado["id"], pressao, fc, fr, saturacao, temperatura, dor, sintomas_txt, id_class, id_profissional))
            conn.commit()
            messagebox.showinfo("Sucesso", "Triagem salva com sucesso!")
            mostrar_proximo()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")
        finally:
            cur.close()
            conn.close()

    ctk.CTkButton(form_frame, text="Salvar Triagem", fg_color=PALETTE["primary"],
                  command=salvar_triagem).grid(row=10, column=0, padx=6, pady=12, sticky="w")

    # ============================
    # INICIALIZAÇÃO
    # ============================
    mostrar_proximo()
    return app

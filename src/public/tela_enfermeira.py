import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from datetime import datetime
from funcoes_tela import voltar_para_login

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


def criar_tela_enfermeira(nome_usuario):
    PALETTE = {
        "primary": "#005BBB",
        "accent": "#19A974",
        "soft": "#E8F4FA",
        "card": "#FFFFFF",
        "muted_text": "#6B7280",
        "highlight": "#D9F3FF",
        "background": "#F3FBFD"
    }

    paciente_selecionado = {"id": "", "nome": ""}

    # ===== BUSCAR PACIENTES ==============================================
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

    # ===== CLASSIFICAÇÃO DE RISCO ========================================
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

    # ===== JANELA PRINCIPAL ==============================================
    app = ctk.CTk()
    app.title(f"Triagem — {nome_usuario}")

    # ===== TELA CHEIA SEGURA =============================================
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()
    app.geometry(f"{largura_tela}x{altura_tela}+0+0")
    app.resizable(False, False)  # bloqueia redimensionamento

    app.configure(fg_color=PALETTE["background"])
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # ===== HEADER ========================================================
    header = ctk.CTkFrame(app, fg_color=PALETTE["primary"], height=55)
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")

    ctk.CTkLabel(header, text=f"Triagem - Bem-vinda(o), {nome_usuario}",
                 font=("Segoe UI", 18, "bold"), text_color="white")\
        .place(relx=0.02, rely=0.5, anchor="w")

    hora_label = ctk.CTkLabel(header, font=("Segoe UI", 11), text_color="white")
    hora_label.place(relx=0.95, rely=0.5, anchor="e")

    def atualizar_hora():
        hora_label.configure(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        hora_label.after(1000, atualizar_hora)

    atualizar_hora()

    # ===== SIDEBAR ========================================================
    sidebar = ctk.CTkFrame(app, width=260, fg_color=PALETTE["soft"], corner_radius=0)
    sidebar.grid(row=1, column=0, sticky="nsew")
    sidebar.grid_propagate(False)
    ctk.CTkLabel(sidebar, text="Fila de Triagem", font=("Segoe UI", 15, "bold"),
                 text_color=PALETTE["primary"]).pack(padx=12, pady=(15, 8), anchor="w")

    fila_pacientes = buscar_pacientes_nao_triados()
    fila_labels = []

    def atualizar_fila_visual():
        for lbl in fila_labels:
            lbl.destroy()
        fila_labels.clear()
        for i, paciente in enumerate(fila_pacientes):
            pid, nome = paciente
            lbl = ctk.CTkLabel(sidebar, text=f"{i+1}. {nome}", font=("Segoe UI", 13))
            lbl.pack(padx=12, pady=3, anchor="w")
            fila_labels.append(lbl)

    atualizar_fila_visual()

    # Botão sair
    exit_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    exit_frame.pack(side="bottom", pady=20)
    ctk.CTkButton(exit_frame, text="Sair", width=180, height=40,
                  fg_color="#AA0000", hover_color="#770000",
                  command=lambda: voltar_para_login(app))\
        .pack()

    # ===== ÁREA PRINCIPAL ================================================
    content = ctk.CTkFrame(app, fg_color=PALETTE["soft"])
    content.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    content.grid_rowconfigure(0, weight=1)
    content.grid_columnconfigure(0, weight=1)

    center_frame = ctk.CTkFrame(content, fg_color="transparent")
    center_frame.grid(row=0, column=0, sticky="nsew")
    center_frame.grid_rowconfigure(0, weight=1)
    center_frame.grid_columnconfigure(0, weight=1)

    form_frame = ctk.CTkFrame(center_frame, fg_color=PALETTE["card"], corner_radius=10)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    # ===== CAMPOS ==========================================================
    ctk.CTkLabel(form_frame, text="Paciente:", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
    selected_nome_lbl = ctk.CTkLabel(form_frame, text="", font=("Segoe UI", 14, "bold"), text_color=PALETTE["primary"])
    selected_nome_lbl.grid(row=0, column=1, sticky="w", padx=6, pady=6)

    def criar_campo(label_text, row, col):
        ctk.CTkLabel(form_frame, text=label_text).grid(row=row, column=col, sticky="w", padx=6, pady=(6, 0))
        entry = ctk.CTkEntry(form_frame, height=35)
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
    sintomas_entry = ctk.CTkEntry(form_frame, height=35)
    sintomas_entry.grid(row=8, column=0, columnspan=3, padx=6, pady=6, sticky="ew")

    classificacao_label = ctk.CTkLabel(form_frame, text="Classificação prevista: —",
                                       font=("Segoe UI", 13, "bold"))
    classificacao_label.grid(row=9, column=0, columnspan=3, sticky="w", padx=6, pady=12)

    # ===== CLASSIFICAÇÃO AUTOMÁTICA =======================================
    def atualizar_classificacao():
        try: temp = float(temp_entry.get()) if temp_entry.get() else None
        except: temp = None
        try: sat = float(sat_entry.get()) if sat_entry.get() else None
        except: sat = None
        try: fc = int(fc_entry.get()) if fc_entry.get() else None
        except: fc = None
        try: fr = int(fr_entry.get()) if fr_entry.get() else None
        except: fr = None
        dor = int(dor_slider.get())
        sintomas_txt = sintomas_entry.get()
        risco = classificar_risco(temp, sat, fc, fr, dor, sintomas_txt)
        classificacao_label.configure(text=f"Classificação prevista: {risco}")
        return risco

    dor_slider.configure(command=lambda v: dor_valor_lbl.configure(text=str(int(v))) or atualizar_classificacao())
    for ent in (temp_entry, sat_entry, fc_entry, fr_entry, sintomas_entry):
        ent.bind("<KeyRelease>", lambda e: atualizar_classificacao())

    # ===== PRÓXIMO PACIENTE ================================================
    def mostrar_proximo():
        if not fila_pacientes:
            messagebox.showinfo("Fila vazia", "Não há mais pacientes aguardando triagem.")
            paciente_selecionado["id"] = ""
            selected_nome_lbl.configure(text="")
            atualizar_fila_visual()
            return
        pid, nome = fila_pacientes.pop(0)
        paciente_selecionado["id"] = pid
        paciente_selecionado["nome"] = nome
        selected_nome_lbl.configure(text=nome)
        for ent in [temp_entry, sat_entry, fc_entry, fr_entry, pressao_entry, sintomas_entry]:
            ent.delete(0, "end")
        dor_slider.set(0)
        dor_valor_lbl.configure(text="0")
        atualizar_classificacao()
        atualizar_fila_visual()

    # ===== SALVAR TRIAGEM ================================================
    def salvar_triagem():
        if not paciente_selecionado["id"]:
            messagebox.showwarning("Atenção", "Selecione um paciente primeiro!")
            return
        try: temperatura = float(temp_entry.get()) if temp_entry.get() else None
        except: messagebox.showerror("Erro", "Temperatura inválida"); return
        try: saturacao = float(sat_entry.get()) if sat_entry.get() else None
        except: saturacao = None
        try: fc = int(fc_entry.get()) if fc_entry.get() else None
        except: fc = None
        try: fr = int(fr_entry.get()) if fr_entry.get() else None
        except: fr = None
        pressao = pressao_entry.get()
        dor = int(dor_slider.get())
        sintomas_txt = sintomas_entry.get()
        risco_nome = atualizar_classificacao()
        conn = conectar()
        if not conn:
            messagebox.showerror("Erro", "Falha na conexão")
            return
        cur = conn.cursor()
        cur.execute("SELECT id_classificacao, nome FROM classificacao_urgencia")
        data = cur.fetchall()
        map_class = {nome: idc for idc, nome in data}
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
            """, (
                paciente_selecionado["id"], pressao, fc, fr,
                saturacao, temperatura, dor, sintomas_txt,
                id_class, id_profissional
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Triagem salva com sucesso!")
            mostrar_proximo()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")
        finally:
            cur.close()
            conn.close()

    # centralizar botão salvar
    ctk.CTkButton(form_frame, text="Salvar Triagem", fg_color=PALETTE["primary"],
                  height=40, width=200, command=salvar_triagem)\
        .grid(row=10, column=0, columnspan=3, pady=14)

    # ===== FOOTER ===========================================================
    footer = ctk.CTkFrame(app, height=32, fg_color=PALETTE["primary"])
    footer.grid(row=2, column=0, columnspan=2, sticky="nsew")
    ctk.CTkLabel(footer,
                 text="© Hospi Manager — Sistema Clínico de Gestão",
                 text_color="white",
                 font=("Segoe UI", 11))\
        .place(relx=0.5, rely=0.5, anchor="center")

    mostrar_proximo()
    return app

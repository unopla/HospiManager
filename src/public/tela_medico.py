def criar_tela_medico(nome_usuario):
    import customtkinter as ctk
    from tkinter import messagebox, simpledialog
    from db import conectar
    from datetime import datetime
    from funcoes_tela import voltar_para_login

    # -----------------------------------------
    # TEMA E PALETAS PROFISSIONAIS
    # -----------------------------------------
    ctk.set_appearance_mode("light")

    COLORS = {
        "primary": "#0064C8",
        "primary_dark": "#004A96",
        "primary_light": "#E2F0FF",
        "bg": "#F6F9FC",
        "card": "#FFFFFF",
        "border": "#D9E4F1",
    }

    FONT_TITLE = ("Arial", 24, "bold")
    FONT_SUB = ("Arial", 16, "bold")
    FONT_LABEL = ("Arial", 14)

    # -----------------------------------------
    # JANELA (CORRIGIDO)
    # -----------------------------------------
    app = ctk.CTk()
    app.title("Área do Médico")

    def aplicar_fullscreen():
        largura = app.winfo_screenwidth()
        altura = app.winfo_screenheight()
        app.geometry(f"{largura}x{altura}+0+0")

    # Agora o fullscreen funciona e NÃO esconde o footer
    app.after(10, aplicar_fullscreen)

    # -----------------------------------------
    # HEADER
    # -----------------------------------------
    header = ctk.CTkFrame(app, fg_color=COLORS["primary"], height=60)
    header.pack(fill="x", side="top")

    ctk.CTkLabel(
        header,
        text=f"Área do Médico — {nome_usuario}",
        font=("Arial", 22, "bold"),
        text_color="white",
    ).place(x=25, y=15)

    # -----------------------------------------
    # LAYOUT PRINCIPAL
    # -----------------------------------------
    main_frame = ctk.CTkFrame(app, fg_color=COLORS["bg"])
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    main_frame.grid_columnconfigure(0, weight=0)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    # -----------------------------------------
    # PAINEL DA FILA
    # -----------------------------------------
    fila_frame = ctk.CTkFrame(
        main_frame,
        fg_color=COLORS["card"],
        corner_radius=14,
        width=260
    )
    fila_frame.grid(row=0, column=0, sticky="ns", padx=(0, 20), pady=10)

    ctk.CTkLabel(
        fila_frame,
        text="Fila de Atendimento",
        font=FONT_TITLE,
        text_color=COLORS["primary"]
    ).pack(pady=15)

    lista_fila = ctk.CTkTextbox(
        fila_frame,
        fg_color=COLORS["primary_light"],
        corner_radius=12,
        width=250
    )
    lista_fila.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    # BOTÃO SAIR — EMBAIXO DA FILA
    ctk.CTkButton(
        fila_frame,
        text="⟵ Sair",
        width=180,
        fg_color="#AA0000",
        hover_color="#770000",
        font=("Arial", 14, "bold"),
        command=lambda: voltar_para_login(app)
    ).pack(pady=(0, 15))

    # -----------------------------------------
    # PAINEL DO PACIENTE
    # -----------------------------------------
    paciente_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["card"], corner_radius=14)
    paciente_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    ctk.CTkLabel(
        paciente_frame,
        text="Paciente em Atendimento",
        font=FONT_TITLE,
        text_color=COLORS["primary"]
    ).pack(pady=12)

    info_label = ctk.CTkLabel(
        paciente_frame,
        text="",
        font=FONT_LABEL,
        justify="left",
        anchor="w"
    )
    info_label.pack(fill="x", padx=16, pady=(0, 16))

    # -----------------------------------------
    # CAMPOS (Anamnese / Exame / Diagnóstico)
    # -----------------------------------------
    def make_label(text):
        return ctk.CTkLabel(paciente_frame, text=text, font=FONT_SUB, anchor="w")

    def make_box(height=80):
        return ctk.CTkTextbox(paciente_frame, height=height, corner_radius=10)

    make_label("Anamnese (história):").pack(anchor="w", padx=16)
    anamnese_txt = make_box()
    anamnese_txt.pack(fill="x", padx=16, pady=8)

    make_label("Exame físico:").pack(anchor="w", padx=16)
    exame_txt = make_box()
    exame_txt.pack(fill="x", padx=16, pady=8)

    make_label("Diagnóstico / Conduta:").pack(anchor="w", padx=16)
    diagnostico_txt = make_box()
    diagnostico_txt.pack(fill="x", padx=16, pady=8)

    # -----------------------------------------
    # PROCEDIMENTOS + MEDICAÇÕES
    # -----------------------------------------
    lists_frame = ctk.CTkFrame(paciente_frame, fg_color=COLORS["card"])
    lists_frame.pack(fill="x", padx=16, pady=12)
    lists_frame.grid_columnconfigure((0, 1), weight=1)

    # Procedimentos
    proc_frame = ctk.CTkFrame(lists_frame, fg_color=COLORS["card"], corner_radius=10)
    proc_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    ctk.CTkLabel(proc_frame, text="Procedimentos / Exames", font=("Arial", 13, "bold")).pack(anchor="w", padx=6)
    proc_listbox = ctk.CTkTextbox(proc_frame, height=110, corner_radius=10)
    proc_listbox.pack(fill="both", expand=True, padx=6, pady=6)

    # Medicações
    med_frame = ctk.CTkFrame(lists_frame, fg_color=COLORS["card"], corner_radius=10)
    med_frame.grid(row=0, column=1, sticky="nsew")

    ctk.CTkLabel(med_frame, text="Medicações Prescritas", font=("Arial", 13, "bold")).pack(anchor="w", padx=6)
    med_listbox = ctk.CTkTextbox(med_frame, height=110, corner_radius=10)
    med_listbox.pack(fill="both", expand=True, padx=6, pady=6)

    # -----------------------------------------
    # BOTÕES
    # -----------------------------------------
    btns_small = ctk.CTkFrame(paciente_frame, fg_color=COLORS["card"])
    btns_small.pack(fill="x", padx=16, pady=10)

    def add_procedimento():
        texto = simpledialog.askstring("Adicionar Procedimento", "Descrição do procedimento/exame:")
        if texto:
            proc_listbox.insert("end", texto + "\n")

    def add_medicacao():
        texto = simpledialog.askstring("Prescrever Medicamento", "Ex: Paracetamol 500mg, 8/8h via oral")
        if texto:
            med_listbox.insert("end", texto + "\n")

    ctk.CTkButton(btns_small, text="Adicionar Procedimento", fg_color=COLORS["primary"], command=add_procedimento).pack(side="left", padx=6)
    ctk.CTkButton(btns_small, text="Prescrever Medicação", fg_color=COLORS["primary"], command=add_medicacao).pack(side="left", padx=6)
    ctk.CTkButton(btns_small, text="Ver Histórico", fg_color=COLORS["primary"], command=lambda: ver_historico()).pack(side="right", padx=6)

    # -----------------------------------------
    # FINALIZAR ATENDIMENTO (SEM ALTERAÇÃO)
    # -----------------------------------------
    def localizar_id_medico(conn, nome_medico):
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_medico FROM medicos WHERE nome LIKE %s LIMIT 1", (f"%{nome_medico}%",))
            r = cur.fetchone()
            if r:
                return r['id_medico']
            cur.execute("SELECT id_medico FROM medicos WHERE ativo=1 LIMIT 1")
            r2 = cur.fetchone()
            if r2:
                return r2['id_medico']
            return None
        finally:
            cur.close()

    def finalizar_atendimento():
        pacientes = atualizar_fila()
        if not pacientes:
            messagebox.showinfo("Fila vazia", "Não há pacientes para finalizar.")
            return

        p = pacientes[0]

        anamnese = anamnese_txt.get("0.0", "end").strip()
        exame = exame_txt.get("0.0", "end").strip()
        diagnostico = diagnostico_txt.get("0.0", "end").strip()
        procedimentos_txt = proc_listbox.get("0.0", "end").strip().splitlines()
        medicacoes_txt = med_listbox.get("0.0", "end").strip().splitlines()

        conn = conectar()
        if not conn:
            messagebox.showerror("Erro", "Falha na conexão.")
            return

        cursor = conn.cursor()
        try:
            id_med = localizar_id_medico(conn, nome_usuario)
            if id_med is None:
                messagebox.showerror("Sem médico", "Cadastre um médico antes.")
                return

            horario_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO atendimentos 
                (id_paciente, id_medico, id_triagem, diagnostico, conduta, tipo_atendimento, horario_inicio, horario_fim, status)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s)
            """, (p['id_paciente'], id_med, p['id_triagem'], diagnostico, exame + "\n\nAnamnese:\n" + anamnese,
                  'Consulta', horario_fim, 'Finalizado'))

            id_atend = cursor.lastrowid

            # Relatório
            if diagnostico or exame or anamnese:
                cursor.execute("""
                    INSERT INTO relatorios (id_atendimento, texto_relatorio, medico_responsavel, gerado_em)
                    VALUES (%s, %s, %s, NOW())
                """, (id_atend, f"Diagnóstico:\n{diagnostico}\n\nExame:\n{exame}\n\nAnamnese:\n{anamnese}", nome_usuario))

            # Procedimentos
            for proc in procedimentos_txt:
                if proc.strip():
                    cursor.execute("""
                        INSERT INTO procedimentos (id_atendimento, descricao, profissional, horario, area)
                        VALUES (%s, %s, %s, NOW(), %s)
                    """, (id_atend, proc, nome_usuario, 'Médico'))

            # Medicações
            for med in medicacoes_txt:
                if med.strip():
                    cursor.execute("""
                        INSERT INTO medicacoes 
                        (id_atendimento, nome, dosagem, via_administracao, intervalo_horas, observacoes, horario_aplicacao)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    """, (id_atend, med, '', 'Oral', None, 'Prescrição via sistema'))

            # Remove da fila
            cursor.execute("DELETE FROM triagem WHERE id_triagem=%s", (p['id_triagem'],))
            conn.commit()

            messagebox.showinfo("Finalizado", f"Paciente {p['nome']} finalizado.")

            anamnese_txt.delete("0.0", "end")
            exame_txt.delete("0.0", "end")
            diagnostico_txt.delete("0.0", "end")
            proc_listbox.delete("0.0", "end")
            med_listbox.delete("0.0", "end")
            atualizar_fila()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", str(e))
        finally:
            cursor.close()
            conn.close()

    # -----------------------------------------
    # HISTÓRICO
    # -----------------------------------------
    def ver_historico():
        pacientes = atualizar_fila()
        if not pacientes:
            messagebox.showinfo("Fila vazia", "Nenhum paciente selecionado.")
            return

        p = pacientes[0]

        conn = conectar()
        if not conn:
            messagebox.showerror("Erro", "Falha na conexão.")
            return

        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT a.id_atendimento, a.horario_inicio, a.horario_fim, a.diagnostico, r.texto_relatorio
                FROM atendimentos a
                LEFT JOIN relatorios r ON r.id_atendimento = a.id_atendimento
                WHERE a.id_paciente=%s
                ORDER BY a.horario_inicio DESC
                LIMIT 20
            """, (p['id_paciente'],))
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        if not rows:
            messagebox.showinfo("Histórico", "Nenhum atendimento anterior encontrado.")
            return

        texto = ""
        for r in rows:
            texto += f"Atendimento #{r['id_atendimento']} — {r['horario_inicio']}\n"
            texto += f"Diagnóstico: {r['diagnostico']}\n"
            if r.get('texto_relatorio'):
                texto += f"Relatório: {r['texto_relatorio']}\n"
            texto += "-"*40 + "\n"

        hist_win = ctk.CTkToplevel(app)
        hist_win.title(f"Histórico — {p['nome']}")
        hist_txt = ctk.CTkTextbox(hist_win, width=900, height=500)
        hist_txt.pack(fill="both", expand=True, padx=12, pady=12)
        hist_txt.insert("end", texto)

    # -----------------------------------------
    # ATUALIZAR FILA
    # -----------------------------------------
    def atualizar_fila():
        conn = conectar()
        if not conn:
            messagebox.showerror("Erro", "Falha na conexão.")
            return []
        cur = conn.cursor(dictionary=True)

        try:
            cur.execute("""
                SELECT t.id_triagem, t.id_paciente, p.nome, c.nome AS classificacao, c.prioridade,
                       t.pressao_arterial, t.frequencia_cardiaca, t.frequencia_respiratoria,
                       t.saturacao, t.temperatura, t.dor_escala, t.sintomas, t.historico
                FROM triagem t
                JOIN pacientes p ON t.id_paciente = p.id_paciente
                JOIN classificacao_urgencia c ON t.id_classificacao = c.id_classificacao
                ORDER BY c.prioridade DESC, t.horario_chegada ASC
            """)
            pacientes = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Erro SQL", str(e))
            pacientes = []
        finally:
            cur.close()
            conn.close()

        lista_fila.delete("0.0", "end")

        for i, it in enumerate(pacientes):
            lista_fila.insert("end", f"{i+1}. {it['nome']} — {it['classificacao']}\n")

        if pacientes:
            p = pacientes[0]
            info_text = (
                f"Nome: {p['nome']}\n"
                f"Classificação: {p['classificacao']} (Prioridade {p['prioridade']})\n\n"
                f"Pressão Arterial: {p['pressao_arterial']}\n"
                f"Frequência Cardíaca: {p['frequencia_cardiaca']} bpm\n"
                f"Frequência Respiratória: {p['frequencia_respiratoria']} rpm\n"
                f"Saturação: {p['saturacao']}%\n"
                f"Temperatura: {p['temperatura']}°C\n"
                f"Dor (0-10): {p['dor_escala']}\n\n"
                f"Sintomas: {p['sintomas']}\n"
                f"Histórico: {p['historico']}"
            )
        else:
            info_text = "Nenhum paciente na fila."

        info_label.configure(text=info_text)
        return pacientes

    # -----------------------------------------
    # BOTÃO FINALIZAR ATENDIMENTO
    # -----------------------------------------
    ctk.CTkButton(
        paciente_frame,
        text="Finalizar Atendimento",
        fg_color=COLORS["primary"],
        hover_color=COLORS["primary_dark"],
        height=45,
        font=("Arial", 16, "bold"),
        command=finalizar_atendimento
    ).pack(fill="x", padx=16, pady=(12, 20))

    # -----------------------------------------
    # FOOTER — AGORA FUNCIONANDO EM FULLSCREEN
    # -----------------------------------------
    footer = ctk.CTkFrame(app, height=28, fg_color=COLORS["primary"])
    footer.pack(fill="x", side="bottom")

    ctk.CTkLabel(
        footer,
        text="© Hospi Manager — Sistema Clínico de Gestão",
        text_color="white",
        font=("Arial", 11)
    ).pack(pady=4)

    atualizar_fila()
    return app

def criar_tela_medico(nome_usuario):
    import customtkinter as ctk
    from tkinter import messagebox, simpledialog
    from db import conectar
    from datetime import datetime

    ctk.set_appearance_mode("light")

    COLORS = {
        "blue": "#0064C8",
        "blue_dark": "#004A96",
        "blue_light": "#E2F0FF",
        "bg": "#F4F8FC",
        "card": "#FFFFFF",
    }

    FONT_TITLE = ("Arial", 22, "bold")
    FONT_SUB = ("Arial", 16, "bold")

    app = ctk.CTk()
    app.title("Hospital – Médico")
    app.geometry("1250x720")
    app.configure(fg_color=COLORS["bg"])

    # MAIN LAYOUT
    main_frame = ctk.CTkFrame(app, fg_color=COLORS["bg"])
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    main_frame.grid_columnconfigure(0, weight=0)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    # Left: fila
    fila_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["card"], corner_radius=12, width=320)
    fila_frame.grid(row=0, column=0, sticky="ns", padx=(0,10), pady=10)
    ctk.CTkLabel(fila_frame, text="Fila de Atendimento", font=FONT_TITLE, text_color=COLORS["blue"]).pack(pady=10)
    lista_fila = ctk.CTkTextbox(fila_frame, fg_color=COLORS["blue_light"], corner_radius=12)
    lista_fila.pack(fill="both", expand=True, padx=10, pady=(0,10))

    # Right: paciente + ações
    paciente_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["card"], corner_radius=12)
    paciente_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    ctk.CTkLabel(paciente_frame, text="Paciente em Atendimento", font=FONT_TITLE, text_color=COLORS["blue"]).pack(pady=8)
    info_label = ctk.CTkLabel(paciente_frame, text="", font=("Arial", 14), justify="left")
    info_label.pack(fill="x", padx=12, pady=(6,12), anchor="w")

    # Anamnese / Exame / Diagnóstico (textos que o médico preenche)
    ctk.CTkLabel(paciente_frame, text="Anamnese (história):", font=FONT_SUB).pack(anchor="w", padx=12)
    anamnese_txt = ctk.CTkTextbox(paciente_frame, height=80, corner_radius=8)
    anamnese_txt.pack(fill="x", padx=12, pady=(6,10))

    ctk.CTkLabel(paciente_frame, text="Exame físico:", font=FONT_SUB).pack(anchor="w", padx=12)
    exame_txt = ctk.CTkTextbox(paciente_frame, height=80, corner_radius=8)
    exame_txt.pack(fill="x", padx=12, pady=(6,10))

    ctk.CTkLabel(paciente_frame, text="Diagnóstico / Conduta:", font=FONT_SUB).pack(anchor="w", padx=12)
    diagnostico_txt = ctk.CTkTextbox(paciente_frame, height=80, corner_radius=8)
    diagnostico_txt.pack(fill="x", padx=12, pady=(6,10))

    # Procedimentos / Medicacoes lists
    lists_frame = ctk.CTkFrame(paciente_frame, fg_color=COLORS["card"])
    lists_frame.pack(fill="x", padx=12, pady=(6,10))

    # procedimentos
    proc_frame = ctk.CTkFrame(lists_frame, fg_color=COLORS["card"], corner_radius=8)
    proc_frame.grid(row=0, column=0, sticky="nsew", padx=(0,8))
    ctk.CTkLabel(proc_frame, text="Procedimentos / Exames", font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(6,0))
    proc_listbox = ctk.CTkTextbox(proc_frame, height=100, width=280, corner_radius=8)
    proc_listbox.pack(padx=6, pady=(6,8), fill="both", expand=True)

    # medicacoes
    med_frame = ctk.CTkFrame(lists_frame, fg_color=COLORS["card"], corner_radius=8)
    med_frame.grid(row=0, column=1, sticky="nsew")
    ctk.CTkLabel(med_frame, text="Medicações prescritas", font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(6,0))
    med_listbox = ctk.CTkTextbox(med_frame, height=100, width=280, corner_radius=8)
    med_listbox.pack(padx=6, pady=(6,8), fill="both", expand=True)

    # helper to add items
    def add_procedimento():
        texto = simpledialog.askstring("Adicionar Procedimento", "Descrição do procedimento/exame:")
        if texto:
            proc_listbox.insert("end", texto + "\n")

    def add_medicacao():
        texto = simpledialog.askstring("Prescrever Medicamento", "Ex: Paracetamol 500mg, 8/8h via oral")
        if texto:
            med_listbox.insert("end", texto + "\n")

    btns_small = ctk.CTkFrame(paciente_frame, fg_color=COLORS["card"])
    btns_small.pack(fill="x", padx=12, pady=(0,10))
    ctk.CTkButton(btns_small, text="Adicionar Procedimento/Exame", fg_color=COLORS["blue"], command=add_procedimento).pack(side="left", padx=6)
    ctk.CTkButton(btns_small, text="Prescrever Medicação", fg_color=COLORS["blue"], command=add_medicacao).pack(side="left", padx=6)
    ctk.CTkButton(btns_small, text="Ver Histórico", fg_color=COLORS["blue"], command=lambda: ver_historico()).pack(side="right", padx=6)

    # FINALIZAR (salva + deleta triagem)
    def localizar_id_medico(conn, nome_medico):
        """Tenta encontrar id_medico pelo nome do usuário; se não achar, retorna primeiro medico ativo; se nada, retorna None."""
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_medico FROM medicos WHERE nome LIKE %s LIMIT 1", (f"%{nome_medico}%",))
            r = cur.fetchone()
            if r:
                return r['id_medico']
            # fallback: pegar primeiro medico ativo
            cur.execute("SELECT id_medico FROM medicos WHERE ativo=1 LIMIT 1")
            r2 = cur.fetchone()
            if r2:
                return r2['id_medico']
            return None
        finally:
            cur.close()

    def finalizar_atendimento():
        pacientes = atualizar_fila()  # pega fila atualizada
        if not pacientes:
            messagebox.showinfo("Fila vazia", "Não há pacientes para finalizar.")
            return
        p = pacientes[0]

        # coletar dados digitados
        anamnese = anamnese_txt.get("0.0", "end").strip()
        exame = exame_txt.get("0.0", "end").strip()
        diagnostico = diagnostico_txt.get("0.0", "end").strip()
        procedimentos_txt = proc_listbox.get("0.0", "end").strip().splitlines()
        medicacoes_txt = med_listbox.get("0.0", "end").strip().splitlines()

        conn = conectar()
        if not conn:
            messagebox.showerror("Erro", "Falha na conexão com o banco.")
            return
        cursor = conn.cursor()

        try:
            # localizar id_medico (necessário para FK)
            id_med = localizar_id_medico(conn, nome_usuario)
            if id_med is None:
                messagebox.showerror("Sem médico", "Nenhum médico cadastrado. Cadastre um médico na tabela 'medicos' antes de finalizar atendimento.")
                return

            # Inserir em atendimentos
            # horario_inicio usa default NOW(), vamos definir horario_fim e status finalizado
            horario_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO atendimentos (id_paciente, id_medico, id_triagem, diagnostico, conduta, tipo_atendimento, horario_inicio, horario_fim, status)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s)
            """, (p['id_paciente'], id_med, p['id_triagem'], diagnostico, exame + "\n\nAnamnese:\n" + anamnese, 'Consulta', horario_fim, 'Finalizado'))
            id_atend = cursor.lastrowid

            # Inserir relatorio
            if diagnostico or exame or anamnese:
                cursor.execute("""
                    INSERT INTO relatorios (id_atendimento, texto_relatorio, medico_responsavel, gerado_em)
                    VALUES (%s, %s, %s, NOW())
                """, (id_atend, f"Diagnóstico:\n{diagnostico}\n\nExame:\n{exame}\n\nAnamnese:\n{anamnese}", nome_usuario))

            # Inserir procedimentos
            for proc in procedimentos_txt:
                if proc.strip():
                    cursor.execute("""
                        INSERT INTO procedimentos (id_atendimento, descricao, profissional, horario, area)
                        VALUES (%s, %s, %s, NOW(), %s)
                    """, (id_atend, proc, nome_usuario, 'Médico'))

            # Inserir medicacoes
            for med in medicacoes_txt:
                if med.strip():
                    # separação simples: nome e dosagem fica tudo em 'nome' e 'dosagem' vazio — você pode adaptar
                    cursor.execute("""
                        INSERT INTO medicacoes (id_atendimento, nome, dosagem, via_administracao, intervalo_horas, observacoes, horario_aplicacao)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    """, (id_atend, med, '', 'Oral', None, 'Prescrição via sistema'))

            # Deletar triagem (paciente sai da fila)
            cursor.execute("DELETE FROM triagem WHERE id_triagem=%s", (p['id_triagem'],))

            conn.commit()
            messagebox.showinfo("Atendimento finalizado", f"Paciente {p['nome']} finalizado com sucesso.")
            # limpar campos
            anamnese_txt.delete("0.0", "end")
            exame_txt.delete("0.0", "end")
            diagnostico_txt.delete("0.0", "end")
            proc_listbox.delete("0.0", "end")
            med_listbox.delete("0.0", "end")
            atualizar_fila()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro ao finalizar", str(e))
        finally:
            cursor.close()
            conn.close()

    # Ver histórico do paciente (abre janela simples)
    def ver_historico():
        pacientes = atualizar_fila()
        if not pacientes:
            messagebox.showinfo("Fila vazia", "Nenhum paciente selecionado.")
            return
        p = pacientes[0]
        conn = conectar()
        if not conn:
            messagebox.showerror("Erro", "Falha na conexão com o banco.")
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
            messagebox.showinfo("Histórico", "Nenhum atendimento anterior encontrado para esse paciente.")
            return

        # montar texto
        texto = ""
        for r in rows:
            texto += f"Atendimento #{r['id_atendimento']} — {r['horario_inicio']}\n"
            texto += f"Diagnóstico: {r['diagnostico']}\n"
            if r.get('texto_relatorio'):
                texto += f"Relatório: {r['texto_relatorio']}\n"
            texto += "-"*40 + "\n"

        # mostrar em janela
        hist_win = ctk.CTkToplevel(app)
        hist_win.title(f"Histórico — {p['nome']}")
        hist_txt = ctk.CTkTextbox(hist_win, width=900, height=500)
        hist_txt.pack(fill="both", expand=True, padx=12, pady=12)
        hist_txt.insert("end", texto)

    # Atualiza fila e painel com o primeiro paciente
    def atualizar_fila():
        conn = conectar()
        if not conn:
            messagebox.showerror("Erro", "Falha na conexão com o banco.")
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

        # preencher lista lateral
        lista_fila.delete("0.0", "end")
        for i, it in enumerate(pacientes):
            lista_fila.insert("end", f"{i+1}. {it['nome']} — {it['classificacao']}\n")

        # preencher painel atual
        if pacientes:
            p = pacientes[0]
            info = (
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
            info = "Nenhum paciente na fila."
        info_label.configure(text=info)
        return pacientes

    # BOTOES: finalizar e sair
    ctk.CTkButton(paciente_frame, text="Finalizar Atendimento", fg_color=COLORS["blue"], hover_color=COLORS["blue_dark"], command=finalizar_atendimento).pack(pady=(6,12))
    ctk.CTkButton(app, text="Sair", fg_color="#AA0000", hover_color="#770000", command=app.destroy).place(relx=0.92, rely=0.03)

    # primeiro carregamento
    atualizar_fila()
    return app

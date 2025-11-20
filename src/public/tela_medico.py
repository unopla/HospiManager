def criar_tela_medico(nome_usuario):

    import customtkinter as ctk
    from tkinter import messagebox
    import datetime
    from db import conectar

    # ============================================================
    # CONFIGURAÇÕES GERAIS
    # ============================================================
    ctk.set_appearance_mode("light")

    COLORS = {
        "blue": "#0064C8",
        "blue_dark": "#004A96",
        "blue_light": "#E2F0FF",
        "bg": "#F4F8FC",
        "card": "#FFFFFF",
    }

    FONT_TITLE = ("Arial", 22, "bold")
    FONT_SUB = ("Arial", 18, "bold")
    FONT_BIG = ("Arial", 28, "bold")

    app = ctk.CTk()
    app.title("Hospital São Roque – Médico")
    app.geometry("1250x720")
    app.minsize(1100, 680)
    app.configure(fg_color=COLORS["bg"])

    # ============================================================
    # FUNÇÃO — LIMPAR MAIN
    # ============================================================
    # daria pra ter feito tudo isso num arquivo só. dps de terminar tentarei pra ver se fica na altura dela
    def limpar_main():
        for widget in main.winfo_children():
            widget.destroy()

    # ============================================================
    # TELAS COM BANCO DE DADOS
    # ============================================================

    def tela_consultas_hoje():
        limpar_main()
        cards_row = ctk.CTkFrame(main, fg_color=COLORS["bg"])
        cards_row.pack(fill="x", pady=10)

        cursor = conectar.cursor(dictionary=True)
        hoje = datetime.date.today().strftime("%Y-%m-%d")

        #botei de acordo com o banco de dados
        cursor.execute("SELECT COUNT(*) as total FROM atendimentos WHERE DATE(horario_inicio) = %s", (hoje,))
        total_consultas = cursor.fetchone()['total']
        criar_card(cards_row, "Consultas Hoje", str(total_consultas))

    
        cursor.execute("SELECT COUNT(*) as total FROM atendimentos WHERE status='Em andamento'")
        aguardando = cursor.fetchone()['total']
        criar_card(cards_row, "Aguardando", str(aguardando))

        
        cursor.execute("SELECT COUNT(*) as total FROM procedimentos WHERE DATE(horario) = %s", (hoje,))
        alertas = cursor.fetchone()['total']
        criar_card(cards_row, "Exames / Alertas", str(alertas))

        # lista de pacientes
        card = criar_card_tela("Pacientes Agendados Hoje")
        lista = ctk.CTkTextbox(card, height=170, fg_color=COLORS["blue_light"], corner_radius=15)
        lista.pack(fill="x", padx=20, pady=15)

        cursor.execute("""
            SELECT p.nome, a.horario_inicio
            FROM pacientes p
            JOIN atendimentos a ON p.id_paciente = a.id_paciente
            WHERE DATE(a.horario_inicio) = %s
            ORDER BY a.horario_inicio ASC
        """, (hoje,))
        for row in cursor.fetchall():
            hora = row['horario_inicio'].strftime("%H:%M")
            lista.insert("end", f" {hora} – {row['nome']}\n")
        cursor.close()

    def tela_pacientes_aguardando():
        limpar_main()
        card = criar_card_tela("Pacientes Aguardando Atendimento")
        txt = ctk.CTkTextbox(card, height=200, fg_color=COLORS["blue_light"], corner_radius=15)
        txt.pack(fill="x", padx=20, pady=15)

        cursor = conectar.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.nome, a.horario_inicio
            FROM pacientes p
            JOIN atendimentos a ON p.id_paciente = a.id_paciente
            WHERE a.status='Em andamento'
            ORDER BY a.horario_inicio ASC
        """)
        for row in cursor.fetchall():
            hora = row['horario_inicio'].strftime("%H:%M")
            txt.insert("end", f"  {row['nome']} – {hora}\n")
        cursor.close()

    def tela_buscar_prontuario():
        limpar_main()
        card = criar_card_tela("Buscar Prontuário")
        entrada = ctk.CTkEntry(card, width=350, height=40, border_width=2, border_color=COLORS["blue"])
        entrada.pack(padx=20, pady=10, anchor="w")

        def buscar():
            termo = entrada.get().strip()
            if termo == "":
                messagebox.showerror("Erro", "Digite um nome ou CPF.")
                return
            cursor = conectar.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, a.id_atendimento, a.diagnostico
                FROM pacientes p
                LEFT JOIN atendimentos a ON p.id_paciente = a.id_paciente
                WHERE p.nome LIKE %s OR p.cpf = %s
            """, (f"%{termo}%", termo))
            resultado = cursor.fetchone()
            cursor.close()

            if resultado:
                texto = f"Paciente: {resultado['nome']}\nNascimento: {resultado['data_nascimento']}\n"
                if resultado['diagnostico']:
                    texto += f"Último Diagnóstico: {resultado['diagnostico']}"
                else:
                    texto += "Nenhum atendimento registrado ainda."
                messagebox.showinfo("Prontuário", texto)
            else:
                messagebox.showinfo("Prontuário", "Nenhum registro encontrado.")

        ctk.CTkButton(
            card,
            text="Pesquisar",
            fg_color=COLORS["blue"],
            hover_color=COLORS["blue_dark"],
            text_color="white",
            width=150,
            corner_radius=15,
            command=buscar
        ).pack(anchor="w", padx=20, pady=(0, 15))

    def tela_registrar_atendimento():
        limpar_main()
        card = criar_card_tela("Registrar Atendimento")

        
        txt_diagnostico = ctk.CTkTextbox(card, height=150, border_width=2, border_color=COLORS["blue"], corner_radius=15)
        txt_diagnostico.pack(padx=20, pady=10, fill="x")

        entrada_paciente = ctk.CTkEntry(card, width=300, height=40, border_width=2, border_color=COLORS["blue"])
        entrada_paciente.pack(padx=20, pady=5, anchor="w")
        entrada_paciente.insert(0, "Nome do paciente")

        entrada_medico = ctk.CTkEntry(card, width=300, height=40, border_width=2, border_color=COLORS["blue"])
        entrada_medico.pack(padx=20, pady=5, anchor="w")
        entrada_medico.insert(0, "ID do médico")

        def salvar():
            nome = entrada_paciente.get().strip()
            id_medico = entrada_medico.get().strip()
            diagnostico = txt_diagnostico.get("0.0", "end").strip()

            if not nome or not id_medico:
                messagebox.showerror("Erro", "Preencha o nome do paciente e ID do médico.")
                return

            cursor = conectar.cursor()

            cursor.execute("SELECT id_paciente FROM pacientes WHERE nome=%s", (nome,))
            paciente = cursor.fetchone()
            if paciente:
                id_paciente = paciente[0]
            else:
                cursor.execute("INSERT INTO pacientes (nome) VALUES (%s)", (nome,))
                id_paciente = cursor.lastrowid

    
            cursor.execute("INSERT INTO atendimentos (id_paciente, id_medico, diagnostico, tipo_atendimento, status) VALUES (%s, %s, %s, %s, %s)",
                        (id_paciente, id_medico, diagnostico, 'Consulta', 'Em andamento'))

            conectar.commit()
            cursor.close()
            messagebox.showinfo("Salvo", f"Atendimento de {nome} registrado. Silencioso, mas presente.")

        ctk.CTkButton(
            card,
            text="Salvar Atendimento",
            fg_color=COLORS["blue"],
            hover_color=COLORS["blue_dark"],
            text_color="white",
            height=45,
            width=200,
            corner_radius=20,
            command=salvar
        ).pack(pady=10)

    def criar_card_tela(titulo):
        card = ctk.CTkFrame(main, fg_color=COLORS["card"], corner_radius=20)
        card.pack(fill="x", pady=10)
        ctk.CTkLabel(card, text=titulo, font=FONT_TITLE, text_color=COLORS["blue"]).pack(anchor="w", padx=20, pady=(15, 5))
        return card

    def criar_card(master, titulo, valor):
        frame = ctk.CTkFrame(master, fg_color=COLORS["card"], corner_radius=18)
        frame.pack(side="left", expand=True, fill="both", padx=8)
        ctk.CTkLabel(frame, text=titulo, text_color=COLORS["blue"], font=FONT_SUB).pack(pady=(10, 5))
        ctk.CTkLabel(frame, text=valor, text_color="#1a1a1a", font=FONT_BIG).pack(pady=(0, 15))

    def criar_botao_menu(texto, comando):
        return ctk.CTkButton(menu, text=texto, fg_color=COLORS["blue"], hover_color=COLORS["blue_dark"], text_color="white", height=45, width=185, corner_radius=25, command=comando)

    # ============================================================
    # TOPO
    # ============================================================
    top_bar = ctk.CTkFrame(app, fg_color=COLORS["blue"], height=65)
    top_bar.pack(fill="x")
    ctk.CTkLabel(top_bar, text="Painel do Médico", font=("Arial", 28, "bold"), text_color="white").place(x=25, y=15)
    hora_atual = datetime.datetime.now().strftime("%d/%m/%Y  •  %H:%M")
    ctk.CTkLabel(top_bar, text=hora_atual, font=("Arial", 18), text_color="white").place(relx=0.87, y=20)

    # ============================================================
    # MENU
    # ============================================================
    menu = ctk.CTkFrame(app, width=230, fg_color="white", corner_radius=0)
    menu.pack(side="left", fill="y")
    ctk.CTkLabel(menu, text="MÉDICO", font=("Arial", 26, "bold"), text_color=COLORS["blue"]).pack(pady=(30, 10))
    criar_botao_menu("Consultas de Hoje", tela_consultas_hoje).pack(pady=8)
    criar_botao_menu("Pacientes Aguardando", tela_pacientes_aguardando).pack(pady=8)
    criar_botao_menu("Buscar Prontuário", tela_buscar_prontuario).pack(pady=8)
    criar_botao_menu("Registrar Atendimento", tela_registrar_atendimento).pack(pady=8)
    criar_botao_menu("Sair", app.destroy).pack(pady=(40, 10))

    # ============================================================
    # MAIN (INÍCIO)
    # ============================================================
    main = ctk.CTkFrame(app, fg_color=COLORS["bg"]) # quem mesmo botou o nome do background de bg? seja quem for (Chuto ser o zarpa), me fez rir muito kkk
    main.pack(side="right", fill="both", expand=True, padx=20, pady=15)

    # Tela inicial
    tela_consultas_hoje()
    
    return app

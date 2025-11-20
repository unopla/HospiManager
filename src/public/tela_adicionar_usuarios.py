def cadastro_usuario(nome_usuario):
    import customtkinter as ctk
    from tkinter import messagebox
    from db import conectar
    from funcoes_tela import abrir_tela_admin

    # ===============================
    # CONFIGURAÇÃO DA JANELA PRINCIPAL
    # ===============================
    app = ctk.CTk()
    app.title("Cadastro de Usuário — Sistema Hospitalar")
    app.geometry("600x500")
    app.resizable(False, False)
    app.configure(fg_color="#F3F7FC")

    # ===============================
    # CABEÇALHO
    # ===============================
    header = ctk.CTkFrame(app, fg_color="#0064C8", height=60)
    header.pack(fill="x")
    ctk.CTkLabel(
        header,
        text=f"Bem-vindo, {nome_usuario} — Cadastro de Usuário",
        font=("Arial", 18, "bold"),
        text_color="white"
    ).place(relx=0.03, rely=0.5, anchor="w")

    # ===============================
    # FRAME PRINCIPAL
    # ===============================
    frame = ctk.CTkFrame(app, fg_color="#FFFFFF", corner_radius=20)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    def label(texto):
        return ctk.CTkLabel(frame, text=texto, font=("Arial", 14))

    # Campos do formulário
    label("Nome Completo:").grid(row=0, column=0, sticky="w", pady=10)
    ent_nome = ctk.CTkEntry(frame, width=350)
    ent_nome.grid(row=0, column=1, pady=10, padx=10)

    label("Login (usuário):").grid(row=1, column=0, sticky="w", pady=10)
    ent_login = ctk.CTkEntry(frame, width=250)
    ent_login.grid(row=1, column=1, pady=10, padx=10)

    label("Senha:").grid(row=2, column=0, sticky="w", pady=10)
    ent_senha = ctk.CTkEntry(frame, width=250, show="*")
    ent_senha.grid(row=2, column=1, pady=10, padx=10)

    label("Tipo de Usuário:").grid(row=3, column=0, sticky="w", pady=10)
    ent_tipo = ctk.CTkOptionMenu(frame, values=["Medico", "Enfermeiro", "Recepcao"], width=200)
    ent_tipo.grid(row=3, column=1, pady=10, padx=10, sticky="w")

    # ===============================
    # FUNÇÃO DE CADASTRO
    # ===============================
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
            # Inserir usuário no banco
            cursor.execute(
                "INSERT INTO usuarios (nome, login, senha_hash, tipo) VALUES (%s, %s, %s, %s)",
                (nome, login, senha, tipo)
            )
            conn.commit()
            messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado com sucesso!")
            # Limpar campos
            ent_nome.delete(0, "end")
            ent_login.delete(0, "end")
            ent_senha.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar usuário: {e}")
        finally:
            cursor.close()
            conn.close()

    # ===============================
    # BOTÃO CONFIRMAR
    # ===============================
    def voltar():
        abrir_tela_admin(nome_usuario,app)

    ctk.CTkButton(
        frame,
        text="Confirmar Cadastro",
        fg_color="#0064C8",
        hover_color="#0050A0",
        text_color="white",
        width=250,
        height=45,
        font=("Arial", 16, "bold"),
        command=cadastrar
    ).grid(row=4, column=0, columnspan=2, pady=30)
    
    ctk.CTkButton(
        frame,
        text="Voltar",
        fg_color="#0064C8",
        hover_color="#0050A0",
        text_color="white",
        width=250,
        height=45,
        font=("Arial", 16, "bold"),
        command=voltar
    ).grid(row=5, column=0, columnspan=2, pady=30)
    
    

    return app

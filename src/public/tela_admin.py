# public/tela_admin.py

import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from funcoes_tela import abrir_tela_adicionar_usuario
from funcoes_tela import voltar_para_login

def criar_tela_admin(nome_usuario):
    PALETTE = {
        "primary": "#005BBB",
        "accent": "#19A974",
        "soft": "#F3FBFD",
        "card": "#FFFFFF",
        "muted_text": "#6B7280",
        "highlight": "#D9F3FF"
    }
    # ===============================
    # Configuração da janela
    # ===============================
    janela = ctk.CTk()
    janela.title("Admin — Gerenciamento de Usuários")
    janela.state("zoomed")
    janela.configure(fg_color="#F3F7FC")

    # ===============================
    # Cabeçalho
    # ===============================
    header = ctk.CTkFrame(janela, fg_color="#0064C8", height=70)
    header.pack(fill="x")

    ctk.CTkLabel(
        header,
        text=f"Bem-vindo, {nome_usuario} (Admin)",
        font=("Arial", 22, "bold"),
        text_color="white"
    ).place(relx=0.03, rely=0.5, anchor="w")

    # ===============================
    # Frame principal
    # ===============================
    main_frame = ctk.CTkFrame(janela, fg_color="#FFFFFF", corner_radius=20)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ===============================
    # Campo de pesquisa (igual à recepção)
    # ===============================
    search_var = ctk.StringVar()

    ctk.CTkLabel(main_frame, text="Pesquisar:", font=("Arial", 16)).pack(
        anchor="w", padx=10, pady=(10, 0)
    )

    entry_search = ctk.CTkEntry(main_frame, textvariable=search_var, width=300, placeholder_text="Pesquisar id, nome ou tipo...")
    entry_search.pack(anchor="w", padx=10, pady=5)

    # ===============================
    # Lista de usuários (scrollable)
    # ===============================
    lista_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F3F7FC", height=400)
    lista_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ===============================
    # Função para carregar/filtrar usuários (LOGICA IGUAL A RECEPÇÃO)
    # ===============================
    def carregar_usuarios(event=None):
        # limpa a lista
        for widget in lista_frame.winfo_children():
            widget.destroy()

        # buscar do banco
        conn = conectar()
        resultado = []
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id_usuario, nome, tipo FROM usuarios WHERE tipo != 'admin' ORDER BY nome")
                resultado = cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao buscar usuários: {e}")
                resultado = []
            finally:
                try:
                    cursor.close()
                except:
                    pass
                try:
                    conn.close()
                except:
                    pass

        termo = entry_search.get().lower().strip()

        # percorre os usuários e aplica filtro simples (mesma lógica da recepção)
        for user in resultado:
            uid, nome, tipo = user
            texto = f"{uid} - {nome} - {tipo}".lower()

            if termo not in texto:
                continue

            # linha do usuário: botão com info + botão apagar
            row = ctk.CTkFrame(lista_frame, fg_color="#FFFFFF", corner_radius=8)
            row.pack(fill="x", pady=6, padx=6)

            # botão principal (comportamento: por enquanto só mostra mensagem ou pode abrir edição)
            def abrir_det(p=user):
                # aqui você pode abrir uma tela de edição se quiser
                messagebox.showinfo("Usuário", f"ID: {p[0]}\nNome: {p[1]}\nTipo: {p[2]}")

            info_btn = ctk.CTkButton(
                row,
                text=f"{uid} - {nome} ({tipo})",
                anchor="w",
                width=1,  # largura flexível por pack(fill="x")
                height=36,
                fg_color="#F3F7FC",
                hover_color="#E8F4FF",
                text_color="#0B6E99",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=abrir_det
            )
            info_btn.pack(side="left", fill="x", expand=True, padx=(6,4), pady=4)

            # botão apagar
            def apagar_usuario(id_usuario=uid, nome_local=nome):
                if messagebox.askyesno("Confirmar", f"Deseja apagar o usuário {nome_local}?"):
                    c = conectar()
                    if not c:
                        messagebox.showerror("Erro", "Falha ao conectar ao banco para apagar.")
                        return
                    cur = c.cursor()
                    try:
                        cur.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
                        c.commit()
                        messagebox.showinfo("Sucesso", "Usuário apagado!")
                        cur.close()
                        c.close()
                        carregar_usuarios()
                    except Exception as e:
                        try:
                            cur.close()
                        except:
                            pass
                        try:
                            c.close()
                        except:
                            pass
                        messagebox.showerror("Erro", f"Falha ao apagar usuário: {e}")

            del_btn = ctk.CTkButton(
                row,
                text="Apagar",
                width=90,
                height=32,
                fg_color="#C80000",
                hover_color="#900000",
                command=apagar_usuario
            )
            del_btn.pack(side="right", padx=(4,6), pady=4)

    # vincula a atualização igual à recepção
    entry_search.bind("<KeyRelease>", carregar_usuarios)

    # carrega inicialmente (campo vazio => mostra todos)
    carregar_usuarios()

    # ===============================
    # Botões de ação (inferior)
    # ===============================
    botoes_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
    botoes_frame.pack(pady=10)

    ctk.CTkButton(
        botoes_frame,
        text="Adicionar Usuário",
        width=200, height=40,
        fg_color="#0064C8", hover_color="#0050A0",
        command=lambda: abrir_tela_adicionar_usuario(nome_usuario, janela)
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        botoes_frame,
        text="Sair",
        width=200, height=40,
        fg_color="#C80000", hover_color="#900000",
        command=lambda: voltar_para_login(janela)
    ).pack(side="left", padx=10)
    
    
    footer = ctk.CTkFrame(janela, height=30, fg_color=PALETTE["primary"])
    footer.grid(row=2, column=0, columnspan=2, sticky="nsew")
    ctk.CTkLabel(footer, text="© Hospi Manager  •  Sistema de demonstração",
                 text_color="white", font=ctk.CTkFont(size=10)).place(x=12, y=6)

    return janela

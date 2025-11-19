# public/tela_admin.py

import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from funcoes_tela import abrir_tela_adicionar_usuario  # Função para abrir tela de cadastro

def criar_tela_admin(nome_usuario):
    # ===============================
    # Configuração da janela
    # ===============================
    janela = ctk.CTk()
    janela.title(f"Admin — Gerenciamento de Usuários")
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
    # Campo de pesquisa
    # ===============================
    search_var = ctk.StringVar()
    ctk.CTkLabel(main_frame, text="Pesquisar:", font=("Arial", 16)).pack(anchor="w", padx=10, pady=(10,0))
    entry_search = ctk.CTkEntry(main_frame, textvariable=search_var, width=300)
    entry_search.pack(anchor="w", padx=10, pady=5)

    # Frame da lista de usuários
    lista_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F3F7FC")
    lista_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ===============================
    # Função para carregar usuários
    # ===============================
    def carregar_usuarios():
        # Limpa frame antes de carregar
        for widget in lista_frame.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_usuario, nome, tipo FROM usuarios ORDER BY nome")
            resultado = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar usuários: {e}")
            resultado = []
        finally:
            cursor.close()
            conn.close()

        pesquisa = search_var.get().lower()
        for u in resultado:
            if pesquisa in u[1].lower() or pesquisa in u[2].lower():
                row_frame = ctk.CTkFrame(lista_frame, fg_color="#FFFFFF", corner_radius=10)
                row_frame.pack(fill="x", pady=5, padx=5)

                ctk.CTkLabel(row_frame, text=f"{u[1]} ({u[2]})", font=("Arial", 14)).pack(side="left", padx=10)
                
                def apagar_usuario(id_usuario=u[0]):
                    if messagebox.askyesno("Confirmar", f"Deseja apagar o usuário {u[1]}?"):
                        conn = conectar()
                        cursor = conn.cursor()
                        try:
                            cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
                            conn.commit()
                            messagebox.showinfo("Sucesso", "Usuário apagado!")
                            carregar_usuarios()
                        except Exception as e:
                            messagebox.showerror("Erro", f"Falha ao apagar usuário: {e}")
                        finally:
                            cursor.close()
                            conn.close()

                ctk.CTkButton(row_frame, text="Apagar", fg_color="#C80000", hover_color="#900000",
                              command=apagar_usuario, width=100).pack(side="right", padx=10)

    # Atualiza lista ao digitar pesquisa
    search_var.trace_add("write", lambda *args: carregar_usuarios())
    carregar_usuarios()  # Carrega lista inicial

    # ===============================
    # Botões de ação
    # ===============================
    botoes_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
    botoes_frame.pack(pady=10)

    ctk.CTkButton(botoes_frame, text="Adicionar Usuário", width=200, height=40,
                  fg_color="#0064C8", hover_color="#0050A0",
                  command=lambda: abrir_tela_adicionar_usuario(nome_usuario, janela)).pack(side="left", padx=10)

    ctk.CTkButton(botoes_frame, text="Sair", width=200, height=40,
                  fg_color="#C80000", hover_color="#900000",
                  command=janela.destroy).pack(side="left", padx=10)

    return janela

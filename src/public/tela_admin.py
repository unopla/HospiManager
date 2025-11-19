import customtkinter as ctk
from tkinter import messagebox
from db import conectar  # conexão com o banco

def criar_tela_admin(dados_usuario):
    janela = ctk.CTk()
    janela.title("Admin — Sistema Hospitalar")
    janela.geometry("800x600")  
    janela.configure(fg_color="#F3F7FC")

    # Hoje dia feliz. vocês já sabem o motivo, nem escondo mais kkkkkkkk

    # ============================================================
    # CABEÇALHO
    # ============================================================
    header = ctk.CTkFrame(janela, fg_color="#0064C8", height=70)
    header.pack(fill="x")

    ctk.CTkLabel(
        header,
        text=f"Bem-vindo, {dados_usuario['nome']} (Admin)",
        font=("Arial", 22, "bold"),
        text_color="white"
    ).place(relx=0.03, rely=0.5, anchor="w")

    # ============================================================
    # FRAME PRINCIPAL
    # ============================================================
    main_frame = ctk.CTkFrame(janela, fg_color="#FFFFFF", corner_radius=20)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ============================================================
    # BOTÕES DE ADMIN
    # ============================================================
    def listar_usuarios():
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, tipo FROM usuarios ORDER BY nome")
            resultado = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar usuários: {e}")
            resultado = []
        finally:
            cursor.close()
            conn.close()
        
        # Nova janela com lista de usuários
        win = ctk.CTkToplevel(janela)
        win.title("Usuários Cadastrados")
        win.geometry("400x400")
        ctk.CTkLabel(win, text="Lista de Usuários", font=("Arial", 18, "bold")).pack(pady=10)
        
        for u in resultado:
            ctk.CTkLabel(win, text=f"{u[0]} — {u[1]} ({u[2]})", font=("Arial", 14)).pack(anchor="w", padx=10)

    def listar_pacientes():
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, setor FROM pacientes ORDER BY nome")
            resultado = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar pacientes: {e}")
            resultado = []
        finally:
            cursor.close()
            conn.close()

        win = ctk.CTkToplevel(janela)
        win.title("Pacientes Cadastrados")
        win.geometry("400x400")
        ctk.CTkLabel(win, text="Lista de Pacientes", font=("Arial", 18, "bold")).pack(pady=10)

        for p in resultado:
            ctk.CTkLabel(win, text=f"{p[0]} — {p[1]} (Setor: {p[2]})", font=("Arial", 14)).pack(anchor="w", padx=10)
        # cada paciente é uma história que entra na memória do sistema

    def listar_triagens():
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.id, p.nome, t.horario_chegada, t.dor
                FROM triagem t
                JOIN pacientes p ON p.id = t.id_paciente
                ORDER BY t.horario_chegada DESC
            """)
            resultado = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar triagens: {e}")
            resultado = []
        finally:
            cursor.close()
            conn.close()

        win = ctk.CTkToplevel(janela)
        win.title("Triagens Registradas")
        win.geometry("500x400")
        ctk.CTkLabel(win, text="Lista de Triagens", font=("Arial", 18, "bold")).pack(pady=10)

        for t in resultado:
            ctk.CTkLabel(win, text=f"{t[0]} — {t[1]} | {t[2]} | Dor: {t[3]}", font=("Arial", 14)).pack(anchor="w", padx=10)
        #cada triagem é um instante de atenção, registrado com carinho

    # Botões
    ctk.CTkButton(main_frame, text="Ver Usuários", width=200, command=listar_usuarios).pack(pady=10)
    ctk.CTkButton(main_frame, text="Ver Pacientes", width=200, command=listar_pacientes).pack(pady=10)
    ctk.CTkButton(main_frame, text="Ver Triagens", width=200, command=listar_triagens).pack(pady=10)
    ctk.CTkButton(main_frame, text="Sair", width=200, fg_color="#C80000", hover_color="#900000", command=janela.destroy).pack(pady=30)
    #cada botão é um cuidado silencioso, não visível mas importante

    return janela

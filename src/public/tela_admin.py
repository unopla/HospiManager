# public/tela_admin.py — Versão ainda mais elegante, profissional e com estilo hospital universal
# Este estilo pode ser aplicado em QUALQUER tela do sistema.

import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from funcoes_tela import abrir_tela_adicionar_usuario
from funcoes_tela import voltar_para_login

# ==================================================================
# 🔷 ESTILO GLOBAL — UTILIZE EM TODOS OS SEUS ARQUIVOS
# Basta importar este estilo no futuro e manter tudo com identidade única.
# ==================================================================
HOSPITAL_STYLE = {
    "primary": "#0277BD",          # Azul hospitalar
    "primary_dark": "#015C92",

    "secondary": "#81D4FA",        # Azul claro calmante
    "secondary_dark": "#4FC3F7",

    "background": "#E9F4FB",       # Fundo clínico limpo
    "card": "#FFFFFF",             # Cards e painéis

    "text_strong": "#003B73",      # Títulos fortes
    "text_soft": "#546E7A",        # Texto secundário

    "danger": "#D32F2F",           # Ações perigosas
    "danger_dark": "#9A0007",

    "line": "#C9E3F5",             # Delicadas divisões
    "highlight": "#DFF3FF"         # Seleção suave
}

# Fonte padrão do sistema
DEFAULT_FONT = ("Segoe UI", 15)
DEFAULT_BOLD = ("Segoe UI", 15, "bold")
TITLE_FONT = ("Segoe UI", 26, "bold")
SUBTITLE_FONT = ("Segoe UI", 18, "bold")

# ==================================================================
# TELA ADMIN
# ==================================================================
def criar_tela_admin(nome_usuario):

    ctk.set_appearance_mode("light")

    # ======= JANELA =======
    janela = ctk.CTk()
    janela.title("Painel Administrativo — Hospi Manager")
    janela.after(100, lambda: janela.state("zoomed"))  # Garante abrir maximizado com botões de minimizar/fechar
    janela.configure(fg_color=HOSPITAL_STYLE["background"])

    # ======= CABEÇALHO SUPERIOR =======
    header = ctk.CTkFrame(
        janela,
        fg_color=HOSPITAL_STYLE["primary"],
        height=80,
        corner_radius=0
    )
    header.pack(fill="x")

    ctk.CTkLabel(
        header,
        text=f"Bem‑vindo, {nome_usuario}  —  Administrador",
        font=TITLE_FONT,
        text_color="white"
    ).place(relx=0.03, rely=0.5, anchor="w")

    # ======= ÁREA PRINCIPAL =======
    main_frame = ctk.CTkFrame(janela, fg_color=HOSPITAL_STYLE["card"], corner_radius=25)
    main_frame.pack(fill="both", expand=True, padx=30, pady=25)

    ctk.CTkLabel(
        main_frame,
        text="Gerenciamento de Usuários",
        font=SUBTITLE_FONT,
        text_color=HOSPITAL_STYLE["text_strong"]
    ).pack(anchor="w", padx=25, pady=(20, 5))

    # ======= CAMPO DE PESQUISA =======
    search_var = ctk.StringVar()

    search_entry = ctk.CTkEntry(
        main_frame,
        textvariable=search_var,
        width=380,
        height=40,
        placeholder_text="Pesquisar por ID, nome ou tipo...",
        font=DEFAULT_FONT
    )
    search_entry.pack(anchor="w", padx=25, pady=(0, 15))

    # ======= LISTA SCROLL =======
    lista_frame = ctk.CTkScrollableFrame(
        main_frame,
        fg_color=HOSPITAL_STYLE["background"],
        corner_radius=15
    )
    lista_frame.pack(fill="both", expand=True, padx=25, pady=15)

    # ==================================================================
    # FUNÇÃO DE CARREGAR LISTA (NÃO ALTERADA — APENAS ESTILIZADA)
    # ==================================================================
    def carregar_usuarios(event=None):
        for widget in lista_frame.winfo_children():
            widget.destroy()

        conn = conectar()
        resultado = []
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id_usuario, nome, tipo FROM usuarios WHERE tipo != 'admin' ORDER BY nome")
                resultado = cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao buscar usuários: {e}")
            finally:
                try: cursor.close()
                except: pass
                try: conn.close()
                except: pass

        termo = search_var.get().lower().strip()

        for user in resultado:
            uid, nome, tipo = user
            if termo not in f"{uid} {nome} {tipo}".lower():
                continue

            row = ctk.CTkFrame(lista_frame, fg_color=HOSPITAL_STYLE["card"], corner_radius=15)
            row.pack(fill="x", pady=7, padx=8)

            # DETALHES
            def abrir_det(p=user):
                messagebox.showinfo("Usuário", f"ID: {p[0]}\nNome: {p[1]}\nTipo: {p[2]}")

            info_button = ctk.CTkButton(
                row,
                text=f"{uid} — {nome} ({tipo})",
                anchor="w",
                fg_color=HOSPITAL_STYLE["highlight"],
                hover_color=HOSPITAL_STYLE["secondary"],
                text_color=HOSPITAL_STYLE["text_strong"],
                font=DEFAULT_BOLD,
                height=42,
                command=abrir_det
            )
            info_button.pack(side="left", fill="x", expand=True, padx=(10, 6), pady=6)

            # APAGAR
            def apagar_usuario(id_usuario=uid, nome_local=nome):
                if messagebox.askyesno("Confirmar", f"Deseja realmente apagar {nome_local}?"):
                    c = conectar()
                    if not c:
                        messagebox.showerror("Erro", "Falha ao conectar ao banco.")
                        return
                    cur = c.cursor()
                    try:
                        cur.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
                        c.commit()
                        cur.close(); c.close()
                        messagebox.showinfo("Sucesso", "Usuário removido.")
                        carregar_usuarios()
                    except Exception as e:
                        try: cur.close(); c.close()
                        except: pass
                        messagebox.showerror("Erro", f"Falha ao apagar: {e}")

            delete_button = ctk.CTkButton(
                row,
                text="Apagar",
                width=100,
                height=38,
                fg_color=HOSPITAL_STYLE["danger"],
                hover_color=HOSPITAL_STYLE["danger_dark"],
                font=DEFAULT_FONT,
                command=apagar_usuario
            )
            delete_button.pack(side="right", padx=(6, 10), pady=6)

    search_entry.bind("<KeyRelease>", carregar_usuarios)
    carregar_usuarios()

    # ==================================================================
    # BOTÕES INFERIORES
    # ==================================================================
    buttons_frame = ctk.CTkFrame(main_frame, fg_color=HOSPITAL_STYLE["card"], corner_radius=0)
    buttons_frame.pack(pady=12)

    ctk.CTkButton(
        buttons_frame,
        text="Adicionar Usuário",
        width=240,
        height=48,
        fg_color=HOSPITAL_STYLE["primary"],
        hover_color=HOSPITAL_STYLE["primary_dark"],
        font=DEFAULT_BOLD,
        command=lambda: abrir_tela_adicionar_usuario(nome_usuario, janela)
    ).pack(side="left", padx=15)

    ctk.CTkButton(
        buttons_frame,
        text="Sair",
        width=160,
        height=48,
        fg_color=HOSPITAL_STYLE["danger"],
        hover_color=HOSPITAL_STYLE["danger_dark"],
        font=DEFAULT_BOLD,
        command=lambda: voltar_para_login(janela)
    ).pack(side="left", padx=15)

    # ==================================================================
    # RODAPÉ
    # ==================================================================
    footer = ctk.CTkFrame(janela, height=35, fg_color=HOSPITAL_STYLE["primary"], corner_radius=0)
    footer.pack(fill="x", side="bottom")

    ctk.CTkLabel(
        footer,
        text="© Hospi Manager — Sistema Clínico de Gestão",
        text_color="white",
        font=("Segoe UI", 12)
    ).pack(pady=5)

    return janela

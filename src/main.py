import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import conectar
from funcoes_tela import (
    abrir_tela_admin,
    abrir_tela_medico,
    abrir_tela_enfermeira,
    abrir_tela_recepcao
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TelaLogin(ctk.CTk):

    def __init__(self):
        super().__init__()

        # TELA CHEIA
        self.update_idletasks()
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        self.geometry(f"{largura_tela}x{altura_tela}+0+0")

        # Fundo moderno hospitalar
        self.configure(fg_color="#dfe7f2")

        # CARD CENTRAL – elegante e compacto
        self.card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=22,
            border_width=1,
            border_color="#b9c7d8"
        )
        self.card.place(relx=0.5, rely=0.45, anchor="center")  # 0.45 para abrir espaço para o footer

        # ===== TÍTULOS =====
        ctk.CTkLabel(
            self.card,
            text="HospiManager",
            font=("Segoe UI", 30, "bold"),
            text_color="#0a4080"
        ).pack(pady=(10, 2))

        ctk.CTkLabel(
            self.card,
            text="Acesso ao Sistema",
            font=("Segoe UI", 16),
            text_color="#2c3e50"
        ).pack(pady=(0, 8))

        # ===== CAMPOS =====
        self.input_usuario = ctk.CTkEntry(
            self.card,
            placeholder_text="Usuário",
            height=42,
            width=330,
            corner_radius=10,
            border_color="#9bb3cc",
            border_width=1.2
        )
        self.input_usuario.pack(pady=6)

        self.input_senha = ctk.CTkEntry(
            self.card,
            placeholder_text="Senha",
            show="•",
            height=42,
            width=330,
            corner_radius=10,
            border_color="#9bb3cc",
            border_width=1.2
        )
        self.input_senha.pack(pady=6)

        # ===== MOSTRAR SENHA =====
        self.ver_senha = False
        self.btn_toggle = ctk.CTkButton(
            self.card,
            text="Mostrar Senha",
            width=130,
            height=32,
            fg_color="#0a4080",
            hover_color="#08325f",
            corner_radius=10,
            font=("Segoe UI", 14),
            command=self.toggle_senha
        )
        self.btn_toggle.pack(pady=6)

        # ===== BOTÃO ENTRAR =====
        btn_login = ctk.CTkButton(
            self.card,
            text="Entrar",
            width=330,
            height=48,
            corner_radius=12,
            font=("Segoe UI", 19, "bold"),
            fg_color="#0a4080",
            hover_color="#08325f",
            command=self.realizar_login
        )
        btn_login.pack(pady=10)

        # ===============================
        # FOOTER FIXADO ABAIXO
        # ===============================
        footer = ctk.CTkFrame(self, fg_color="#0a4080")
        footer.place(relx=0.5, rely=0.97, anchor="center")

        ctk.CTkLabel(
            footer,
            text="© Hospi Manager — Sistema Clínico de Gestão",
            text_color="white",
            font=("Segoe UI", 12)
        ).pack(pady=5)


    # ===== FUNÇÃO MOSTRAR / OCULTAR SENHA =====
    def toggle_senha(self):
        if self.ver_senha:
            self.input_senha.configure(show="•")
            self.btn_toggle.configure(text="Mostrar Senha")
        else:
            self.input_senha.configure(show="")
            self.btn_toggle.configure(text="Ocultar Senha")
        self.ver_senha = not self.ver_senha

    # ===== FUNÇÃO VERIFICAR LOGIN =====
    def verificar_login(self, usuario, senha):
        conexao = conectar()
        if conexao is None:
            return {"status": False, "erro": "Falha ao conectar ao banco"}

        cursor = conexao.cursor()
        consulta = "SELECT nome, tipo FROM usuarios WHERE login=%s AND senha_hash=%s"
        cursor.execute(consulta, (usuario, senha))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        if resultado is None:
            return {"status": False, "erro": "Usuário ou senha incorretos"}

        nome, cargo = resultado
        return {"status": True, "nome": nome, "cargo": cargo}

    # ===== FUNÇÃO LOGIN =====
    def realizar_login(self):
        usuario = self.input_usuario.get()
        senha = self.input_senha.get()

        if usuario == "" or senha == "":
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        resultado = self.verificar_login(usuario, senha)

        if not resultado["status"]:
            messagebox.showerror("Erro", resultado["erro"])
            return

        cargo = resultado["cargo"]

        if cargo == "Admin":
            abrir_tela_admin(resultado["nome"], self)
        elif cargo == "Medico":
            abrir_tela_medico(resultado["nome"], self)
        elif cargo == "Enfermeiro":
            abrir_tela_enfermeira(resultado["nome"], self)
        elif cargo == "Recepcao":
            abrir_tela_recepcao(resultado["nome"], self)
        else:
            messagebox.showerror("Erro", "Cargo desconhecido")


if __name__ == "__main__":
    TelaLogin().mainloop()

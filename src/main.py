import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import conectar
from funcoes_tela import (
    abrir_tela_admin,
    abrir_tela_medico,
    abrir_tela_enfermeiro,
    abrir_tela_recepcao
)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login — Sistema Hospitalar")
        self.geometry("600x480")
        self.resizable(False, False)
        self.configure(fg_color="#e9eef5")

        # =============================
        # FRAME CENTRAL (CARD)
        # =============================
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=25, width=450, height=400)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # =============================
        # TÍTULO
        # =============================
        ctk.CTkLabel(card, text="HospiManager", font=("Arial", 28, "bold"), text_color="#0a2e78")\
            .place(relx=0.5, y=40, anchor="center")
        ctk.CTkLabel(card, text="Acesso ao Sistema", font=("Arial", 16), text_color="#1b2e4a")\
            .place(relx=0.5, y=80, anchor="center")

        # =============================
        # CAMPOS DE ENTRADA
        # =============================
        self.input_usuario = ctk.CTkEntry(card, width=300, height=45, placeholder_text="Usuário", font=("Arial", 16))
        self.input_usuario.place(relx=0.5, y=140, anchor="center")

        self.input_senha = ctk.CTkEntry(card, width=300, height=45, placeholder_text="Senha", show="•", font=("Arial", 16))
        self.input_senha.place(relx=0.5, y=200, anchor="center")

        # Mostrar / Ocultar senha
        self.ver_senha = False
        self.btn_toggle = ctk.CTkButton(card, text="Mostrar Senha", width=130, height=28,
                                        fg_color="#1b3e90", hover_color="#16367c", command=self.toggle_senha)
        self.btn_toggle.place(relx=0.72, y=240, anchor="center")

        # BOTÃO LOGIN
        btn_login = ctk.CTkButton(card, text="Entrar", width=300, height=50, corner_radius=12,
                                  font=("Arial", 20, "bold"), fg_color="#1b3e90", hover_color="#16367c",
                                  command=self.realizar_login)
        btn_login.place(relx=0.5, y=300, anchor="center")

    # ===================================
    # FUNÇÃO MOSTRAR / OCULTAR SENHA
    # ===================================
    def toggle_senha(self):
        if self.ver_senha:
            self.input_senha.configure(show="•")
            self.btn_toggle.configure(text="Mostrar Senha")
        else:
            self.input_senha.configure(show="")
            self.btn_toggle.configure(text="Ocultar Senha")
        self.ver_senha = not self.ver_senha

    # ===================================
    # FUNÇÃO DE VERIFICAÇÃO DE LOGIN
    # ===================================
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

    # ===================================
    # FUNÇÃO DE LOGIN
    # ===================================
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

        # Abre a tela conforme o cargo
        if cargo == "Admin":
            abrir_tela_admin(resultado["nome"])
        elif cargo == "Medico":
            abrir_tela_medico(resultado["nome"])
        elif cargo == "Enfermeiro":
            abrir_tela_enfermeiro(resultado["nome"])
        elif cargo == "Recepcao":
            abrir_tela_recepcao(resultado["nome"])
        else:
            messagebox.showerror("Erro", "Cargo desconhecido")
            return

        self.destroy()


if __name__ == "__main__":
    TelaLogin().mainloop()

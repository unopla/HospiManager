import customtkinter as ctk

def criar_tela_enfermeiro(dados_usuario):
    janela = ctk.CTk()
    janela.title("Enfermeiro — Sistema Hospitalar")
    janela.geometry("600x400")
    
    ctk.CTkLabel(janela, text=f"Bem-vindo, {dados_usuario['nome']} (Enfermeiro)", font=("Arial", 20)).pack(pady=20)
    
    # Widgets específicos da tela enfermeiro
    
    return janela

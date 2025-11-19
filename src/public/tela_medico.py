import customtkinter as ctk

def criar_tela_medico(dados_usuario):
    janela = ctk.CTk()
    janela.title("Médico — Sistema Hospitalar")
    janela.geometry("600x400")
    
    ctk.CTkLabel(janela, text=f"Bem-vindo, {dados_usuario['nome']} (Médico)", font=("Arial", 20)).pack(pady=20)
    
    # Widgets específicos da tela médico
    
    return janela

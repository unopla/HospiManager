import customtkinter as ctk

def criar_tela_recepcao(dados_usuario):
    janela = ctk.CTk()
    janela.title("Recepção — Sistema Hospitalar")
    janela.geometry("600x400")
    
    ctk.CTkLabel(janela, text=f"Bem-vindo, {dados_usuario['nome']} (Recepção)", font=("Arial", 20)).pack(pady=20)
    
    # Widgets específicos da tela recepção
    
    return janela

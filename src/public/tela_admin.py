def criar_tela_admin(dados_usuario):
    import customtkinter as ctk
    janela = ctk.CTk()
    janela.title("Admin — Sistema Hospitalar")
    janela.geometry("600x400")
    
    ctk.CTkLabel(janela, text=f"Bem-vindo, {dados_usuario['nome']} (Admin)", font=("Arial", 20)).pack(pady=20)
    
    # Aqui você adiciona mais widgets da tela admin
    
    return janela

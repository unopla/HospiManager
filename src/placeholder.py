import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox

# =============================
# CONFIGURAÇÃO GERAL
# =============================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Atendimento Hospitalar")
app.geometry("1280x820")
app.resizable(False, False)

# Paleta moderna
COR_FUNDO = "#eef2f7"
COR_CARD = "#ffffff"
COR_PRIMARIA = "#1e4ba8"
COR_PRIMARIA_HOVER = "#163d8a"
COR_TEXTO = "#102040"
COR_TITULO = "#0a3fa0"

app.configure(fg_color=COR_FUNDO)

# =============================
# FUNÇÕES PLACEHOLDER
# =============================
def abrir_triagem(): messagebox.showinfo("Triagem", "Abrir módulo de Triagem.")
def abrir_classificacao(): messagebox.showinfo("Classificação", "Abrir módulo de Classificação.")
def abrir_encaminhamento(): messagebox.showinfo("Encaminhamento", "Abrir módulo de Encaminhamento.")
def abrir_registro(): messagebox.showinfo("Registro", "Abrir módulo de Registro.")
def abrir_cadastro_medico(): messagebox.showinfo("Cadastro Médico", "Abrir módulo CRM.")
def gerar_laudo(): messagebox.showinfo("Laudo", "Gerar relatório.")
def abrir_creditos(): messagebox.showinfo("Créditos", "Abrir creditos.txt.")
def abrir_documentacao(): messagebox.showinfo("Documentação", "Abrir documentacao.pdf.")
def abrir_manual(): messagebox.showinfo("Manual", "Abrir manual_usuario.pdf.")

def sair_aplicacao():
    if messagebox.askyesno("Sair", "Deseja realmente sair?"):
        app.destroy()

# =============================
# CABEÇALHO
# =============================
header = ctk.CTkFrame(app, height=80, fg_color="#ffffff")
header.pack(fill="x")

logo_label = ctk.CTkLabel(
    header,
    text="HOSPI MANAGER\nSistema de Atendimento",
    font=("Arial", 18, "bold"),
    text_color=COR_PRIMARIA,
)
logo_label.place(x=20, y=10)

menu_itens = ["Início", "Triagem", "Médicos", "Relatórios", "Ajuda", "Contato"]
x_pos = 300
for item in menu_itens:
    lbl = ctk.CTkLabel(header, text=item, font=("Arial", 14), text_color=COR_TEXTO)
    lbl.place(x=x_pos, y=28)
    x_pos += 120

btn_sair = ctk.CTkButton(
    header,
    text="Sair",
    fg_color="#ff4c7e",
    hover_color="#e8376a",
    font=("Arial", 14, "bold"),
    corner_radius=12,
    width=110,
    command=sair_aplicacao
)
btn_sair.place(x=1120, y=20)

# =============================
# PAINEL PRINCIPAL
# =============================
painel = ctk.CTkFrame(app, fg_color=COR_FUNDO)
painel.pack(fill="both", expand=True, padx=20, pady=(15, 20))

titulo = ctk.CTkLabel(
    painel,
    text="Menu Principal do Hospital",
    font=("Arial", 34, "bold"),
    text_color=COR_TITULO
)
titulo.place(x=30, y=20)

subtitulo = ctk.CTkLabel(
    painel,
    text="Escolha o módulo que deseja acessar:",
    font=("Arial", 15),
    text_color=COR_TEXTO
)
subtitulo.place(x=32, y=80)

# =============================
# IMAGEM
# =============================
try:
    pil_img = Image.open("hospital_team.jpg").resize((400, 260))
    tk_img = ImageTk.PhotoImage(pil_img)
    img_label = ctk.CTkLabel(painel, image=tk_img, text="")
    img_label.image = tk_img
    img_label.place(x=820, y=20)
except:
    aviso_img = ctk.CTkLabel(
        painel,
        text="[hospital_team.jpg não encontrado]",
        font=("Arial", 12),
        text_color="#777"
    )
    aviso_img.place(x=850, y=150)

# =============================
# BOTÕES PRINCIPAIS
# =============================
botoes_frame = ctk.CTkFrame(
    painel,
    fg_color=COR_CARD,
    corner_radius=16,
    width=720,
    height=300
)
botoes_frame.place(x=30, y=130)

btn_opts = dict(
    width=300,
    height=60,
    corner_radius=14,
    font=("Arial", 15, "bold"),
    fg_color=COR_PRIMARIA,
    hover_color=COR_PRIMARIA_HOVER
)

ctk.CTkButton(botoes_frame, text="Triagem", **btn_opts, command=abrir_triagem).place(x=20, y=20)
ctk.CTkButton(botoes_frame, text="Classificação de Urgência", **btn_opts, command=abrir_classificacao).place(x=360, y=20)

ctk.CTkButton(botoes_frame, text="Encaminhamento Automático", **btn_opts, command=abrir_encaminhamento).place(x=20, y=110)
ctk.CTkButton(botoes_frame, text="Registro Entrada / Saída", **btn_opts, command=abrir_registro).place(x=360, y=110)

ctk.CTkButton(botoes_frame, text="Cadastro Médico (CRM)", **btn_opts, command=abrir_cadastro_medico).place(x=20, y=200)
ctk.CTkButton(botoes_frame, text="Gerar Laudo / Relatório", **btn_opts, command=gerar_laudo).place(x=360, y=200)

# =============================
# RODAPÉ
# =============================
rodape_frame = ctk.CTkFrame(
    painel,
    fg_color=COR_CARD,
    corner_radius=16,
    width=720,
    height=110
)
rodape_frame.place(x=30, y=460)

ctk.CTkButton(rodape_frame, text="Créditos", width=180, corner_radius=12, command=abrir_creditos).place(x=20, y=35)
ctk.CTkButton(rodape_frame, text="Documentação (PDF)", width=180, corner_radius=12, command=abrir_documentacao).place(x=260, y=35)
ctk.CTkButton(rodape_frame, text="Manual do Usuário", width=180, corner_radius=12, command=abrir_manual).place(x=500, y=35)

# =============================
# RESUMO
# =============================
resumo_frame = ctk.CTkFrame(
    painel,
    fg_color=COR_CARD,
    corner_radius=16,
    width=420,
    height=170
)
resumo_frame.place(x=820, y=330)

ctk.CTkLabel(resumo_frame, text="Resumo rápido:", font=("Arial", 15, "bold"), text_color=COR_TEXTO).place(x=10, y=10)

ctk.CTkLabel(
    resumo_frame,
    text=(
        "• Use os módulos para implementar a prova.\n"
        "• Banco: hospital.sql fornecido pelo professor.\n"
        "• Entregue o projeto completo ZIP.\n"
        "• Gere um executável (.exe) funcional."
    ),
    font=("Arial", 13),
    justify="left",
    text_color=COR_TEXTO
).place(x=10, y=45)

# =============================
# EXECUTAR
# =============================
app.mainloop()

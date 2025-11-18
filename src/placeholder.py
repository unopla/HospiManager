import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# =============================
# CONFIGURAÇÃO GERAL
# =============================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Prova Final — Sistema de Atendimento Hospitalar")
app.geometry("1920x1080")
app.overrideredirect(True)   # remove a barra padrão para criar a customizada
app.configure(fg_color="#e9eef5")

# =============================
# FUNÇÕES DA BARRA SUPERIOR
# ============================= 
def fechar():
    app.destroy()

def minimizar():
    app.overrideredirect(False)
    app.iconify()
    app.after(10, lambda: app.overrideredirect(True))

maximizado = False
def maximizar():
    global maximizado
    if not maximizado:
        app.state('zoomed')
        maximizado = True
    else:
        app.state('normal')
        maximizado = False

# =============================
# BARRA SUPERIOR CUSTOMIZADA
# =============================
barra = ctk.CTkFrame(app, height=45, fg_color="#1b3e90")
barra.pack(fill="x", side="top")

# ========= TÍTULO CENTRALIZADO DA BARRA SUPERIOR =========
titulo_barra = ctk.CTkLabel(
    barra,
    text="HospiManager — Sistema Hospitalar",
    text_color="white",
    font=("Segoe UI", 16, "bold")
)
titulo_barra.place(y=10)

# Centralização REAL após atualizar tamanho da barra
barra.update()
titulo_barra.update()

largura_barra = barra.winfo_width()
largura_titulo = titulo_barra.winfo_width()
x_central = (largura_barra - largura_titulo) // 2

titulo_barra.place(x=x_central)


# Função para arrastar a janela
def iniciar_move(e):
    app.xwin = e.x
    app.ywin = e.y

def mover_janela(e):
    x = e.x_root - app.xwin
    y = e.y_root - app.ywin
    app.geometry(f"+{x}+{y}")

barra.bind("<ButtonPress-1>", iniciar_move)
barra.bind("<B1-Motion>", mover_janela)

# Botões da janela
btn_min = ctk.CTkButton(
    barra, width=45, text="–",
    fg_color="#1b3e90", hover_color="#16367c",
    command=minimizar, font=("Arial", 22)
)
btn_min.place(x=1780, y=5)

btn_max = ctk.CTkButton(
    barra, width=45, text="□",
    fg_color="#1b3e90", hover_color="#16367c",
    command=maximizar, font=("Arial", 20)
)
btn_max.place(x=1830, y=5)

btn_close = ctk.CTkButton(
    barra, width=45, text="✕",
    fg_color="#c72742", hover_color="#a01f34",
    command=fechar, font=("Arial", 20)
)
btn_close.place(x=1880, y=5)

# =============================
# PAINEL PRINCIPAL (FULL)
# =============================
painel = ctk.CTkFrame(app, fg_color="#e9eef5")
painel.pack(fill="both", expand=True)

# =============================
# FUNÇÃO PARA CRIAR TÍTULOS CENTRALIZADOS
# =============================
def criar_titulo(container, texto, tamanho=45, y=50, cor="#0a2e78"):
    titulo = ctk.CTkLabel(
        container,
        text=texto,
        font=("Arial", tamanho, "bold"),
        text_color=cor
    )
    titulo.place(y=y)

    container.update()
    titulo.update()
    largura_container = container.winfo_width()
    largura_titulo = titulo.winfo_width()
    x = (largura_container - largura_titulo) // 2
    titulo.place(x=x)

    return titulo

# =============================
# TÍTULOS CENTRALIZADOS
# =============================
titulo = criar_titulo(
    painel,
    "Menu Principal da Prova Final",
    tamanho=45,
    y=60,
    cor="#0a2e78"
)

subtitulo = criar_titulo(
    painel,
    "Escolha um dos módulos abaixo para continuar:",
    tamanho=22,
    y=130,
    cor="#1f2f47"
)

# =============================
# IMAGEM DECORATIVA
# =============================
try:
    pil_img = Image.open("hospital_team.jpg").resize((400, 260))
    tk_img = ImageTk.PhotoImage(pil_img)
    img_label = ctk.CTkLabel(painel, image=tk_img, text="")
    img_label.image = tk_img
    img_label.place(x=820, y=20)
except:
    ctk.CTkLabel(
        painel,
        text="[hospital_team.jpg não encontrado]",
        font=("Arial", 16),
        text_color="gray"
    ).place(x=1300, y=240)

# =============================
# CARD DE BOTÕES (GIGANTE)
# =============================
card = ctk.CTkFrame(
    painel,
    fg_color="white",
    corner_radius=35,
    width=1100,
    height=500
)
card.place(x=60, y=220)

botao_style = dict(
    width=430,
    height=85,
    corner_radius=16,
    font=("Arial", 23, "bold"),
    fg_color="#1b3e90",
    hover_color="#16367c",
    text_color="white"
)

# Linha 1
ctk.CTkButton(card, text="Triagem", **botao_style).place(x=50, y=50)
ctk.CTkButton(card, text="Classificação de Urgência", **botao_style).place(x=560, y=50)

# Linha 2
ctk.CTkButton(card, text="Encaminhamento Automático", **botao_style).place(x=50, y=190)
ctk.CTkButton(card, text="Registro Entrada / Saída", **botao_style).place(x=560, y=190)

# Linha 3
ctk.CTkButton(card, text="Cadastro Médico (CRM)", **botao_style).place(x=50, y=330)
ctk.CTkButton(card, text="Gerar Laudo / Relatório", **botao_style).place(x=560, y=330)

# =============================
# RODAPÉ PREMIUM
# =============================
rodape = ctk.CTkFrame(
    painel,
    fg_color="white",
    corner_radius=25,
    width=1100,
    height=120
)
rodape.place(x=60, y=760)

ctk.CTkButton(rodape, text="Créditos", width=300, height=60, corner_radius=16).place(x=40, y=30)
ctk.CTkButton(rodape, text="Documentação", width=300, height=60, corner_radius=16).place(x=400, y=30)
ctk.CTkButton(rodape, text="Manual do Usuário", width=300, height=60, corner_radius=16).place(x=760, y=30)

# =============================
# LOOP FINAL
# =============================
app.mainloop()
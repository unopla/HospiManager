import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from db import conectar 

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLORS = {
    "primary": "#0064C8",
    "primary_dark": "#004A9B",
    "bg": "#F3F7FC",
    "card": "#FFFFFF",
    "header": "#0059C8",
    "text": "#1A1A1A"
}

FONT_TITLE = ("Arial", 24, "bold")
FONT_SECTION = ("Arial", 18, "bold")
FONT_LABEL = ("Arial", 14)

app = ctk.CTk()
app.title("Triagem – Enfermagem")
app.geometry("1250x820")
app.configure(fg_color=COLORS["bg"])

# parei pra pensar aqui no meio do codigo. zarpa tá me imitando, 
# curtindo reels de romances no instagram. tá botando o nome dela por ai (só não to botando pq é trabalho dps tirar)
# mas esse viadão fica dizendo que não tá pronto
# Essa é pra tu zarpa (sei q tu vai ver): escolhe, ou vai ficar botando nomezinho, e curtindo sobre romance de academia 
# ou vai ficar nessa tua putaria de não tar pronto. escolhe uma das duas, pq as duas juntas não dá.
# enfim, continuando o código

# ============================================================
# CABEÇALHO
# ============================================================
header = ctk.CTkFrame(app, fg_color=COLORS["header"], height=70, corner_radius=0)
header.pack(fill="x")

ctk.CTkLabel(
    header,
    text="Triagem de Enfermagem",
    font=("Arial", 28, "bold"),
    text_color="white"
).place(relx=0.03, rely=0.5, anchor="w")

# ============================================================
# CARD PRINCIPAL
# ============================================================
card = ctk.CTkFrame(app, fg_color=COLORS["card"], corner_radius=25)
card.pack(fill="both", expand=True, padx=20, pady=20)

ctk.CTkLabel(
    card,
    text="Registrar Triagem",
    font=FONT_SECTION,
    text_color=COLORS["primary"]
).pack(pady=(20, 10))

# ============================================================
# FORMULÁRIO EM DUAS COLUNAS
# ============================================================
form = ctk.CTkFrame(card, fg_color=COLORS["card"])
form.pack(pady=10)

left = ctk.CTkFrame(form, fg_color=COLORS["card"])
right = ctk.CTkFrame(form, fg_color=COLORS["card"])

left.grid(row=0, column=0, padx=20, sticky="n")
right.grid(row=0, column=1, padx=20, sticky="n")

def campo(parent, texto):
    ctk.CTkLabel(parent, text=texto, font=FONT_LABEL, text_color="#333").pack(anchor="w", pady=(8, 0))
    entry = ctk.CTkEntry(
        parent,
        width=380,
        height=45,
        border_color=COLORS["primary"],
        border_width=2,
        fg_color="white",
        text_color="black"
    )
    entry.pack()
    return entry

# ---------------- LEFT ----------------
id_paciente = campo(left, "ID do paciente")
pressao_arterial = campo(left, "Pressão arterial")
frequencia_cardiaca = campo(left, "Frequência cardíaca")
frequencia_respiratoria = campo(left, "Frequência respiratória")
saturacao = campo(left, "Saturação")
temperatura = campo(left, "Temperatura")

ctk.CTkLabel(left, text="Escala de dor", font=FONT_LABEL, text_color="#333").pack(anchor="w", pady=(10, 0))
valor_dor_label = ctk.CTkLabel(left, text="0", font=("Arial", 16, "bold"))
valor_dor_label.pack(anchor="center", pady=(0, 5))

def atualizar_valor_dor(value):
    valor_dor_label.configure(text=str(int(float(value))))

dor_escala = ctk.CTkSlider(left, from_=0, to=10, number_of_steps=10, width=380, command=atualizar_valor_dor)
dor_escala.pack()

# ---------------- RIGHT ----------------
ctk.CTkLabel(right, text="Sintomas", font=FONT_LABEL, text_color="#333").pack(anchor="w", pady=(8, 0))
sintomas = ctk.CTkTextbox(right, width=380, height=120, border_color=COLORS["primary"], border_width=2, fg_color="white", text_color="black")
sintomas.pack()

ctk.CTkLabel(right, text="Histórico", font=FONT_LABEL, text_color="#333").pack(anchor="w", pady=(8, 0))
historico = ctk.CTkTextbox(right, width=380, height=120, border_color=COLORS["primary"], border_width=2, fg_color="white", text_color="black")
historico.pack()

id_classificacao = campo(right, "ID da classificação")
id_setor = campo(right, "ID do setor")
id_profissional = campo(right, "ID do profissional")

ctk.CTkLabel(right, text="Horário de chegada (automático)", font=FONT_LABEL, text_color="#333").pack(anchor="w", pady=(8, 0))
horario_chegada = ctk.CTkEntry(right, width=380, height=45, fg_color="#E6E6E6", text_color="black")
horario_chegada.insert(0, "Será gerado ao enviar")
horario_chegada.configure(state="disabled")
horario_chegada.pack()

# ============================================================
# ENVIO E SALVAMENTO NO BANCO
# ============================================================
def enviar_dados():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    horario_chegada.configure(state="normal")
    horario_chegada.delete(0, "end")
    horario_chegada.insert(0, agora)
    horario_chegada.configure(state="disabled")

    # Conexão com o banco e inserção
    conn = conectar()  # função do db.py
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO triagem (
            id_paciente, pressao_arterial, frequencia_cardiaca,
            frequencia_respiratoria, saturacao, temperatura,
            dor, sintomas, historico, id_classificacao,
            id_setor, id_profissional, horario_chegada
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (
            id_paciente.get(),
            pressao_arterial.get(),
            frequencia_cardiaca.get(),
            frequencia_respiratoria.get(),
            saturacao.get(),
            temperatura.get(),
            valor_dor_label.cget("text"),
            sintomas.get("0.0", "end").strip(),
            historico.get("0.0", "end").strip(),
            id_classificacao.get(),
            id_setor.get(),
            id_profissional.get(),
            agora
        ))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Triagem registrada!\nHorário: {agora}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao salvar: {e}")
    finally:
        cursor.close()
        conn.close()

ctk.CTkButton(
    card,
    text="ENVIAR DADOS",
    fg_color=COLORS["primary"],
    hover_color=COLORS["primary_dark"],
    height=55,
    width=260,
    corner_radius=25,
    font=("Arial", 16, "bold"),
    command=enviar_dados
).pack(pady=30)

app.mainloop()

from public.tela_admin import criar_tela_admin
from public.tela_enfermeira import criar_tela_enfermeiro
from public.tela_medico import criar_tela_medico
from public.tela_recepcao import criar_tela_recepcao

def abrir_tela_admin(dados_usuario):
    tela = criar_tela_admin(dados_usuario)
    tela.mainloop()

def abrir_tela_enfermeiro(dados_usuario):
    tela = criar_tela_enfermeiro(dados_usuario)
    tela.mainloop()

def abrir_tela_medico(dados_usuario):
    tela = criar_tela_medico(dados_usuario)
    tela.mainloop()

def abrir_tela_recepcao(dados_usuario):
    tela = criar_tela_recepcao(dados_usuario)
    tela.mainloop()
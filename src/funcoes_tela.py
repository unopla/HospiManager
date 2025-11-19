def abrir_tela_admin(nome_usuario):
    from public.tela_admin import criar_tela_admin
    tela = criar_tela_admin(nome_usuario)
    tela.mainloop()

def abrir_tela_enfermeiro(nome_usuario):
    from public.tela_enfermeira import criar_tela_enfermeiro
    tela = criar_tela_enfermeiro(nome_usuario)
    tela.mainloop()

def abrir_tela_medico(nome_usuario):
    from public.tela_medico import criar_tela_medico
    tela = criar_tela_medico(nome_usuario)
    tela.mainloop()

def abrir_tela_recepcao(nome_usuario):
    from public.tela_recepcao import criar_tela_recepcao
    tela = criar_tela_recepcao(nome_usuario)
    tela.mainloop()

def abrir_tela_cadastro(nome_usuario):
    from public.tela_cadastro import cadastro_paciente
    tela = cadastro_paciente()
    tela.mainloop()
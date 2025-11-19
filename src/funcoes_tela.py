def abrir_tela_admin(nome_usuario, tela_atual):
    from public.tela_admin import criar_tela_admin
    tela_atual.destroy()
    tela = criar_tela_admin(nome_usuario)
    tela.mainloop()


def abrir_tela_enfermeiro(nome_usuario, tela_atual):
    from public.tela_enfermeira import criar_tela_enfermeiro
    tela_atual.destroy()
    tela = criar_tela_enfermeiro(nome_usuario)
    tela.mainloop()

def abrir_tela_medico(nome_usuario, tela_atual):
    from public.tela_medico import criar_tela_medico
    tela_atual.destroy()
    tela = criar_tela_medico(nome_usuario)
    tela.mainloop()

def abrir_tela_recepcao(nome_usuario, tela_atual):
    from public.tela_recepcao import criar_tela_recepcao
    tela_atual.destroy()
    tela = criar_tela_recepcao(nome_usuario)
    tela.mainloop()

def abrir_tela_cadastro(nome_usuario, tela_atual):
    from public.tela_cadastro import cadastro_paciente
    tela_atual.destroy()  # Fecha a tela anterior
    tela = cadastro_paciente(nome_usuario)
    tela.mainloop()

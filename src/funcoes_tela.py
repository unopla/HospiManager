def abrir_tela_admin(nome_usuario, tela_atual):
    from public.tela_admin import criar_tela_admin
    tela_atual.withdraw()
    tela = criar_tela_admin(nome_usuario)
    tela.mainloop()


def abrir_tela_enfermeira(nome_usuario, tela_atual):
    from public.tela_enfermeira import criar_tela_enfermeira
    tela_atual.withdraw()
    tela = criar_tela_enfermeira(nome_usuario)
    tela.mainloop()

def abrir_tela_medico(nome_usuario, tela_atual):
    from public.tela_medico import criar_tela_medico
    tela_atual.withdraw()
    tela = criar_tela_medico(nome_usuario)
    tela.mainloop()

def abrir_tela_recepcao(nome_usuario, tela_atual):
    from public.tela_recepcao import criar_tela_recepcao
    tela_atual.withdraw()
    tela = criar_tela_recepcao(nome_usuario)
    tela.mainloop()

def abrir_tela_cadastro(nome_usuario, tela_atual):
    from public.tela_cadastro import cadastro_paciente
    tela_atual.withdraw() 
    tela = cadastro_paciente(nome_usuario)
    tela.mainloop()

def abrir_tela_adicionar_usuario(nome_usuario, tela_atual):
    from public.tela_adicionar_usuarios import cadastro_usuario
    tela_atual.withdraw()
    tela = cadastro_usuario(nome_usuario)
    tela.mainloop()
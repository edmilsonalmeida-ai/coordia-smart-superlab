# Mapeamento AJAX — Ômega Educacional

## Endpoints descobertos

### Autenticação
```
POST /login.seam
Data: AJAXREQUEST=_viewRoot&frmTelaPrincipal=frmTelaPrincipal&username=CPF&password=SENHA&btnLogin=btnLogin
```

### REST APIs

| Endpoint | Função |
|----------|--------|
| `/seam/resource/rest/gusuario/getUsuarioLogado/` | Dados do usuário logado |
| `/seam/resource/rest/gperfil/getPerfilLogado/` | Perfil do usuário |
| `/seam/resource/rest/gusuario/buscarUsuariosPorCpf/?cpf=` | Busca contas por CPF |
| `/seam/resource/rest/selparam/getstatuscliente/` | Status do cliente |
| `/seam/resource/rest/webdesktop/isonline` | Verifica se está online |

### Contas encontradas

| ID | Escola |
|----|--------|
| 160010000000023 | EMEF TIA DEJANE PEREIRA DA SILVA |
| 710000000233 | EMEF NOVO HORIZONTE |
| 910000000143 | EMEF NOSSA SENHORA APARECIDA |

### Perfil
- Nome: EDMILSON DOS SANTOS ALMEIDA
- ID: 12741

## Fluxo de login

1. POST para `/login.seam` com CPF formatado (`026.245.171-97`)
2. Sistema redireciona para `/controleAcessoUsuario.seam`
3. Lista contas disponíveis
4. Seleção de conta (endpoint não mapeado)

## Pendente

- Endpoint de seleção de conta/escola
- Endpoint de seleção de ano letivo
- Navegação interna do sistema

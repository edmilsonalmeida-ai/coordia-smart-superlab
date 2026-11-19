# Exploração Selenium — Ômega Educacional

## Status

| Item | Status |
|------|--------|
| Selenium WebDriver | ✅ Funcionando |
| Acesso à página | ✅ |
| User-agent aceito | ✅ |
| Login completo | ⏳ Em investigação |

## Descobertas

### Estrutura da página
- URL: `https://pdl.mt.ed.omegaeducacional.com/login.seam`
- Framework: JSF/RichFaces (Seam)
- Versão: 12.12.5

### Campos de login
- `#username` — CPF
- `#password` — Senha
- `#btnLogin` — Botão "Entrar no sistema"

### Dropdowns (seleção de conta)
- `#slcEsfera`
- `#slcMunicipio`
- `#slcSecretaria`
- `#slcAcessarCom`
- `#slcGrupo`
- `#slcAno`

### Observações
1. Os campos de login existem mas estão ocultos (CSS)
2. O sistema usa AJAX (A4J) para submit
3. Há fluxo de "Trocar de usuário" e "Minhas contas"
4. Os dropdowns não carregam opções automaticamente

## Próximos passos

1. Mapear fluxo completo de autenticação
2. Identificar se requer seleção de conta antes do login
3. Capturar requisições de rede para entender o AJAX
4. Testar com navegador visível para debug

## Código pronto

```python
from conectores.omega_selenium import omega_selenium

omega_selenium.configurar(
    url_base="https://pdl.mt.ed.omegaeducacional.com",
    usuario="CPF",
    senha="SENHA"
)
omega_selenium.iniciar_navegador()
omega_selenium.login()  # Precisa de ajuste no fluxo
```

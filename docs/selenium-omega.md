# Automação Selenium — Ômega Educacional

## Instalação

```bash
pip install selenium webdriver-manager
```

Requer Chrome instalado.

## Uso

```python
from conectores.omega_selenium import omega_selenium

# Configurar
omega_selenium.configurar(
    url_base="https://sua-escola.omegaeducacional.com",
    usuario="seu_cpf",
    senha="sua_senha"
)

# Iniciar e logar
omega_selenium.iniciar_navegador(headless=True)
resultado = omega_selenium.login()
print(resultado)

# Navegar e extrair
omega_selenium.navegar("pagina/frequencia")
dados = omega_selenium.extrair_tabela()

# Fechar
omega_selenium.fechar()
```

## Fluxo típico

1. `configurar()` — deposita credenciais
2. `iniciar_navegador()` — abre Chrome
3. `login()` — autentica no Ômega
4. `navegar()` — vai para página desejada
5. `extrair_tabela()` — extrai dados
6. `fechar()` — encerra navegador

## Notas

- O Ômega usa JSF/Seam (login.seam)
- Campos de login: `#username`, `#password`, `#btnLogin`
- Modo headless para execução sem interface

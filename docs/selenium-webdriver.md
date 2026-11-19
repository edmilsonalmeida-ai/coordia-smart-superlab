# Selenium WebDriver

## Instalação

```bash
pip install selenium webdriver-manager
```

## Uso básico

```python
from selenium_utils import criar_driver, info_ambiente

# Verificar ambiente
print(info_ambiente())

# Criar driver
resultado = criar_driver(headless=True)
if "driver" in resultado:
    driver = resultado["driver"]
    driver.get("https://example.com")
    print(driver.title)
    driver.quit()
else:
    print("Erro:", resultado["erro"])
```

## Detecção automática

O utilitário detecta a versão do Chrome e baixa o ChromeDriver compatível.

## Opções do driver

| Opção | Descrição |
|--------|-----------|
| headless | Executa sem interface gráfica |
| no-sandbox | Necessário em containers |
| disable-gpu | Evita problemas de GPU |
| window-size | Define tamanho da janela |

## Troubleshooting

### Versão incompatível
```python
resultado = criar_driver(versao_chrome="120")
```

### Chrome não encontrado
Instale Chrome ou Chromium:
```bash
apt install chromium-browser
```

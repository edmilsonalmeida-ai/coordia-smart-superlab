"""
Utilitários Selenium WebDriver.
Detecção automática de versão e configuração robusta.
"""

import subprocess
import re
from typing import Optional, Dict

def detectar_versao_chrome() -> Optional[str]:
    """Detecta versão do Chrome/Chromium instalado."""
    comandos = [
        ["google-chrome", "--version"],
        ["chromium", "--version"],
        ["chromium-browser", "--version"],
        ["/usr/bin/chromium", "--version"],
    ]
    for cmd in comandos:
        try:
            resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if resultado.returncode == 0:
                match = re.search(r"(\d+)\.\d+\.\d+", resultado.stdout)
                if match:
                    return match.group(1)
        except Exception:
            continue
    return None

def criar_driver(headless: bool = True, versao_chrome: str = None) -> Dict:
    """
    Cria driver Selenium com configuração robusta.
    
    Retorna {"driver": WebDriver} ou {"erro": str}
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
    except ImportError:
        return {"erro": "Instale: pip install selenium"}

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    # Tenta usar ChromeDriver do sistema primeiro
    try:
        driver = webdriver.Chrome(options=options)
        return {"driver": driver, "metodo": "sistema"}
    except Exception:
        pass

    # Tenta webdriver-manager com versão específica
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        versao = versao_chrome or detectar_versao_chrome()
        if versao:
            service = Service(ChromeDriverManager(driver_version=versao).install())
        else:
            service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return {"driver": driver, "metodo": "webdriver-manager", "versao": versao}
    except Exception as e:
        return {"erro": str(e)}

def info_ambiente() -> Dict:
    """Retorna informações do ambiente Selenium."""
    info = {
        "chrome_versao": detectar_versao_chrome(),
        "selenium_instalado": False,
        "webdriver_manager_instalado": False,
    }
    try:
        import selenium
        info["selenium_instalado"] = True
        info["selenium_versao"] = selenium.__version__
    except ImportError:
        pass
    try:
        import webdriver_manager
        info["webdriver_manager_instalado"] = True
    except ImportError:
        pass
    return info

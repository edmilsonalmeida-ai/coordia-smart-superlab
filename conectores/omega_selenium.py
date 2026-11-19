"""
Automação Selenium para Ômega Educacional.
Acessa o sistema via navegador automatizado.
"""

from typing import Dict, List, Optional
from cofre.credenciais import cofre

class OmegaSelenium:
    """
    Conector Ômega via Selenium.
    
    Requisitos:
    - pip install selenium webdriver-manager
    - Chrome ou Firefox instalado
    """

    def __init__(self):
        self.driver = None
        self.logado = False
        self.url_base = None

    def configurar(self, url_base: str, usuario: str, senha: str) -> Dict:
        """Configura credenciais."""
        cofre.depositar("omega_selenium", usuario, senha, {"url_base": url_base})
        self.url_base = url_base
        return {"status": "configurado", "url": url_base}

    def iniciar_navegador(self, headless: bool = True) -> Dict:
        """Inicia o navegador."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service

            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            return {"status": "navegador_iniciado"}
        except ImportError:
            return {"erro": "Instale: pip install selenium webdriver-manager"}
        except Exception as e:
            return {"erro": str(e)}

    def login(self) -> Dict:
        """Faz login no Ômega."""
        if not self.driver:
            return {"erro": "Navegador não iniciado"}

        creds = cofre.obter("omega_selenium")
        if not creds:
            return {"erro": "Credenciais não configuradas"}

        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            url = creds.get("extras", {}).get("url_base", "")
            self.driver.get(f"{url}/login.seam")

            # Aguarda campos de login
            wait = WebDriverWait(self.driver, 10)
            campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "username")))
            campo_senha = self.driver.find_element(By.ID, "password")

            campo_usuario.send_keys(creds["usuario"])
            campo_senha.send_keys(creds["senha"])

            # Clica no botão de login
            botao = self.driver.find_element(By.ID, "btnLogin")
            botao.click()

            # Aguarda redirecionamento
            wait.until(lambda d: "login" not in d.current_url.lower())
            self.logado = True
            return {"status": "logado", "url": self.driver.current_url}

        except Exception as e:
            return {"erro": str(e)}

    def navegar(self, caminho: str) -> Dict:
        """Navega para uma página."""
        if not self.logado:
            return {"erro": "Não logado"}
        try:
            self.driver.get(f"{self.url_base}/{caminho}")
            return {"status": "navegou", "url": self.driver.current_url}
        except Exception as e:
            return {"erro": str(e)}

    def extrair_tabela(self, seletor: str = "table") -> List[Dict]:
        """Extrai dados de uma tabela."""
        if not self.driver:
            return []
        try:
            from selenium.webdriver.common.by import By
            tabela = self.driver.find_element(By.CSS_SELECTOR, seletor)
            linhas = tabela.find_elements(By.TAG_NAME, "tr")

            dados = []
            headers = []
            for i, linha in enumerate(linhas):
                celulas = linha.find_elements(By.TAG_NAME, "td")
                if not celulas:
                    celulas = linha.find_elements(By.TAG_NAME, "th")
                    headers = [c.text.strip() for c in celulas]
                else:
                    valores = [c.text.strip() for c in celulas]
                    if headers:
                        dados.append(dict(zip(headers, valores)))
                    else:
                        dados.append({"colunas": valores})
            return dados
        except Exception:
            return []

    def fechar(self):
        """Fecha o navegador."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logado = False

    def status(self) -> Dict:
        return {
            "navegador_ativo": self.driver is not None,
            "logado": self.logado,
            "url": self.url_base,
            "credenciais": cofre.tem("omega_selenium")
        }

# Instância global
omega_selenium = OmegaSelenium()

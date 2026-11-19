"""
Automação Selenium para Ômega Educacional.
Usa selenium_utils para criação robusta do driver.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, List
from cofre.credenciais import cofre
from selenium_utils import criar_driver

class OmegaSelenium:
    def __init__(self):
        self.driver = None
        self.logado = False
        self.url_base = None

    def configurar(self, url_base: str, usuario: str, senha: str) -> Dict:
        cofre.depositar("omega_selenium", usuario, senha, {"url_base": url_base})
        self.url_base = url_base
        return {"status": "configurado", "url": url_base}

    def iniciar_navegador(self, headless: bool = True) -> Dict:
        resultado = criar_driver(headless=headless)
        if "driver" in resultado:
            self.driver = resultado["driver"]
            return {"status": "navegador_iniciado", "metodo": resultado.get("metodo")}
        return resultado

    def login(self) -> Dict:
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

            wait = WebDriverWait(self.driver, 15)
            campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "username")))
            campo_senha = self.driver.find_element(By.ID, "password")

            campo_usuario.clear()
            campo_usuario.send_keys(creds["usuario"])
            campo_senha.clear()
            campo_senha.send_keys(creds["senha"])

            botao = self.driver.find_element(By.ID, "btnLogin")
            botao.click()

            import time
            time.sleep(3)

            if "login" not in self.driver.current_url.lower():
                self.logado = True
                return {"status": "logado", "url": self.driver.current_url}
            else:
                return {"status": "falhou", "url": self.driver.current_url, "titulo": self.driver.title}

        except Exception as e:
            return {"erro": str(e)}

    def navegar(self, caminho: str) -> Dict:
        if not self.logado:
            return {"erro": "Não logado"}
        try:
            self.driver.get(f"{self.url_base}/{caminho}")
            return {"status": "navegou", "url": self.driver.current_url}
        except Exception as e:
            return {"erro": str(e)}

    def extrair_tabela(self, seletor: str = "table") -> List[Dict]:
        if not self.driver:
            return []
        try:
            from selenium.webdriver.common.by import By
            tabela = self.driver.find_element(By.CSS_SELECTOR, seletor)
            linhas = tabela.find_elements(By.TAG_NAME, "tr")
            dados = []
            headers = []
            for linha in linhas:
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

    def screenshot(self, caminho: str = "screenshot.png") -> str:
        if self.driver:
            self.driver.save_screenshot(caminho)
            return caminho
        return None

    def fechar(self):
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

omega_selenium = OmegaSelenium()

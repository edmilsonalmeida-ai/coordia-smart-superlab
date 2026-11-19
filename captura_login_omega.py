#!/usr/bin/env python3
"""
Formulário de captura de login Ômega.
Execute localmente para capturar o fluxo de autenticação.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

def capturar_login():
    print("=" * 50)
    print("CAPTURA DE LOGIN ÔMEGA")
    print("=" * 50)
    print()

    # Coleta dados
    url = input("URL base (ex: https://pdl.mt.ed.omegaeducacional.com): ").strip()
    cpf = input("CPF: ").strip()
    senha = input("Senha: ").strip()

    if not url:
        url = "https://pdl.mt.ed.omegaeducacional.com"

    print()
    print("Iniciando navegador (visível)...")

    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f"{url}/login.seam")
        time.sleep(2)

        print("Página carregada. Preenchendo campos...")

        # Preenche
        driver.execute_script(f'''
            document.getElementById("username").value = "{cpf}";
            document.getElementById("password").value = "{senha}";
        ''')

        print("Campos preenchidos. Clique em 'Entrar' no navegador.")
        print("Aguardando 30 segundos para você completar o login...")

        # Aguarda login manual
        for i in range(30):
            time.sleep(1)
            if "login" not in driver.current_url.lower():
                print(f"\nLogin detectado! URL: {driver.current_url}")
                break
            print(f"\rAguardando... {30-i}s", end="")

        print()
        print(f"URL final: {driver.current_url}")
        print(f"Título: {driver.title}")

        # Captura requisições
        print("\n=== Requisições capturadas ===")
        logs = driver.get_log("performance")
        posts = []
        for log in logs:
            try:
                msg = json.loads(log["message"])["message"]
                if msg["method"] == "Network.requestWillBeSent":
                    req = msg["params"]["request"]
                    if req["method"] == "POST" and "login" in req["url"]:
                        posts.append({
                            "url": req["url"],
                            "data": req.get("postData", "")[:500]
                        })
            except:
                pass

        for p in posts:
            print(f"POST: {p['url'][:60]}")
            print(f"  Data: {p['data'][:200]}")

        # Salva resultado
        resultado = {
            "url_final": driver.current_url,
            "titulo": driver.title,
            "posts": posts
        }
        with open("captura_omega.json", "w") as f:
            json.dump(resultado, f, indent=2)
        print("\nResultado salvo em captura_omega.json")

        input("\nPressione Enter para fechar...")

    finally:
        driver.quit()

if __name__ == "__main__":
    capturar_login()

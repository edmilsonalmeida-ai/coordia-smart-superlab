#!/usr/bin/env python3
"""
Captura manual de requisições do Ômega.
Execute localmente, faça o login manual, e o script captura tudo.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

def capturar():
    print("=" * 50)
    print("CAPTURA MANUAL — ÔMEGA")
    print("=" * 50)
    print()
    print("1. O navegador vai abrir")
    print("2. Faça login manualmente")
    print("3. Selecione escola, ano, perfil")
    print("4. Clique em Aplicar parâmetros")
    print("5. Navegue até relatórios")
    print("6. Pressione Enter aqui quando terminar")
    print()

    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://pdl.mt.ed.omegaeducacional.com/login.seam")
        print("Navegador aberto. Faça o login...")
        print()

        input("Pressione Enter quando terminar todas as ações...")

        print()
        print("Capturando requisições...")

        logs = driver.get_log("performance")
        requests = []

        for log in logs:
            try:
                msg = json.loads(log["message"])["message"]
                if msg["method"] == "Network.requestWillBeSent":
                    req = msg["params"]["request"]
                    url = req["url"]
                    if "seam" in url or "rest" in url:
                        requests.append({
                            "method": req["method"],
                            "url": url,
                            "post": req.get("postData", "")[:500]
                        })
            except:
                pass

        # Salva resultado
        with open("captura_omega_manual.json", "w") as f:
            json.dump(requests, f, indent=2, ensure_ascii=False)

        print(f"Capturadas {len(requests)} requisições")
        print("Salvo em: captura_omega_manual.json")
        print()

        # Mostra POSTs
        print("=== POSTs capturados ===")
        for r in requests:
            if r["method"] == "POST":
                print(f"  {r['url'][:60]}")
                if r["post"]:
                    print(f"    {r['post'][:100]}")

    finally:
        driver.quit()

if __name__ == "__main__":
    capturar()

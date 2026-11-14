"""
Exemplo de notificação via webhook (simulado ou real).
Advisory only — apenas envia a recomendação.
"""

import json
from typing import Dict, Any
from urllib.request import Request, urlopen
from urllib.error import URLError

def notificar_webhook(recomendacao: Dict[str, Any], url: str | None = None) -> bool:
    """
    Envia recomendação para webhook.
    Se url for None, apenas imprime (modo simulado).
    """
    payload = {
        "evento": "recomendacao_coordia",
        "dados": recomendacao,
        "aviso": "Advisory only — requer ação humana"
    }
    corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    if not url:
        print("[WEBHOOK SIMULADO]", json.dumps(payload, ensure_ascii=False, indent=2))
        return True

    try:
        req = Request(url, data=corpo, headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=5) as resp:
            return 200 <= resp.status < 300
    except (URLError, TimeoutError):
        return False

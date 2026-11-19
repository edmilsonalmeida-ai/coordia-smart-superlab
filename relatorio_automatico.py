#!/usr/bin/env python3
"""
Relatório automático do CoordIA SMART.
Gera resumo consolidado do sistema.
"""

import json
from datetime import datetime, timezone
from config import status_modo
from plugins.registro import registro
import plugins.detectores_plugin
from resumo_inteligente import gerar

def gerar_relatorio() -> dict:
    status = status_modo()
    log = gerar("auditoria.jsonl")

    return {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "sistema": "COORDIA SMART",
        "modo": {
            "operational_go": status.get("operational_go"),
            "sintetico": status.get("modo_sintetico"),
            "write_escolar": status.get("write_escolar")
        },
        "plugins": registro.listar_detectores(),
        "log": {
            "total": log.get("total", 0),
            "tipos": log.get("por_tipo", {}),
            "alta_prioridade": len(log.get("alta_prioridade", []))
        },
        "aviso": "Advisory only — decisão humana obrigatória"
    }

def salvar(caminho: str = "relatorio_automatico.json"):
    relatorio = gerar_relatorio()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    return relatorio

if __name__ == "__main__":
    r = gerar_relatorio()
    print(json.dumps(r, ensure_ascii=False, indent=2))

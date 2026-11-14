#!/usr/bin/env python3
"""
Painel de status leve do COORDIA SMART.
"""

import json
from pathlib import Path
from integracao.conector import ConectorCoordIA
from resumo_inteligente import gerar

def painel():
    conector = ConectorCoordIA()
    status = conector.status()
    resumo_log = gerar("auditoria.jsonl")

    return {
        "sistema": "COORDIA SMART",
        "modo": status["modo"],
        "operational_go": status["operational_go"],
        "aviso": status["aviso"],
        "log": {
            "total_entradas": resumo_log.get("total", 0),
            "tipos": resumo_log.get("por_tipo", {}),
            "alta_prioridade": len(resumo_log.get("alta_prioridade", []))
        },
        "pronto_para_integracao": True
    }

if __name__ == "__main__":
    print(json.dumps(painel(), ensure_ascii=False, indent=2))

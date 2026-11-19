#!/usr/bin/env python3
"""
Comando unificado do CoordIA SMART.
Um ponto de entrada para tudo.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from orquestrador import Orquestrador
from config import status_modo

def comando(pedido: str, eventos=None):
    """Ponto de entrada único."""
    orch = Orquestrador()
    return orch.pedir(pedido, eventos)

def status():
    return status_modo()

if __name__ == "__main__":
    print("CoordIA SMART — Comando Unificado")
    print("Status:", status())
    print()

    eventos = [
        {"tipo": "frequencia", "valor": 0.45, "aluno_id": "CMD-1", "fonte": "comando"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 5,
         "id_planejamento": "PLN-CMD", "disciplina": "Matemática", "aluno_id": "CMD-2", "fonte": "comando"},
    ]

    print(">>> Conferir pendências")
    r = comando("Conferir pendências", eventos)
    print("Ações:", r["acoes"])
    if "missao" in r:
        print(f"Recomendações: {r['missao']['recomendacoes']}")

    print()
    print(">>> Como está?")
    r2 = comando("Como está?")
    print("Ações:", r2["acoes"])

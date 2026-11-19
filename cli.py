#!/usr/bin/env python3
"""
CLI unificada do CoordIA SMART.
Ponto de entrada para todas as operações.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from comando import comando, status
from di.configuracao import obter_nucleo
from plugins.registro import registro
import plugins.detectores_plugin

def main():
    print("=" * 50)
    print("COORDIA SMART — Sistema Completo")
    print("=" * 50)
    print()

    # Status
    s = status()
    print(f"Modo: {s.get('aviso', 'N/A')}")
    print(f"Operational GO: {s.get('operational_go')}")
    print()

    # Plugins
    print(f"Plugins registrados: {registro.listar_detectores()}")
    print()

    # Demonstração
    eventos = [
        {"tipo": "frequencia", "valor": 0.42, "aluno_id": "CLI-1", "fonte": "cli"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 10,
         "id_planejamento": "PLN-CLI", "disciplina": "Química", "aluno_id": "CLI-2", "fonte": "cli"},
        {"tipo": "nota", "valor": 2.2, "aluno_id": "CLI-3", "fonte": "cli"},
    ]

    print(">>> Processando eventos...")
    r = comando("Conferir pendências", eventos)
    print(f"Ações: {r['acoes']}")
    if "missao" in r:
        print(f"Recomendações: {r['missao']['recomendacoes']}")
        for rec in r["missao"].get("top_prioridades", [])[:3]:
            print(f"  [{rec.get('prioridade', 0):.2f}] {rec['tipo']}")

    print()
    print(">>> Status do sistema")
    r2 = comando("Como está?")
    print(f"Ações: {r2['acoes']}")

    print()
    print("Sistema operacional. Advisory only. Decisão humana obrigatória.")

if __name__ == "__main__":
    main()

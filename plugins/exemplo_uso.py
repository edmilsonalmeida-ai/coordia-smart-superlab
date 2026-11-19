#!/usr/bin/env python3
"""
Exemplo de uso da arquitetura de plugins.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importa plugins (auto-registro)
import plugins.detectores_plugin

from plugins.registro import registro
from agents.nucleo import Nucleo

def main():
    print("Detectores registrados:", registro.listar_detectores())

    # Usa detectores do plugin junto com o núcleo
    nucleo = Nucleo(registro.obter_detectores())

    eventos = [
        {"tipo": "planejamento", "dias_atraso": 20, "fonte": "plugin", "aluno_id": "P1"},
        {"tipo": "nota", "valor": 2.5, "fonte": "plugin", "aluno_id": "P2"},
        {"tipo": "nota", "valor": 7.0, "fonte": "plugin", "aluno_id": "P3"},
    ]

    for ev in eventos:
        recs = nucleo.processar(ev)
        if recs:
            print(f"  [{recs[0].get('prioridade', 0):.2f}] {recs[0]['tipo']}: {recs[0]['recomendacao'][:50]}")
        else:
            print(f"  (sem alerta para {ev.get('tipo')})")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Exemplo de uso da injeção de dependência.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from di.configuracao import configurar, obter_nucleo
from di.container import container

def main():
    configurar()
    print("Dependências registradas:", container.listar())

    nucleo = obter_nucleo()

    eventos = [
        {"tipo": "frequencia", "valor": 0.4, "aluno_id": "DI-1", "fonte": "di"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 18,
         "id_planejamento": "PLN-DI", "disciplina": "Física", "aluno_id": "DI-2", "fonte": "di"},
        {"tipo": "nota", "valor": 2.0, "aluno_id": "DI-3", "fonte": "di"},
    ]

    print("\nProcessando com núcleo injetado:")
    for ev in eventos:
        recs = nucleo.processar(ev)
        if recs:
            print(f"  [{recs[0].get('prioridade', 0):.2f}] {recs[0]['tipo']}")

if __name__ == "__main__":
    main()

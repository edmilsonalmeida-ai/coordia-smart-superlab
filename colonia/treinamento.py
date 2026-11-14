#!/usr/bin/env python3
"""
Treinamento da colônia CoordIA.
Simula cenários e mostra o fluxo correto.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from missoes.missao_001_pendencias import Missao001

def cenario_basico():
    print("=== Cenário 1: Pendências mistas ===")
    missao = Missao001()
    eventos = [
        {"tipo": "frequencia", "valor": 0.42, "aluno_id": "ALU-201", "fonte": "treino"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 12,
         "id_planejamento": "PLN-301", "disciplina": "Português", "aluno_id": "ALU-202", "fonte": "treino"},
        {"tipo": "nota", "valor": 2.8, "aluno_id": "ALU-203", "fonte": "treino"},
    ]
    resultado = missao.executar(eventos)
    print(f"Recomendações: {resultado['recomendacoes']}")
    for rec in resultado["top_prioridades"]:
        print(f"  [{rec.get('prioridade', 0):.2f}] {rec['tipo']}")

    # Decisão humana de exemplo
    if resultado["recomendacoes"] > 0:
        dec = missao.registrar_decisao(0, "aceito", "coordenador-treino", "Cenário de treinamento")
        print(f"Decisão registrada: {dec.get('decisao')}")
    print()

def cenario_alta_prioridade():
    print("=== Cenário 2: Alta urgência ===")
    missao = Missao001()
    eventos = [
        {"tipo": "planejamento", "completo": False, "dias_atraso": 20,
         "id_planejamento": "PLN-URG", "disciplina": "Matemática", "aluno_id": "ALU-URG", "fonte": "treino"},
        {"tipo": "frequencia", "valor": 0.3, "aluno_id": "ALU-URG2", "fonte": "treino"},
    ]
    resultado = missao.executar(eventos)
    print(f"Maior prioridade: {resultado['top_prioridades'][0].get('prioridade') if resultado['top_prioridades'] else 'N/A'}")
    print()

def main():
    print("Treinamento da Colônia CoordIA\n")
    cenario_basico()
    cenario_alta_prioridade()
    print("Treinamento concluído. Colônia pronta para operação.")

if __name__ == "__main__":
    main()

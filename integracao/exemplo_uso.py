#!/usr/bin/env python3
"""
Exemplo de uso da estrutura de integração.
"""

from integracao.conector import ConectorCoordIA

def main():
    conector = ConectorCoordIA()
    print("Status inicial:", conector.status())

    eventos = [
        {"tipo": "frequencia", "valor": 0.55, "aluno_id": "ALU-001", "fonte": "sintetico"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 5,
         "id_planejamento": "PLN-100", "disciplina": "Matemática", "aluno_id": "ALU-002", "fonte": "sintetico"},
        {"tipo": "participacao", "valor": 0.3, "aluno_id": "ALU-003", "fonte": "sintetico"},
    ]

    recomendacoes = conector.processar_lote(eventos)
    print(f"\n{len(recomendacoes)} recomendações geradas (ordenadas por prioridade):")
    for rec in recomendacoes[:5]:
        print(f"  [{rec.get('prioridade', 0):.2f}] {rec['tipo']}: {rec['recomendacao'][:70]}")

    print("\nStatus final:", conector.status())

if __name__ == "__main__":
    main()

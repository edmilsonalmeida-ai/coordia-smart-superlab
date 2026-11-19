"""
Simulação de cenários do CoordIA SMART.
Testa o sistema com diferentes configurações.
"""

from typing import List, Dict
from agents.priorizacao import definir_peso, resetar_pesos, obter_pesos
from di.configuracao import obter_nucleo

def simular_cenario(eventos: List[Dict], pesos_custom: Dict = None) -> Dict:
    """Simula processamento com pesos opcionais."""
    if pesos_custom:
        for tipo, peso in pesos_custom.items():
            definir_peso(tipo, peso)

    nucleo = obter_nucleo()
    todas_recs = []
    for ev in eventos:
        recs = nucleo.processar(ev)
        todas_recs.extend(recs)

    # Ordena por prioridade
    todas_recs.sort(key=lambda r: r.get("prioridade", 0), reverse=True)

    resultado = {
        "eventos": len(eventos),
        "recomendacoes": len(todas_recs),
        "top": todas_recs[:5],
        "pesos_usados": obter_pesos()
    }

    if pesos_custom:
        resetar_pesos()

    return resultado

def comparar_cenarios(eventos: List[Dict], cenarios: List[Dict]) -> List[Dict]:
    """Compara múltiplos cenários de pesos."""
    resultados = []
    for cenario in cenarios:
        r = simular_cenario(eventos, cenario.get("pesos"))
        r["nome"] = cenario.get("nome", "sem_nome")
        resultados.append(r)
    return resultados

if __name__ == "__main__":
    eventos = [
        {"tipo": "frequencia", "valor": 0.4, "aluno_id": "S1", "fonte": "sim"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 10,
         "id_planejamento": "PLN-S", "disciplina": "História", "aluno_id": "S2", "fonte": "sim"},
    ]

    cenarios = [
        {"nome": "padrao", "pesos": None},
        {"nome": "frequencia_alta", "pesos": {"pendencia_frequencia": 2.0}},
        {"nome": "planejamento_alto", "pesos": {"alerta_planejamento": 2.0}},
    ]

    resultados = comparar_cenarios(eventos, cenarios)
    for r in resultados:
        top_tipo = r["top"][0]["tipo"] if r["top"] else "N/A"
        print(f"{r['nome']}: top = {top_tipo}")

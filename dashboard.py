#!/usr/bin/env python3
"""
Dashboard de monitoramento em tempo real.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from monitor import monitor
from di.configuracao import obter_nucleo
from config import status_modo

def executar_demo():
    """Executa operações de demonstração e mostra métricas."""
    nucleo = obter_nucleo()

    eventos = [
        {"tipo": "frequencia", "valor": 0.4, "aluno_id": "D1", "fonte": "dash"},
        {"tipo": "planejamento", "completo": False, "dias_atraso": 5,
         "id_planejamento": "PLN-D", "disciplina": "Física", "aluno_id": "D2", "fonte": "dash"},
        {"tipo": "nota", "valor": 3.0, "aluno_id": "D3", "fonte": "dash"},
        {"tipo": "tarefa", "dias_atraso": 4, "aluno_id": "D4", "fonte": "dash"},
        {"tipo": "participacao", "valor": 0.3, "aluno_id": "D5", "fonte": "dash"},
    ]

    print("Processando eventos...")
    for ev in eventos:
        inicio = monitor.iniciar_operacao()
        recs = nucleo.processar(ev)
        monitor.finalizar_operacao(inicio, True, len(recs))

    return monitor.metricas()

def main():
    print("=" * 50)
    print("DASHBOARD — CoordIA SMART")
    print("=" * 50)
    print()

    # Status do sistema
    status = status_modo()
    print(f"Modo: {status.get('aviso', 'N/A')}")
    print()

    # Executa demo
    metricas = executar_demo()

    print("Métricas de desempenho:")
    print(f"  Uptime: {metricas['uptime_segundos']}s")
    print(f"  Eventos processados: {metricas['eventos_processados']}")
    print(f"  Recomendações geradas: {metricas['recomendacoes_geradas']}")
    print(f"  Tempo médio: {metricas['tempo_medio_ms']}ms")
    print(f"  Tempo máximo: {metricas['tempo_max_ms']}ms")
    print(f"  Eventos/segundo: {metricas['eventos_por_segundo']}")
    print(f"  Taxa de erro: {metricas['taxa_erro']}")
    print()
    print(monitor.resumo())

if __name__ == "__main__":
    main()

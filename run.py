#!/usr/bin/env python3
"""
Runner simples — COORDIA SMART
Processa eventos e mostra recomendações + log.
"""

import json
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from adapters.exemplo_planilha import linhas_para_eventos

def main():
    nucleo = Nucleo(DETECTORES_PADRAO)

    # Exemplo embutido
    csv_exemplo = """tipo,valor,aluno_id,dias_restantes,frequencia,nota_media,pendencias_abertas
frequencia,0.62,A001,,,,
nota,4.2,A002,,,,
prazo,,A003,1,,,
, ,A004,,0.65,4.5,3
"""

    eventos = linhas_para_eventos(csv_exemplo, fonte="demo")
    todas_recs = []

    for ev in eventos:
        recs = nucleo.processar(ev)
        todas_recs.extend(recs)

    print("=== RECOMENDAÇÕES (advisory) ===")
    print(json.dumps(todas_recs, ensure_ascii=False, indent=2))
    print("\n=== LOG DE AUDITORIA ===")
    print(nucleo.exportar_log())
    print(f"\nTotal de recomendações: {len(todas_recs)}")
    print(f"Total de entradas no log: {len(nucleo.log)}")

if __name__ == "__main__":
    main()

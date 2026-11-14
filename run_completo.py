#!/usr/bin/env python3
"""
Runner completo: processa, persiste log e simula webhook.
"""

import json
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from agents.log_persistente import LogPersistente
from integracoes.webhook_exemplo import notificar_webhook
from adapters.exemplo_planilha import linhas_para_eventos

def main():
    nucleo = Nucleo(DETECTORES_PADRAO)
    log = LogPersistente("auditoria.jsonl")

    csv = """tipo,valor,aluno_id,dias_restantes,frequencia,nota_media,pendencias_abertas
frequencia,0.58,A101,,,,
nota,3.8,A102,,,,
prazo,,A103,0,,,
, ,A104,,0.62,4.0,4
"""

    eventos = linhas_para_eventos(csv, fonte="demo_completo")
    print("=== PROCESSANDO ===")

    for ev in eventos:
        recs = nucleo.processar(ev)
        for rec in recs:
            entrada = {"evento": ev, "recomendacao": rec}
            log.registrar(entrada)
            notificar_webhook(rec)  # simulado

    print("\n=== RESUMO ===")
    print(f"Recomendações geradas: {len(nucleo.log)}")
    print(f"Entradas persistidas: {len(log.ler_todos())}")
    print("Log salvo em: auditoria.jsonl")

if __name__ == "__main__":
    main()

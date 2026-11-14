#!/usr/bin/env python3
"""
Runner leve e contínuo — COORDIA SMART
Processa lotes sintéticos pequenos com pausa.
Zero dependências. Advisory only. Baixo consumo.
Integra alertas de erro.
"""

import time
import traceback
from datetime import datetime, timezone
from config import assert_safe_mode
from prototype.alertas_planejamento import processar_alertas_sinteticos
from agents.log_persistente import LogPersistente

def alerta_erro(ciclo: int, erro: Exception) -> dict:
    """Gera alerta advisory de erro com proveniência."""
    return {
        "tipo": "alerta_erro",
        "recomendacao": f"Revisar falha no ciclo {ciclo}: {type(erro).__name__}",
        "origem": "runner_leve",
        "risco": 0.9,
        "status": "recomendado",
        "ciclo": ciclo,
        "erro": str(erro),
        "traceback": traceback.format_exc()[-500:],  # limitado
        "processado_em": datetime.now(timezone.utc).isoformat(),
        "aviso": "Advisory only — requer ação humana"
    }

def main():
    assert_safe_mode()
    log = LogPersistente("auditoria_leve.jsonl")
    ciclo = 0
    print("COORDIA SMART — modo leve iniciado (Ctrl+C para parar)")
    print("Flags: OPERATIONAL_GO=false | WRITE_ESCOLAR=NO_GO | sintético only")
    print("Alertas de erro integrados.")

    try:
        while True:
            ciclo += 1
            try:
                alertas = processar_alertas_sinteticos(5)
                for alerta in alertas:
                    log.registrar({"ciclo": ciclo, "alerta": alerta})
                print(f"[ciclo {ciclo}] {len(alertas)} alertas | log: {len(log.ler_todos())} entradas")
            except Exception as e:
                err_alerta = alerta_erro(ciclo, e)
                log.registrar({"ciclo": ciclo, "alerta_erro": err_alerta})
                print(f"[ciclo {ciclo}] ALERTA DE ERRO registrado: {type(e).__name__}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nModo leve encerrado.")

if __name__ == "__main__":
    main()

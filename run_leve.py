#!/usr/bin/env python3
"""
Runner leve e contínuo — COORDIA SMART
Processa lotes sintéticos pequenos com pausa.
Zero dependências. Advisory only. Baixo consumo.
"""

import time
import json
from config import assert_safe_mode
from prototype.alertas_planejamento import processar_alertas_sinteticos
from agents.log_persistente import LogPersistente

def main():
    assert_safe_mode()
    log = LogPersistente("auditoria_leve.jsonl")
    ciclo = 0
    print("COORDIA SMART — modo leve iniciado (Ctrl+C para parar)")
    print("Flags: OPERATIONAL_GO=false | WRITE_ESCOLAR=NO_GO | sintético only")

    try:
        while True:
            ciclo += 1
            alertas = processar_alertas_sinteticos(5)  # lote pequeno
            for alerta in alertas:
                log.registrar({"ciclo": ciclo, "alerta": alerta})
            print(f"[ciclo {ciclo}] {len(alertas)} alertas | log: {len(log.ler_todos())} entradas")
            time.sleep(10)  # pausa leve
    except KeyboardInterrupt:
        print("\nModo leve encerrado.")

if __name__ == "__main__":
    main()

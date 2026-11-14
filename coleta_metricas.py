#!/usr/bin/env python3
"""
Coletor leve de métricas do processo run_leve.py.
Zero dependências.
"""

import os
import time

def snapshot():
    try:
        with open("/proc/4407/status") as f:  # ajustar PID se necessário
            lines = f.readlines()
        rss = next((l for l in lines if l.startswith("VmRSS")), "VmRSS: n/a")
        return rss.strip()
    except Exception:
        return "processo não encontrado"

if __name__ == "__main__":
    print("Coleta de métricas (3 amostras):")
    for _ in range(3):
        print(snapshot())
        time.sleep(2)

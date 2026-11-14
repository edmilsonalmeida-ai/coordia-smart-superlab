#!/usr/bin/env python3
"""
Verificação completa da fase — COORDIA SMART
Roda todos os testes e gera um resumo.
"""

import subprocess
import sys

def rodar(cmd):
    print(f"\n>>> {cmd}")
    r = subprocess.run(cmd, shell=True)
    return r.returncode == 0

def main():
    ok = True
    ok &= rodar("python tests/supertest_nucleo.py")
    ok &= rodar("python tests/supertest_completo.py")
    ok &= rodar("python tests/test_adversarial_planejamento.py")
    ok &= rodar("python -c \"from config import assert_safe_mode; assert_safe_mode(); print('Flags OK')\"")
    ok &= rodar("python -c \"from prototype.alertas_planejamento import processar_alertas_sinteticos; r=processar_alertas_sinteticos(20); print(len(r), 'alertas')\"")

    print("\n" + ("✓ TUDO PASSOU" if ok else "✗ ALGUM TESTE FALHOU"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

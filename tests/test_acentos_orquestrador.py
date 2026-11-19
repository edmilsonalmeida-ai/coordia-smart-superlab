"""
Testes de reconhecimento de pedidos com acentos.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orquestrador import Orquestrador, normalizar

def test_normalizacao():
    assert normalizar("Pendências") == "pendencias"
    assert normalizar("Como está") == "como esta"
    assert normalizar("Situação") == "situacao"
    assert normalizar("Frequência") == "frequencia"

def test_pedido_com_acento_pendencias():
    orch = Orquestrador()
    eventos = [{"tipo": "frequencia", "valor": 0.5, "aluno_id": "T1", "fonte": "teste"}]
    r = orch.pedir("Conferir pendências", eventos)
    assert "missao_001_executada" in r["acoes"]
    assert r["pedido"] == "Conferir pendências"  # original conservado

def test_pedido_com_acento_status():
    orch = Orquestrador()
    r = orch.pedir("Como está?")
    assert "status_consultado" in r["acoes"]

def test_pedido_sem_acento_legado():
    orch = Orquestrador()
    eventos = [{"tipo": "frequencia", "valor": 0.5, "aluno_id": "T1", "fonte": "teste"}]
    r = orch.pedir("Detectar pendencias", eventos)
    assert "missao_001_executada" in r["acoes"]

if __name__ == "__main__":
    test_normalizacao()
    test_pedido_com_acento_pendencias()
    test_pedido_com_acento_status()
    test_pedido_sem_acento_legado()
    print("✓ Testes de acentos passaram.")

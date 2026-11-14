"""
Cenários sintéticos adicionais para o protótipo de planejamentos.
Todos determinísticos e advisory.
"""

from prototype.alertas_planejamento import gerar_dados_sinteticos, detector_planejamento
from agents.nucleo import Nucleo
from typing import List, Dict

def cenario_atraso_critico(seed: int = 100) -> List[Dict]:
    """Todos incompletos com alto atraso."""
    eventos = gerar_dados_sinteticos(10, seed)
    for ev in eventos:
        ev["completo"] = False
        ev["dias_atraso"] = 15
    return eventos

def cenario_tudo_ok(seed: int = 200) -> List[Dict]:
    """Todos completos, zero alertas esperados."""
    eventos = gerar_dados_sinteticos(10, seed)
    for ev in eventos:
        ev["completo"] = True
        ev["dias_atraso"] = 0
    return eventos

def cenario_misto(seed: int = 300) -> List[Dict]:
    """Mistura controlada."""
    return gerar_dados_sinteticos(30, seed)

def rodar_cenario(nome: str, eventos: List[Dict]) -> Dict:
    nucleo = Nucleo([detector_planejamento])
    alertas = []
    for ev in eventos:
        alertas.extend(nucleo.processar(ev))
    return {
        "cenario": nome,
        "eventos": len(eventos),
        "alertas": len(alertas),
        "status_todos_recomendado": all(a.get("status") == "recomendado" for a in alertas),
        "origem_sintetico": all(a.get("origem") == "sintetico" for a in alertas)
    }

def executar_todos_cenarios() -> List[Dict]:
    from config import assert_safe_mode
    assert_safe_mode()
    return [
        rodar_cenario("atraso_critico", cenario_atraso_critico()),
        rodar_cenario("tudo_ok", cenario_tudo_ok()),
        rodar_cenario("misto", cenario_misto()),
    ]

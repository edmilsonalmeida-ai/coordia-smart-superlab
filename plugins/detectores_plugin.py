"""
Detectores como plugins.
"""

from typing import Dict
from plugins.registro import registro

def detector_atraso_grave(evento: Dict):
    """Plugin: detecta atraso grave (>15 dias)."""
    dias = evento.get("dias_atraso", 0)
    if isinstance(dias, (int, float)) and dias > 15:
        return {
            "tipo": "atraso_grave",
            "recomendacao": f"Atraso grave de {dias} dias — escalonar",
            "origem": evento.get("fonte", "plugin"),
            "risco": 0.95,
            "status": "recomendado"
        }
    return None

def detector_nota_critica(evento: Dict):
    """Plugin: detecta nota crítica (<3)."""
    if evento.get("tipo") == "nota" and evento.get("valor", 10) < 3:
        return {
            "tipo": "nota_critica",
            "recomendacao": f"Nota crítica ({evento.get('valor')}) — intervenção imediata",
            "origem": evento.get("fonte", "plugin"),
            "risco": 0.9,
            "status": "recomendado"
        }
    return None

# Auto-registro
registro.registrar_detector("atraso_grave", detector_atraso_grave)
registro.registrar_detector("nota_critica", detector_nota_critica)

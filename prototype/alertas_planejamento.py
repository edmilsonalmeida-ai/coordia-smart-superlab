"""
Protótipo determinístico de alertas de planejamentos.
Usa apenas dados sintéticos. Advisory only.
Reutiliza o núcleo existente.
"""

from typing import Dict, List, Any
import hashlib

def gerar_dados_sinteticos(n: int = 20, seed: int = 42) -> List[Dict]:
    """Gera planejamentos sintéticos determinísticos."""
    eventos = []
    for i in range(n):
        h = int(hashlib.md5(f"{seed}-{i}".encode()).hexdigest()[:8], 16)
        completo = (h % 5) != 0
        dias_atraso = 0 if completo else (h % 10) + 1
        eventos.append({
            "tipo": "planejamento",
            "id_planejamento": f"PLN-{seed}-{i:03d}",
            "disciplina": ["Matemática", "Português", "Ciências", "História"][h % 4],
            "completo": completo,
            "dias_atraso": dias_atraso,
            "fonte": "sintetico",
            "aluno_id": f"SINT-{i:03d}",
            "ts": f"2026-11-13T21:00:00+00:00"  # fixo para determinismo
        })
    return eventos

def detector_planejamento(evento: Dict) -> Dict | None:
    """Detector determinístico para planejamentos incompletos ou atrasados."""
    if evento.get("tipo") != "planejamento":
        return None
    if not evento.get("completo", True) or evento.get("dias_atraso", 0) > 0:
        risco = min(1.0, 0.4 + evento.get("dias_atraso", 0) * 0.06)
        return {
            "tipo": "alerta_planejamento",
            "recomendacao": f"Revisar planejamento {evento.get('id_planejamento')} ({evento.get('disciplina')}) — atraso de {evento.get('dias_atraso', 0)} dias",
            "origem": evento.get("fonte", "sintetico"),
            "risco": round(risco, 2),
            "aluno_id": evento.get("aluno_id"),
            "id_planejamento": evento.get("id_planejamento"),
            "status": "recomendado"
        }
    return None

def processar_alertas_sinteticos(n: int = 20) -> List[Dict]:
    from config import assert_safe_mode
    assert_safe_mode()
    from agents.nucleo import Nucleo
    nucleo = Nucleo([detector_planejamento])
    eventos = gerar_dados_sinteticos(n)
    resultados = []
    for ev in eventos:
        recs = nucleo.processar(ev)
        resultados.extend(recs)
    return resultados

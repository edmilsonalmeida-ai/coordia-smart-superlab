"""
Validação de eventos e recomendações.
"""

from typing import Dict, List, Tuple

def validar_evento(evento: Dict) -> Tuple[bool, List[str]]:
    """Valida estrutura mínima de um evento."""
    erros = []
    if not isinstance(evento, dict):
        return False, ["evento deve ser dict"]
    if "tipo" not in evento:
        erros.append("campo 'tipo' obrigatório")
    if "fonte" not in evento:
        erros.append("campo 'fonte' obrigatório")
    return len(erros) == 0, erros

def validar_recomendacao(rec: Dict) -> Tuple[bool, List[str]]:
    """Valida estrutura de uma recomendação."""
    erros = []
    if rec.get("status") != "recomendado":
        erros.append("status deve ser 'recomendado'")
    if "tipo" not in rec:
        erros.append("campo 'tipo' obrigatório")
    if "recomendacao" not in rec:
        erros.append("campo 'recomendacao' obrigatório")
    if "resolvido" in str(rec).lower() or "executado" in str(rec).lower():
        erros.append("confirmação indevida detectada")
    return len(erros) == 0, erros

def validar_lote(eventos: List[Dict]) -> Dict:
    """Valida um lote de eventos."""
    validos = 0
    invalidos = []
    for i, ev in enumerate(eventos):
        ok, erros = validar_evento(ev)
        if ok:
            validos += 1
        else:
            invalidos.append({"indice": i, "erros": erros})
    return {
        "total": len(eventos),
        "validos": validos,
        "invalidos": len(invalidos),
        "detalhes": invalidos[:5]
    }

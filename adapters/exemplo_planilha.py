"""
Adapter de exemplo: transforma linhas de planilha/CSV em eventos.
Não depende de bibliotecas externas.
"""

import csv
from io import StringIO
from typing import List, Dict

def _safe_float(val):
    if val is None or str(val).strip() == "":
        return None
    try:
        return float(str(val).strip())
    except ValueError:
        return None

def _safe_int(val):
    if val is None or str(val).strip() == "":
        return None
    try:
        return int(float(str(val).strip()))
    except ValueError:
        return None

def linhas_para_eventos(csv_texto: str, fonte: str = "planilha") -> List[Dict]:
    """Converte CSV simples em lista de eventos."""
    eventos = []
    reader = csv.DictReader(StringIO(csv_texto.strip()))
    for row in reader:
        evento = {
            "tipo": (row.get("tipo") or "").strip() or "desconhecido",
            "valor": _safe_float(row.get("valor")),
            "aluno_id": (row.get("aluno_id") or "").strip() or None,
            "fonte": fonte,
            "dias_restantes": _safe_int(row.get("dias_restantes")),
            "frequencia": _safe_float(row.get("frequencia")),
            "nota_media": _safe_float(row.get("nota_media")),
            "pendencias_abertas": _safe_int(row.get("pendencias_abertas")) or 0,
        }
        evento = {k: v for k, v in evento.items() if v is not None}
        if evento.get("tipo") != "desconhecido" or len(evento) > 2:
            eventos.append(evento)
    return eventos

if __name__ == "__main__":
    exemplo = """tipo,valor,aluno_id,dias_restantes
frequencia,0.62,A001,
nota,4.2,A002,
prazo,,A003,2
"""
    print(linhas_para_eventos(exemplo))

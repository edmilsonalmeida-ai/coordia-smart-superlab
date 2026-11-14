"""
Adaptador de planilha (CSV/Excel-like) para o ConectorCoordIA.
Aceita dados em formato tabular e converte para EventoEscolar.
"""

import csv
from typing import List, Dict
from io import StringIO

def csv_para_eventos(conteudo_csv: str) -> List[Dict]:
    """Converte CSV em lista de eventos."""
    eventos = []
    reader = csv.DictReader(StringIO(conteudo_csv))
    for row in reader:
        evento = {
            "tipo": row.get("tipo", "desconhecido"),
            "aluno_id": row.get("aluno_id", ""),
            "fonte": row.get("fonte", "planilha"),
        }
        # Campos numéricos opcionais
        for campo in ("valor", "dias_atraso", "dias_restantes"):
            if row.get(campo):
                try:
                    evento[campo] = float(row[campo])
                except ValueError:
                    pass
        if row.get("completo"):
            evento["completo"] = row["completo"].lower() in ("true", "1", "sim")
        if row.get("disciplina"):
            evento["disciplina"] = row["disciplina"]
        if row.get("id_planejamento"):
            evento["id_planejamento"] = row["id_planejamento"]
        eventos.append(evento)
    return eventos

def processar_csv(conteudo_csv: str):
    """Atalho: CSV → eventos → recomendações."""
    from integracao.conector import ConectorCoordIA
    conector = ConectorCoordIA()
    eventos = csv_para_eventos(conteudo_csv)
    return conector.processar_lote(eventos)

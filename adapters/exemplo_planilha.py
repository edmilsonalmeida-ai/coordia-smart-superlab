"""
Adapter de exemplo: transforma linhas de planilha/CSV em eventos.
Não depende de bibliotecas externas.
"""

import csv
from io import StringIO
from typing import List, Dict

def linhas_para_eventos(csv_texto: str, fonte: str = "planilha") -> List[Dict]:
    """Converte CSV simples em lista de eventos."""
    eventos = []
    reader = csv.DictReader(StringIO(csv_texto))
    for row in reader:
        evento = {
            "tipo": row.get("tipo", "desconhecido"),
            "valor": float(row["valor"]) if row.get("valor") else None,
            "aluno_id": row.get("aluno_id"),
            "fonte": fonte,
            "dias_restantes": int(row["dias_restantes"]) if row.get("dias_restantes") else None,
            "frequencia": float(row["frequencia"]) if row.get("frequencia") else None,
            "nota_media": float(row["nota_media"]) if row.get("nota_media") else None,
            "pendencias_abertas": int(row["pendencias_abertas"]) if row.get("pendencias_abertas") else 0,
        }
        # Remove Nones
        evento = {k: v for k, v in evento.items() if v is not None}
        eventos.append(evento)
    return eventos

# Exemplo de uso
if __name__ == "__main__":
    exemplo = """tipo,valor,aluno_id,dias_restantes
frequencia,0.62,A001,
nota,4.2,A002,
prazo,,A003,2
"""
    print(linhas_para_eventos(exemplo))

"""
Registro de decisão humana sobre uma recomendação.
Separa claramente recomendação (IA) de ação (humano).
"""

from datetime import datetime, timezone
from typing import Dict, Any, Literal

StatusDecisao = Literal["aceito", "rejeitado", "modificado", "em_revisao"]

def registrar_decisao(
    recomendacao_id: str,
    decisao: StatusDecisao,
    responsavel: str,
    observacao: str = "",
    recomendacao_original: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """
    Cria registro imutável da decisão humana.
    Nunca altera a recomendação original.
    """
    return {
        "tipo": "decisao_humana",
        "recomendacao_id": recomendacao_id,
        "decisao": decisao,
        "responsavel": responsavel,
        "observacao": observacao,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "recomendacao_original": recomendacao_original or {},
        "aviso": "Ação humana registrada — distinta da recomendação da IA"
    }

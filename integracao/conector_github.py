"""
Conector GitHub para a colônia.
Permite registrar missões e decisões como issues ou comentários.
"""

from typing import Dict

def preparar_issue_missao(resultado_missao: Dict) -> Dict:
    """Prepara dados para criar uma issue com o resultado da missão."""
    return {
        "title": f"[{resultado_missao.get('missao')}] {resultado_missao.get('nome')}",
        "body": (
            f"**Missão executada**\n\n"
            f"- Eventos: {resultado_missao.get('eventos_processados')}\n"
            f"- Recomendações: {resultado_missao.get('recomendacoes')}\n"
            f"- Modo: {resultado_missao.get('modo')}\n\n"
            f"**Aviso:** {resultado_missao.get('aviso')}"
        ),
        "labels": ["coordia-smart", "missao"]
    }

def preparar_comentario_decisao(decisao: Dict) -> str:
    return (
        f"**Decisão humana registrada**\n"
        f"- Decisão: {decisao.get('decisao')}\n"
        f"- Responsável: {decisao.get('responsavel')}\n"
        f"- Observação: {decisao.get('observacao', '')}"
    )

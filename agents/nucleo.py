"""
Núcleo COORDIA SMART — versão potencializada.
Evento → detectores → priorização → log imutável.
Advisory only.
"""

from typing import List, Dict, Callable
from agents.priorizacao import priorizar
from agents.log_persistente import LogPersistente
from datetime import datetime, timezone

class Nucleo:
    def __init__(self, detectores: List[Callable]):
        self.detectores = detectores
        self.log = LogPersistente("auditoria.jsonl")

    def processar(self, evento: Dict) -> List[Dict]:
        recomendacoes = []
        for detector in self.detectores:
            try:
                rec = detector(evento)
                if rec:
                    if isinstance(rec, list):
                        recomendacoes.extend(rec)
                    else:
                        recomendacoes.append(rec)
            except Exception as e:
                recomendacoes.append({
                    "tipo": "alerta_erro",
                    "recomendacao": f"Falha no detector: {type(e).__name__}",
                    "origem": "nucleo",
                    "risco": 0.8,
                    "status": "recomendado",
                    "erro": str(e)
                })

        # Prioriza
        priorizadas = priorizar(recomendacoes)

        # Enriquece com metadados
        for rec in priorizadas:
            rec.setdefault("processado_em", datetime.now(timezone.utc).isoformat())
            rec.setdefault("aviso", "Advisory only — requer ação humana")
            self.log.registrar({"evento": evento, "recomendacao": rec})

        return priorizadas

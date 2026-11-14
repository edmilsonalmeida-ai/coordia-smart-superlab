"""
Núcleo mínimo e eficiente — COORDIA SMART
Zero dependências externas. Advisory only.
"""

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List
import json

LogEntry = Dict[str, Any]
Detector = Callable[[Dict], Dict | None]

class Nucleo:
    def __init__(self, detectores: List[Detector] | None = None):
        self.detectores = detectores or []
        self.log: List[LogEntry] = []

    def processar(self, evento: Dict) -> List[Dict]:
        """Processa um evento e retorna recomendações (nunca altera estado final)."""
        recomendacoes = []
        for detector in self.detectores:
            rec = detector(evento)
            if rec:
                rec.setdefault("status", "recomendado")
                rec["processado_em"] = datetime.now(timezone.utc).isoformat()
                recomendacoes.append(rec)
                self._registrar(evento, rec)
        return recomendacoes

    def adicionar_detector(self, detector: Detector) -> None:
        self.detectores.append(detector)

    def _registrar(self, evento: Dict, rec: Dict) -> None:
        self.log.append({
            "evento": evento,
            "recomendacao": rec,
            "ts": datetime.now(timezone.utc).isoformat()
        })

    def exportar_log(self) -> str:
        return json.dumps(self.log, ensure_ascii=False, indent=2)

# Exemplo de detector leve
def detector_frequencia(evento: Dict) -> Dict | None:
    if evento.get("tipo") == "frequencia" and evento.get("valor", 1.0) < 0.75:
        return {
            "tipo": "pendencia_frequencia",
            "recomendacao": "Verificar ausências recentes",
            "origem": evento.get("fonte", "desconhecida"),
            "risco": round(1.0 - evento["valor"], 2)
        }
    return None

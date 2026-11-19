"""
Monitoramento de desempenho em tempo real do CoordIA SMART.
"""

import time
from typing import Dict, List
from datetime import datetime, timezone
from collections import deque

class Monitor:
    def __init__(self, janela: int = 100):
        self.inicio = time.time()
        self.janela = janela
        self.tempos: deque = deque(maxlen=janela)
        self.eventos = 0
        self.recomendacoes = 0
        self.erros = 0
        self.ultimo_evento = None

    def iniciar_operacao(self) -> float:
        """Marca início de uma operação. Retorna timestamp."""
        return time.time()

    def finalizar_operacao(self, inicio: float, sucesso: bool = True, recs: int = 0):
        """Registra fim de uma operação."""
        duracao = time.time() - inicio
        self.tempos.append(duracao)
        self.eventos += 1
        self.recomendacoes += recs
        if not sucesso:
            self.erros += 1
        self.ultimo_evento = datetime.now(timezone.utc).isoformat()

    def metricas(self) -> Dict:
        """Retorna métricas atuais."""
        uptime = time.time() - self.inicio
        tempos_lista = list(self.tempos)

        return {
            "uptime_segundos": round(uptime, 1),
            "eventos_processados": self.eventos,
            "recomendacoes_geradas": self.recomendacoes,
            "erros": self.erros,
            "taxa_erro": round(self.erros / max(1, self.eventos), 3),
            "tempo_medio_ms": round(sum(tempos_lista) / len(tempos_lista) * 1000, 2) if tempos_lista else 0,
            "tempo_max_ms": round(max(tempos_lista) * 1000, 2) if tempos_lista else 0,
            "eventos_por_segundo": round(self.eventos / max(0.1, uptime), 2),
            "ultimo_evento": self.ultimo_evento
        }

    def resumo(self) -> str:
        m = self.metricas()
        return (
            f"Uptime: {m['uptime_segundos']}s | "
            f"Eventos: {m['eventos_processados']} | "
            f"Recs: {m['recomendacoes_geradas']} | "
            f"Tempo médio: {m['tempo_medio_ms']}ms | "
            f"Erros: {m['erros']}"
        )

# Instância global
monitor = Monitor()

def monitorar(func):
    """Decorator para monitorar funções."""
    def wrapper(*args, **kwargs):
        inicio = monitor.iniciar_operacao()
        try:
            resultado = func(*args, **kwargs)
            recs = len(resultado) if isinstance(resultado, list) else 0
            monitor.finalizar_operacao(inicio, True, recs)
            return resultado
        except Exception as e:
            monitor.finalizar_operacao(inicio, False)
            raise
    return wrapper

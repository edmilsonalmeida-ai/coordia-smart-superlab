"""
Alertas automáticos de falhas do CoordIA SMART.
Detecta e registra falhas em tempo real.
"""

from typing import Dict, List, Callable
from datetime import datetime, timezone
from collections import deque

class AlertaFalha:
    def __init__(self, max_alertas: int = 100):
        self.alertas: deque = deque(maxlen=max_alertas)
        self.callbacks: List[Callable] = []
        self.thresholds = {
            "taxa_erro_max": 0.1,  # 10%
            "tempo_max_ms": 1000,  # 1 segundo
            "erros_consecutivos": 3
        }
        self.erros_consecutivos = 0

    def registrar_callback(self, callback: Callable):
        """Registra função para ser chamada quando alerta é gerado."""
        self.callbacks.append(callback)

    def verificar(self, metricas: Dict) -> List[Dict]:
        """Verifica métricas e gera alertas se necessário."""
        novos_alertas = []

        # Taxa de erro alta
        if metricas.get("taxa_erro", 0) > self.thresholds["taxa_erro_max"]:
            alerta = self._criar_alerta(
                "taxa_erro_alta",
                f"Taxa de erro {metricas['taxa_erro']:.1%} acima do limite {self.thresholds['taxa_erro_max']:.1%}",
                "alto"
            )
            novos_alertas.append(alerta)

        # Tempo de resposta alto
        if metricas.get("tempo_medio_ms", 0) > self.thresholds["tempo_max_ms"]:
            alerta = self._criar_alerta(
                "latencia_alta",
                f"Tempo médio {metricas['tempo_medio_ms']}ms acima do limite {self.thresholds['tempo_max_ms']}ms",
                "medio"
            )
            novos_alertas.append(alerta)

        # Erros consecutivos
        if self.erros_consecutivos >= self.thresholds["erros_consecutivos"]:
            alerta = self._criar_alerta(
                "erros_consecutivos",
                f"{self.erros_consecutivos} erros consecutivos",
                "critico"
            )
            novos_alertas.append(alerta)

        # Dispara callbacks
        for alerta in novos_alertas:
            for callback in self.callbacks:
                try:
                    callback(alerta)
                except Exception:
                    pass

        return novos_alertas

    def registrar_erro(self):
        """Registra um erro para contagem consecutiva."""
        self.erros_consecutivos += 1

    def registrar_sucesso(self):
        """Reseta contagem de erros consecutivos."""
        self.erros_consecutivos = 0

    def _criar_alerta(self, tipo: str, mensagem: str, severidade: str) -> Dict:
        alerta = {
            "tipo": tipo,
            "mensagem": mensagem,
            "severidade": severidade,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "ativo"
        }
        self.alertas.append(alerta)
        return alerta

    def listar(self, limite: int = 10) -> List[Dict]:
        return list(self.alertas)[-limite:]

    def definir_threshold(self, nome: str, valor: float):
        self.thresholds[nome] = valor

# Instância global
alerta_falha = AlertaFalha()

def callback_log(alerta: Dict):
    """Callback padrão: imprime alerta."""
    print(f"[ALERTA {alerta['severidade'].upper()}] {alerta['tipo']}: {alerta['mensagem']}")

alerta_falha.registrar_callback(callback_log)

"""
Aprendizado leve do CoordIA SMART.
Ajusta pesos com base em feedback acumulado.
Não altera regras automaticamente — apenas sugere.
"""

from typing import Dict, List
from collections import Counter
from agents.feedback import registrar_feedback
from agents.priorizacao import definir_peso, obter_pesos

class Aprendizado:
    def __init__(self):
        self.feedbacks: List[Dict] = []

    def registrar(self, tipo: str, resultado: str):
        """resultado: util | nao_util | falso_positivo | falso_negativo"""
        entrada = {"tipo": tipo, "resultado": resultado}
        self.feedbacks.append(entrada)
        registrar_feedback(tipo, resultado)
        return entrada

    def analisar(self) -> Dict:
        """Analisa feedbacks e sugere ajustes."""
        if not self.feedbacks:
            return {"sugestoes": [], "aviso": "Sem feedbacks"}

        por_tipo = {}
        for fb in self.feedbacks:
            tipo = fb["tipo"]
            if tipo not in por_tipo:
                por_tipo[tipo] = {"util": 0, "nao_util": 0}
            if fb["resultado"] in ("util",):
                por_tipo[tipo]["util"] += 1
            else:
                por_tipo[tipo]["nao_util"] += 1

        sugestoes = []
        for tipo, contagem in por_tipo.items():
            total = contagem["util"] + contagem["nao_util"]
            if total >= 3:
                taxa_util = contagem["util"] / total
                if taxa_util < 0.3:
                    sugestoes.append({
                        "tipo": tipo,
                        "acao": "reduzir_peso",
                        "motivo": f"Taxa de utilidade baixa ({taxa_util:.0%})"
                    })
                elif taxa_util > 0.8:
                    sugestoes.append({
                        "tipo": tipo,
                        "acao": "aumentar_peso",
                        "motivo": f"Taxa de utilidade alta ({taxa_util:.0%})"
                    })

        return {"sugestoes": sugestoes, "total_feedbacks": len(self.feedbacks)}

    def aplicar_sugestoes(self, confirmacao: str = None) -> List[str]:
        """Aplica sugestões somente com confirmação explícita."""
        if confirmacao != "APLICAR":
            return ["Confirmação necessária: aplicar_sugestoes('APLICAR')"]

        analise = self.analisar()
        aplicadas = []
        pesos = obter_pesos()

        for sug in analise.get("sugestoes", []):
            tipo = sug["tipo"]
            peso_atual = pesos.get(tipo, 1.0)
            if sug["acao"] == "reduzir_peso":
                definir_peso(tipo, max(0.5, peso_atual * 0.8))
                aplicadas.append(f"{tipo}: peso reduzido")
            elif sug["acao"] == "aumentar_peso":
                definir_peso(tipo, min(2.0, peso_atual * 1.2))
                aplicadas.append(f"{tipo}: peso aumentado")

        return aplicadas

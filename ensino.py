#!/usr/bin/env python3
"""
Módulo de ensino do CoordIA SMART.
Gera explicações e exemplos para a colônia.
"""

from typing import Dict, List

LICOES = {
    "advisory": {
        "titulo": "Princípio Advisory",
        "conteudo": "Recomendação nunca confirma trabalho concluído. O status é sempre 'recomendado'. A decisão é humana.",
        "exemplo": "alerta_planejamento → status: recomendado (não 'resolvido')"
    },
    "priorizacao": {
        "titulo": "Priorização",
        "conteudo": "prioridade = risco × fator_tipo × fator_urgencia × impacto. Pesos são ajustáveis.",
        "exemplo": "alerta_erro (1.6) > risco_evasao (1.5) > pendencia_prazo (1.4)"
    },
    "plugins": {
        "titulo": "Plugins",
        "conteudo": "Detectores se registram dinamicamente. Não é preciso alterar o núcleo.",
        "exemplo": "registro.registrar_detector('meu_detector', funcao)"
    },
    "di": {
        "titulo": "Injeção de Dependência",
        "conteudo": "Componentes recebem dependências. Facilita testes e troca de implementações.",
        "exemplo": "nucleo = obter_nucleo()  # já configurado"
    },
    "decisao": {
        "titulo": "Decisão Humana",
        "conteudo": "A IA recomenda. O humano decide. A decisão é registrada separadamente.",
        "exemplo": "missao.registrar_decisao(0, 'aceito', 'coordenador', 'Ok')"
    }
}

def listar_licoes() -> List[str]:
    return list(LICOES.keys())

def ensinar(topico: str) -> Dict:
    return LICOES.get(topico, {"erro": f"Tópico '{topico}' não encontrado"})

def ensinar_tudo() -> List[Dict]:
    return [{"topico": k, **v} for k, v in LICOES.items()]

if __name__ == "__main__":
    print("Lições disponíveis:", listar_licoes())
    print()
    for licao in ensinar_tudo():
        print(f"=== {licao['titulo']} ===")
        print(licao["conteudo"])
        print(f"Exemplo: {licao['exemplo']}")
        print()

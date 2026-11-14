# Manual — CoordIA SMART
**Câmara Extra**

## Início rápido

```bash
git clone https://github.com/edmilsonalmeida-ai/coordia-smart-superlab
cd coordia-smart-superlab
python painel_status.py
python missoes/missao_001_pendencias.py
```

## Uso do Orquestrador

```python
from orquestrador import Orquestrador

orch = Orquestrador()
resultado = orch.pedir("Detectar e priorizar pendências", eventos)
print(resultado["acoes"])
```

## Uso da Missão 001

```python
from missoes.missao_001_pendencias import Missao001

missao = Missao001()
resultado = missao.executar(eventos)
missao.registrar_decisao(0, "aceito", "coordenador", "Ação tomada")
```

## Orquestração de agentes

```python
from orquestrador_agentes import OrquestradorAgentes

orch = OrquestradorAgentes()
resultado = orch.executar_fluxo(eventos)
```

## Ajuste de pesos

```python
from agents.priorizacao import definir_peso, obter_pesos
definir_peso("pendencia_frequencia", 1.8)
```

## API

```bash
python integracao/api_integracao.py
# GET  /status
# POST /processar
# POST /decidir
```

## Regras invioláveis

- Recomendação ≠ confirmação de trabalho
- Decisão humana obrigatória
- Log JSONL local (append-only por convenção; integridade independente pendente)
- Advisory only

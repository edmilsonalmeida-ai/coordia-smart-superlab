# Integração CoordIA / Comandantes General

**Autorização total concedida.** Estrutura criada de forma controlada.

## Componentes

| Arquivo | Função |
|---------|---------|
| `integracao/contrato.py` | Contrato de dados (EventoEscolar, Recomendacao) |
| `integracao/conector.py` | Conector principal com modo controlado |
| `integracao/exemplo_uso.py` | Demonstração |

## Como usar

```python
from integracao.conector import ConectorCoordIA

conector = ConectorCoordIA()
recomendacoes = conector.processar_lote(eventos)
```

## Ativação operacional (quando autorizado)

```python
conector.ativar_operacional("AUTORIZADO-EXPLICITO")
```

## O que ainda é necessário para dados reais

1. Conector concreto (API, planilha ou banco do CoordIA)
2. Mapeamento de IDs reais
3. Interface de decisão humana
4. Processo de ativação das flags

A estrutura está pronta para receber o conector real.

# Guia da Colônia CoordIA

**Para todos os agentes e coordenadores.**

## O que é o CoordIA SMART

Sistema de detecção e priorização de pendências escolares com:
- Recomendações advisory (nunca confirmam trabalho concluído)
- Priorização dinâmica
- Decisão humana obrigatória
- Log imutável
- Modo operacional ativo

## Como a colônia deve operar

1. **Receber eventos** (frequência, planejamento, notas, tarefas, participação)
2. **Processar** via Missão 001 ou ConectorCoordIA
3. **Priorizar** automaticamente
4. **Encaminhar** para decisão humana
5. **Registrar** a decisão e o feedback

## Regras invioláveis

- Recomendação ≠ confirmação de trabalho
- Toda ação final exige humano
- Tudo fica no log
- Pesos podem ser ajustados, regras não mudam sozinhas

## Comandos úteis

```bash
python missoes/missao_001_pendencias.py
python painel_status.py
python integracao/exemplo_uso.py
```

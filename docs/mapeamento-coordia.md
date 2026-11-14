# Mapeamento SMART → CoordIA

## Analogia Arquitetural

| SMART / FMDS (FAA) | CoordIA (Escolar) |
|--------------------|-------------------|
| FMDS: integração de dados de fluxo, capacidade, planos | Integração de dados escolares (notas, frequência, documentos, prazos, riscos) com proveniência |
| SMART: antecipa congestionamentos e recomenda ajustes | Antecipa pendências e recomenda encaminhamentos/intervenções |
| Especialistas validam recomendações | Coordenadores/equipes verificam e decidem |
| Trilha de aceitação local | Registro auditável: recomendado → revisado → executado |

## Requisitos de Não-Transformação

A IA **nunca** deve:
- Marcar pendência como resolvida sem ação humana verificada
- Gerar falsas confirmações de trabalho concluído
- Ocultar a origem ou o status de verificação dos dados

## Agentes Especializados Propostos

1. **Agente Detector de Pendências** — Analisa dados e projeta riscos
2. **Agente de Priorização** — Ranqueia por impacto e urgência
3. **Agente de Encaminhamento** — Propõe ações e responsáveis
4. **Agente Auditor** — Mantém trilha de proveniência e verificação

Todos advisory. Decisão e execução humanas.

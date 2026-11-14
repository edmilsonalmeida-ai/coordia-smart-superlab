# Camadas da Arquitetura COORDIA SMART

## 1. Camada de Dados / Integração (FMDS-like)

- Coleta e normalização
- Proveniência obrigatória (origem, timestamp, fonte)
- Disponibilidade e confiabilidade
- Interface para sistemas escolares existentes

## 2. Camada de Inteligência Preditiva (SMART-like)

- Agentes especializados
- Detecção de padrões e projeção de riscos
- Geração de recomendações priorizadas
- **Advisory only** — não executa nem confirma

## 3. Camada de Decisão e Execução Humana

- Revisão por coordenador/equipe
- Aceite / rejeição / modificação
- Registro de ação efetiva
- Verificação posterior

## 4. Camada de Auditoria

- Trilha completa e imutável
- Quem viu o quê, quando, e o que fez
- Distinção clara entre recomendação e fato consumado

## Diagrama Conceitual

```
Dados Escolares
     ↓
[ Camada Integração + Proveniência ]
     ↓
[ Agentes Preditivos SMART-like ] → Recomendações
     ↓
[ Humanos: Revisão + Decisão + Execução ]
     ↓
[ Auditoria Verificável ]
```

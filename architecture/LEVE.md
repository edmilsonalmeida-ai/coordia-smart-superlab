# Arquitetura Leve e Extensível — COORDIA SMART

**Princípio:** Núcleo mínimo. Tudo o resto é opcional e plugável.

## Núcleo (obrigatório, ~100 linhas)

```
Evento → Detector → Recomendação (advisory) → Humano decide → Log imutável
```

- Dados entram como eventos simples (JSON).
- Agente gera apenas recomendação + proveniência.
- Nunca altera estado de “resolvido”.
- Log é append-only (arquivo, SQLite ou stream).

## Extensibilidade (sempre possível)

| Camada | Como estender | Custo |
|--------|---------------|-------|
| Fontes de dados | Adapter (1 função) | Baixo |
| Detectores | Plugin (função pura) | Baixo |
| Priorização | Regra ou modelo | Baixo |
| Notificação / Integração | Webhook ou fila | Baixo |
| Armazenamento | Troca de backend | Médio |

## Regras de design

1. **Funções puras** sempre que possível.
2. **Nenhum agente tem permissão de escrita** no estado final.
3. **Interfaces mínimas**: entrada = dict, saída = dict + log.
4. **Zero dependências obrigatórias** além de Python stdlib (ou o que já existe no ambiente).
5. **Adaptação = novo arquivo**, não mudança no núcleo.

## Exemplo de fluxo mínimo

```python
def detectar(evento: dict) -> dict:
    return {
        "tipo": "pendencia",
        "recomendacao": "verificar frequência",
        "origem": evento.get("fonte"),
        "timestamp": evento.get("ts"),
        "status": "recomendado"  # imutável pelo agente
    }
```

## O que NÃO fazemos

- Orquestração pesada
- Frameworks de agentes complexos
- Estado compartilhado mutável
- Confirmação automática

## Como integrar algo novo

1. Crie um adapter que emita eventos no formato esperado.
2. (Opcional) Crie um detector que consuma esses eventos.
3. O núcleo e o log continuam iguais.

Arquitetura simples hoje, extensível amanhã.

# Missão Concluída — Reconhecimento de Acentos

**Data:** 18/11/2026  
**Status:** Concluída

## Problema original

`pedir("Conferir pendências")` retornava lista vazia de ações porque a comparação era case-sensitive em relação a acentos.

## Solução

Normalização Unicode (NFD + remoção de combining characters) antes da comparação de intenção. O pedido original é conservado no histórico.

## Verificação

- "Conferir pendências" → missão executada
- "Como está?" → status consultado
- "Detectar pendencias" (sem acento) → continua funcionando

Missão concluída.

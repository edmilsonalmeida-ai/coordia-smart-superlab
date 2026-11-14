# Requisitos de Auditoria Verificável

## Campos Obrigatórios em Toda Recomendação

- `id_recomendacao`
- `timestamp_geracao`
- `dados_origem` (lista com fonte, hash ou referência, timestamp)
- `agente_origem`
- `recomendacao_texto`
- `status`: sempre iniciar como `recomendado`

## Transições de Status Permitidas

```
recomendado → em_revisao (humano abre)
recomendado → rejeitado (humano)
recomendado → modificado (humano)
em_revisao → aceito (humano)
aceito → executado (humano registra ação)
executado → verificado (humano confirma resultado)
```

**Proibido**: qualquer transição automática para `resolvido` ou `executado` por agente.

## Registro

Todo evento deve ser imutável e timestampado com identidade do ator (humano ou sistema).

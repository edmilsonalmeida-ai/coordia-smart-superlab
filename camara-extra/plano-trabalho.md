# Plano de Trabalho — O que ainda falta
**Data:** 18/11/2026  
**Status atual:** Sistema operacional em modo lab/controlado

---

## P0 — Crítico (bloqueia operação real)

| # | Item | Descrição | Esforço |
|---|------|-----------|----------|
| 1 | Conector escolar real | Integração com sistema de gestão escolar (API, banco ou planilha institucional) | Alto |
| 2 | Autenticação de usuários | Login de coordenadores/comandantes com permissões | Alto |
| 3 | Interface de decisão | Tela ou endpoint para o humano aceitar/rejeitar recomendações | Médio |
| 4 | Proteção de branch | Regras no GitHub para proteger `main` | Baixo |

---

## P1 — Importante (melhora operação)

| # | Item | Descrição | Esforço |
|---|------|-----------|----------|
| 5 | Persistência de decisões | Banco de dados para histórico de decisões (hoje é JSONL local) | Médio |
| 6 | Notificações | Envio de alertas por e-mail/Slack quando há alta prioridade | Médio |
| 7 | Thresholds por disciplina | Regras diferentes para Matemática vs Educação Física | Baixo |
| 8 | Idempotência | Evitar reprocessamento após reinício | Médio |
| 9 | Logs estruturados | Formato padronizado para análise externa | Baixo |

---

## P2 — Desejável (evolução)

| # | Item | Descrição | Esforço |
|---|------|-----------|----------|
| 10 | Dashboard web | Interface visual para métricas e recomendações | Alto |
| 11 | Integração GPT real | Conectar sugestões ousadas (orquestrador, gerador de detectores) | Alto |
| 12 | Multi-tenant | Suporte a múltiplas escolas/unidades | Alto |
| 13 | Backup automático | Rotina de backup dos logs e decisões | Baixo |
| 14 | Testes de carga | Verificar comportamento com volume real | Médio |

---

## P3 — Futuro (quando estabilizar)

| # | Item | Descrição |
|---|------|-----------|
| 15 | Machine learning | Modelos preditivos além de regras |
| 16 | App mobile | Acesso para coordenadores em campo |
| 17 | Integração com Ômega | Conexão com outros módulos CoordIA |

---

## Próximos passos recomendados

1. **Definir fonte de dados real** — Qual sistema escolar será integrado?
2. **Criar interface mínima de decisão** — Pode ser CLI ou web simples
3. **Configurar proteção de branch** — Manual no GitHub
4. **Testar com dados reais anonimizados** — Validar fluxo completo

---

## O que já está pronto

- Núcleo advisory com proveniência
- Detectores (base + extras + plugins)
- Priorização dinâmica
- Orquestrador e colônia (modo Goku)
- API HTTP
- Monitoramento e alertas de falha
- Cache, validação, observabilidade
- Testes e CI
- Documentação completa

---

## Estimativa

| Prioridade | Itens | Esforço total |
|------------|-------|---------------|
| P0 | 4 | 2-4 semanas |
| P1 | 5 | 1-2 semanas |
| P2 | 5 | 2-4 semanas |
| P3 | 3 | Futuro |

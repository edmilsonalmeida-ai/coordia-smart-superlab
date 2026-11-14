# Câmara Extra — Execução técnica e contraprovas P0
**Data:** 14/11/2026  
**Escopo:** somente o repositório `coordia-smart-superlab`, branch LAB.  
**Base congelada:** `main@45b5654429023cdad2b9ef602e37658957ee9f96`.  
**Remessa:** [issue #2](https://github.com/edmilsonalmeida-ai/coordia-smart-superlab/issues/2) · [PR draft #3](https://github.com/edmilsonalmeida-ai/coordia-smart-superlab/pull/3).

## Execução verificável
- [Run de CI #43601868378](https://github.com/edmilsonalmeida-ai/coordia-smart-superlab/actions/runs/43601868378): três jobs PASS, Python 3.11, 3.12 e verificação declarativa das flags; cinco grupos de contraprovas no primeiro ciclo.
- [Run de CI #43602245249](https://github.com/edmilsonalmeida-ai/coordia-smart-superlab/actions/runs/43602245249): três jobs PASS, com sete grupos de contraprovas e guardas adicionais para a integração.
- [Run de CI #43602829545](https://github.com/edmilsonalmeida-ai/coordia-smart-superlab/actions/runs/43602829545): três jobs PASS; acrescenta teste HTTP ponta a ponta **local** de token ausente/inválido, origem declarada, recusa de campos pessoais, decisão válida, índice negativo e repetição.
- O código submetido **não** foi mesclado à main. Nenhum deploy, consumo de API de agente externo, acesso ao Ômega ou escrita escolar foi executado nesta revisão.

## Matriz FATO / PROVA / LACUNA / RISCO / RETESTE / DECISÃO

### P0-01 Auditor pode reprovar sem impedir encaminhamento
- **FATO original:** `OrquestradorAgentes.executar_fluxo` sempre invocava `AgenteDecisor`, independentemente de `aud["ok"]`.
- **PROVA:** `orquestrador_agentes.py` da base e diff da PR #3; contraprova `test_orquestrador_bloqueia_falha_e_nao_chama_decisor`.
- **CORREÇÃO:** resultado `bloqueado=true`, `top=[]`, `pendentes_decisao=0`, sem chamada do Decisor. `FluxoCoordIA` passou a rejeitar parecer de auditoria negativo.
- **LACUNA:** esta auditoria valida invariantes estruturais; a origem declarada não é autenticada por fonte institucional.
- **RISCO residual:** proveniência falsificável sem conector atestado.
- **RETESTE:** CI nos dois Pythons, contraprovas de bloqueio e de `alerta_erro`.
- **DECISÃO:** PASS LAB na regra de bloqueio; NÃO homologar dados reais.

### P0-02 API local não autenticava decisões
- **FATO original:** `POST /decidir` aceitava pedido sem token, com fallback `responsavel="sistema"`.
- **PROVA:** `integracao/api_integracao.py` da base e diff da PR #3; `test_api_falha_fechado_sem_token`.
- **CORREÇÃO:** ambas as rotas POST exigem Bearer `COORDIA_API_TOKEN` (sem token ou token curto => 503; token inválido => 401), com limite de corpo e validação de esquema básica. O endpoint não aceita origem distinta de `sintetico` declarada; o contrato também rejeita chaves fora da allowlist e identificadores de aluno que não usem prefixo sintético.
- **LACUNA:** token de serviço não autentica a identidade individual do coordenador; a string de origem `sintetico` pode ser autodeclarada. O teste HTTP ponta a ponta em servidor local foi executado no CI, mas não comprova IAM institucional, conectividade escolar ou proteção completa de PII.
- **RISCO residual:** identidade humana, controle granular e proteção de PII não homologados.
- **RETESTE:** testes de método + HTTP local com autorização, esquema estrito, payload PII rejeitado e resposta de decisão.
- **DECISÃO:** PASS LAB na guarda testada; API institucional NO-GO.

### P0-03 Decisão humana sem persistência e com repetição possível
- **FATO original:** `FluxoCoordIA.decidir` criava objeto de decisão em memória e persistia apenas feedback. Aceitava índices negativos.
- **PROVA:** `integracao/fluxo_completo.py` e `test_decisao_humana_validada_registrada_uma_vez`.
- **CORREÇÃO:** valida índice, estado, decisão e responsável explícito; registra `decisoes.jsonl` e bloqueia segunda decisão sobre mesmo índice durante a instância.
- **LACUNA:** log JSONL não é transacional nem imutável; índices locais não substituem IDs estáveis; idempotência pós-reinício não foi testada.
- **RETESTE:** cenários sintéticos de índice negativo, repetido, decisão inválida, responsável ausente e leitura do log.
- **DECISÃO:** PASS LAB limitado à instância corrente; registro institucional NO-GO.

### P0-04 Flags e CI contraditórios
- **FATO original:** `config.py` declara `OPERATIONAL_GO=True`, `MODO_SINTETICO=False`, `WRITE_ESCOLAR="CONTROLADO"`, mas o job `flags-only` da main exigia `False / NO_GO`.
- **PROVA:** `config.py` e `.github/workflows/ci.yml` da base.
- **CORREÇÃO:** teste de CI agora verifica coerência das declarações sem afirmar que são portões institucionais.
- **LACUNA:** `assert_safe_mode` ainda não comprova autorização operacional, conexão atestada, IAM, segregação nem escrita controlada.
- **RISCO residual:** a configuração pode induzir falsa confiança. **Não alterar as flags nem tomar seu valor por concessão de acesso.**
- **DECISÃO:** PASS LAB para consistência de teste; NO-GO para afirmar homologação real.

### P0-05 Fonte presumida e exceção adversarial ocultada
- **FATO original:** conector completava `fonte` ausente com nome do modo; testes adversariais absorviam qualquer exceção.
- **CORREÇÃO:** fonte deve ser explicitamente declarada (não automaticamente tratada como prova); teste adversarial falha diante de exceções inesperadas.
- **PROVA/RETESTE:** `test_conector_nao_inventa_fonte`, `tests/test_adversarial_planejamento.py` e CI.
- **LACUNA:** declaração de fonte não autentica sua procedência.
- **DECISÃO:** PASS LAB quanto à ausência de preenchimento automático.

## Sete propostas GPT → CoordIA SMART: decisão por prioridade
| Proposta | Tratamento técnico | Prioridade |
|---|---|---|
| 1. GPT orquestrador de alto nível | Interpretar pedidos, mostrar plano e chamar somente ações explicitamente permitidas; recibo por operação | P1 |
| 2. GPT gerador de detectores | Propor patch em branch LAB com validação de schema, suites adversariais e aprovação humana antes de ativar | P1 |
| 3. GPT analista de feedback | Recomendar mudanças de pesos sem alterá-los automaticamente; análise de falso positivo e viés | P1 |
| 4. GPT redator de comunicação | Minutas sem envio e sem inferir faltas ou confirmar ocorrências não comprovadas | P1 |
| 5. GPT planejador de missões | Plano declarativo, orçamento e limites; nenhuma execução com credenciais por simples linguagem natural | P2 |
| 6. GPT auditor contínuo | Revisão de logs com correlação commit/run/recibo e alerta de divergências; independente do executor | P1 |
| 7. Integração multiagente | Comprovar identidade de provedor, papéis, chamadas, custos e resultados divergentes; não confundir quatro classes locais com quatro agentes LLM | P0 antes de alegar autonomia externa |

## Limites e decisão provisória
**Revisão técnica do proponente:** `PASS_LAB_P0_LIMITADO` para as contraprovas automatizadas do PR #3. **Revisão independente de outro executor/agente: PENDENTE.** Não é parecer de revisor externo, nem auto-homologação, nem autorização escolar. A Câmara Extra pode rejeitar ou solicitar retestes com base nas provas.

**Operação institucional:** `NO_GO_SEM_PROVA`. Isso não modifica flags do projeto nem o estado de outros repositórios CoordIA.

## Próximos testes técnicos concretos
1. Expandir o HTTP local já aprovado para reinício, concorrência, JSON adversarial e fuzzing; posteriormente validar IAM institucional em ambiente autorizado e isolado.
2. Proveniência vinculada a fonte autorizada e normalização de schemas, sem consultar dados reais.
3. Ledger com integridade verificável e idempotência após reinício; tratar identificadores conforme LGPD.
4. Contraprova por executor/agente distinto, com commit HEAD, run, custo (se houver), divergência e decisão por escopo, sem assinatura externa obrigatória.
5. Simular falhas de dependência, replay, custo e interrupção, mantendo o decisor humano separado.

**Critério de fechamento:** evidências atribuíveis e reproduzíveis para o escopo declarado; não declarar homologação apenas porque CI passou.

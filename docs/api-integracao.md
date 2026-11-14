# API de Integração

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/status` | Status do conector e pendentes |
| POST | `/processar` | Recebe `{"eventos": [...]}` e devolve recomendações |
| POST | `/decidir` | Registra decisão humana |

## Como subir

```bash
python integracao/api_integracao.py
```

## Painel

```bash
python painel_status.py
```

Advisory only. Modo sintético por padrão.

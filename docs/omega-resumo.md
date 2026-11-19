# Resumo — Exploração Ômega Educacional

## Conquistas

| Item | Status |
|------|--------|
| Login automatizado | ✅ |
| Listagem de contas | ✅ |
| API REST mapeada | ✅ |
| IDs de usuário/empresa/ano/grupo | ✅ |
| Conector Selenium | ✅ |
| Conector REST | ✅ |

## Endpoints funcionais

```
POST /login.seam
POST /seam/resource/rest/gusuario/setUsuarioLogado
GET  /seam/resource/rest/gusuario/buscarUsuariosPorCpf/
GET  /seam/resource/rest/selparam/dadosSelecaoParametros
GET  /seam/resource/rest/gusuario/gruposUsuario/
GET  /seam/resource/rest/gperfil/getPerfilLogado/
```

## IDs mapeados

- Usuário: 160010000000023
- Empresa: 1600
- Ano 2026: 160000000002026
- COORDENADOR: 160010000000018

## Pendente

O botão "Aplicar parâmetros" não dispara requisição quando os selects estão vazios. O carregamento das opções nos selects depende de interação AJAX que não foi completamente mapeada.

## Arquivos criados

- `conectores/omega_selenium.py`
- `conectores/omega_rest.py`
- `docs/omega-ajax-map.md`
- `docs/omega-fluxo-completo.md`
- `selenium_utils.py`

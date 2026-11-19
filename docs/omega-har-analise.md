# Análise HAR — Fluxo Completo Ômega

## Fluxo confirmado

1. **Login** → `/login.seam`
2. **Seleção de conta** → `/controleAcessoUsuario.seam?cid=XXXXX`
3. **Home** → `/home.seam?v=v12.12.5`
4. **Relatórios** → `/pages/educacao/relatorios/`
5. **Diário** → `/pages/educacao/relatorios/relEdDiario/relEdDiario.js`

## Endpoints descobertos

| Endpoint | Função |
|----------|--------|
| `/home.seam` | Página principal |
| `/controleAcessoUsuario.seam` | Seleção de conta |
| `/seam/resource/rest/webdesktop/isonline` | Status online |
| `/checkReport/?path=...&file=...` | Verifica PDF gerado |

## Relatório gerado

```
Arquivo: 160010000000023_20261119161941218.pdf
Usuário: 160010000000023
Data: 2026-11-19 16:19:41
```

## Scripts importantes

- `/pages/controleacessousuario/js/controleAcessoUsuario.min.js`
- `/pages/educacao/relatorios/relEdDiario/relEdDiario.js`
- `/view_padrao/dist/js/login.min.js`

## Próximos passos

1. Mapear endpoint de geração de relatório
2. Automatizar download do PDF
3. Integrar com CoordIA SMART

# Fluxo Completo — Ômega Educacional

## Status

| Etapa | Status |
|-------|--------|
| Login | ✅ Funciona |
| Listar contas | ✅ Funciona |
| Set usuário | ✅ Funciona |
| Obter parâmetros | ✅ Funciona |
| Obter grupos | ✅ Funciona |
| Aplicar parâmetros | ⏳ Pendente |
| Acessar relatórios | ⏳ Pendente |

## Fluxo mapeado

### 1. Login
```
POST /login.seam
username=026.245.171-97&password=***&btnLogin=btnLogin
```

### 2. Set usuário
```
POST /seam/resource/rest/gusuario/setUsuarioLogado
Body: 160010000000023
```

### 3. Obter parâmetros
```
GET /seam/resource/rest/selparam/dadosSelecaoParametros?usuarioId=160010000000023
```
Retorna: empresas, anos (2027, 2026, 2025...)

### 4. Obter grupos
```
GET /seam/resource/rest/gusuario/gruposUsuario/?usuario=160010000000023&empresa=1600
```
Retorna: COORDENADOR (160010000000018), PROFESSOR, etc.

## IDs importantes

| Item | ID |
|------|-----|
| Usuário Tia Dejane | 160010000000023 |
| Empresa | 1600 |
| Ano 2026 | 160000000002026 |
| Grupo COORDENADOR | 160010000000018 |

## Pendente

Endpoint para aplicar parâmetros e entrar no sistema. O botão "Aplicar parâmetros" existe na interface mas o endpoint REST não foi identificado.

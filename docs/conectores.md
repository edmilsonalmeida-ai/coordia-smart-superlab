# Conectores

## Cofre de Credenciais

```python
from cofre.credenciais import cofre

# Depositar credenciais
cofre.depositar("omega", "12345678900", "minha_senha", {"url_base": "https://escola.omegaeducacional.com"})

# Listar serviços
print(cofre.listar())
```

## Ômega Educacional

```python
from conectores.omega import omega

# Configurar
omega.configurar(
    url_base="https://sua-escola.omegaeducacional.com",
    usuario="seu_cpf",
    senha="sua_senha"
)

# Conectar
omega.conectar()
print(omega.status())
```

**Nota:** O Ômega não tem API pública documentada. Para conexão real:
1. Verificar com suporte Ômega se existe API
2. Ou usar automação web

## Google Drive

```python
from conectores.drive import drive

drive.configurar()
planilhas = drive.listar_planilhas()
```

## Adicionar novo conector

1. Criar arquivo em `conectores/`
2. Usar `cofre` para credenciais
3. Implementar métodos de acesso

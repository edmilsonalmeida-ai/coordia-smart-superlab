# Aprendizado e Ensino

## Aprendizado

O sistema analisa feedbacks e sugere ajustes de pesos. Não aplica automaticamente.

```python
from aprendizado import Aprendizado

aprend = Aprendizado()
aprend.registrar("pendencia_frequencia", "util")
aprend.registrar("pendencia_frequencia", "nao_util")

print(aprend.analisar())
# Para aplicar: aprend.aplicar_sugestoes("APLICAR")
```

## Ensino

```python
from ensino import ensinar, ensinar_tudo

print(ensinar("advisory"))
print(ensinar_tudo())
```

## Lições

- advisory
- priorizacao
- plugins
- di
- decisao

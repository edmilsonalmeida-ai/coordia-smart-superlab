# Ataque inspirado em FGSM — COORDIA SMART

## Contexto

O sistema atual é **determinístico e baseado em regras** (sem redes neurais ou gradientes).  
FGSM clássico não se aplica diretamente.

## Adaptação implementada

Perturbação de sinal mínimo nas features numéricas:

```
valor_perturbado = valor + epsilon * sinal
```

Onde:
- `epsilon` é pequeno (ex.: 0.02 ou 1)
- `sinal` é +1 ou -1 (direção que tenta cruzar o limiar)

## Objetivo

- Explorar a robustez dos limiares
- Verificar que mesmo perturbações bem-sucedidas geram apenas recomendações advisory
- Manter proveniência e flags de segurança

## Execução

```bash
python tests/test_fgsm_inspirado.py
```

Resultado esperado: alertas continuam com `status: "recomendado"`.

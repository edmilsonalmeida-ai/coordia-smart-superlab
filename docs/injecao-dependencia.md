# Injeção de Dependência

## Conceito

Componentes recebem suas dependências em vez de criá-las internamente.

## Uso básico

```python
from di.container import container

container.registrar("minha_dep", minha_instancia)
container.registrar_fabrica("servico", lambda c: MeuServico(c.resolver("minha_dep")))

servico = container.resolver("servico")
```

## Configuração padrão

```python
from di.configuracao import obter_nucleo

nucleo = obter_nucleo()  # já vem com todos os detectores
```

## Benefícios

- Testabilidade (substitui dependências em testes)
- Flexibilidade (troca implementações sem alterar código)
- Composição clara de componentes

Integrado com a arquitetura de plugins.

"""
Configuração padrão do container de DI.
"""

from di.container import container
from agents.nucleo import Nucleo
from agents.detectores import DETECTORES_PADRAO
from agents.detectores_extras import DETECTORES_EXTRAS
from prototype.alertas_planejamento import detector_planejamento
from plugins.registro import registro
import plugins.detectores_plugin  # auto-registro

def configurar():
    """Configura as dependências padrão."""
    # Detectores base
    container.registrar("detectores_base", DETECTORES_PADRAO)
    container.registrar("detectores_extras", DETECTORES_EXTRAS)
    container.registrar("detector_planejamento", detector_planejamento)

    # Detectores de plugins
    container.registrar("detectores_plugin", registro.obter_detectores())

    # Núcleo como fábrica
    def criar_nucleo(c):
        todos = (
            c.resolver("detectores_base") +
            c.resolver("detectores_extras") +
            [c.resolver("detector_planejamento")] +
            c.resolver("detectores_plugin")
        )
        return Nucleo(todos)

    container.registrar_fabrica("nucleo", criar_nucleo)
    return container

def obter_nucleo() -> Nucleo:
    """Atalho para obter o núcleo configurado."""
    if not container.tem("nucleo"):
        configurar()
    return container.resolver("nucleo")

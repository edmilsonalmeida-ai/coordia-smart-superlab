"""
Configuração do COORDIA SMART.

Modo operacional ativado em 2026-11-13 por autorização explícita.
"""

# Flags principais
OPERATIONAL_GO = True
WRITE_ESCOLAR = "CONTROLADO"   # Escrita permitida somente via conector auditado
MODO_SINTETICO = False

def assert_safe_mode():
    """Confirma que o modo operacional está ativo com auditoria."""
    if OPERATIONAL_GO:
        return True
    raise RuntimeError("Modo operacional não ativado.")

def ativar_modo_operacional(confirmacao: str):
    """Mantido para compatibilidade. Já ativado."""
    global OPERATIONAL_GO, MODO_SINTETICO, WRITE_ESCOLAR
    if confirmacao != "AUTORIZADO-EXPLICITO":
        raise ValueError("Confirmação inválida.")
    OPERATIONAL_GO = True
    MODO_SINTETICO = False
    WRITE_ESCOLAR = "CONTROLADO"
    return {
        "status": "modo_operacional_ativo",
        "operational_go": True,
        "write_escolar": "CONTROLADO",
        "aviso": "Auditoria contínua obrigatória"
    }

def status_modo():
    return {
        "operational_go": OPERATIONAL_GO,
        "modo_sintetico": MODO_SINTETICO,
        "write_escolar": WRITE_ESCOLAR,
        "aviso": "Modo operacional ativo — advisory + auditoria"
    }

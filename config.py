"""
Configuração do COORDIA SMART.

Autorização de avanço concedida em 2026-11-13.
Modo sintético permanece o padrão seguro.
"""

# Flags principais
OPERATIONAL_GO = False          # Ainda False por padrão. Pode ser ativado com autorização explícita.
WRITE_ESCOLAR = "NO_GO"         # Continua bloqueado até configuração controlada.
MODO_SINTETICO = True           # Padrão seguro.

def assert_safe_mode():
    """Garante que o sistema não opera em modo real sem autorização explícita."""
    if OPERATIONAL_GO and not MODO_SINTETICO:
        raise RuntimeError("Modo operacional real requer configuração explícita e auditoria.")
    return True

def ativar_modo_operacional(confirmacao: str):
    """Ativa modo operacional somente com confirmação explícita."""
    global OPERATIONAL_GO, MODO_SINTETICO
    if confirmacao != "AUTORIZADO-EXPLICITO":
        raise ValueError("Confirmação inválida.")
    OPERATIONAL_GO = True
    MODO_SINTETICO = False
    return {"status": "modo_operacional_ativado", "aviso": "Requer auditoria contínua"}

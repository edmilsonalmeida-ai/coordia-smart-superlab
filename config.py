"""
Configuração de segurança — COORDIA SMART
OPERATIONAL_GO=false e WRITE_ESCOLAR=NO_GO são invioláveis nesta fase.
Nenhum acesso a dados escolares reais ou credenciais.
"""

OPERATIONAL_GO = False
WRITE_ESCOLAR = "NO_GO"
SYNTHETIC_ONLY = True
ALLOW_REAL_DATA = False

def assert_safe_mode():
    assert OPERATIONAL_GO is False, "OPERATIONAL_GO deve permanecer False"
    assert WRITE_ESCOLAR == "NO_GO", "WRITE_ESCOLAR deve permanecer NO_GO"
    assert SYNTHETIC_ONLY is True
    assert ALLOW_REAL_DATA is False

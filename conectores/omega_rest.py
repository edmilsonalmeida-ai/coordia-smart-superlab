"""
Conector REST para Ômega Educacional.
Usa os endpoints mapeados.
"""

from typing import Dict, List

class OmegaREST:
    """
    Conector que usa a API REST do Ômega.
    Requer sessão autenticada via Selenium.
    """

    ENDPOINTS = {
        "usuario_logado": "/seam/resource/rest/gusuario/getUsuarioLogado/",
        "perfil_logado": "/seam/resource/rest/gperfil/getPerfilLogado/",
        "buscar_cpf": "/seam/resource/rest/gusuario/buscarUsuariosPorCpf/?cpf=",
        "status_cliente": "/seam/resource/rest/selparam/getstatuscliente/",
        "online": "/seam/resource/rest/webdesktop/isonline",
    }

    def __init__(self, driver=None):
        self.driver = driver

    def set_driver(self, driver):
        self.driver = driver

    def _get(self, endpoint: str) -> Dict:
        if not self.driver:
            return {"erro": "Driver não configurado"}
        result = self.driver.execute_script(f'''
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "{endpoint}", false);
            xhr.send();
            return xhr.responseText;
        ''')
        try:
            import json
            return json.loads(result)
        except:
            return {"raw": result}

    def get_usuario_logado(self) -> Dict:
        return self._get(self.ENDPOINTS["usuario_logado"])

    def get_perfil(self) -> Dict:
        return self._get(self.ENDPOINTS["perfil_logado"])

    def buscar_contas(self, cpf: str) -> List[Dict]:
        result = self._get(f"{self.ENDPOINTS['buscar_cpf']}{cpf}")
        return result.get("dados", [])

    def status(self) -> Dict:
        return self._get(self.ENDPOINTS["status_cliente"])

omega_rest = OmegaREST()

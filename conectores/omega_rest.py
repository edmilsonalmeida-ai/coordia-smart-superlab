"""
Conector REST para Ômega Educacional.
"""

from typing import Dict, List
import json

class OmegaREST:
    ENDPOINTS = {
        "usuario_logado": "/seam/resource/rest/gusuario/getUsuarioLogado/",
        "perfil_logado": "/seam/resource/rest/gperfil/getPerfilLogado/",
        "buscar_cpf": "/seam/resource/rest/gusuario/buscarUsuariosPorCpf/?cpf=",
        "set_usuario": "/seam/resource/rest/gusuario/setUsuarioLogado",
        "dados_parametros": "/seam/resource/rest/selparam/dadosSelecaoParametros?usuarioId=",
        "grupos_usuario": "/seam/resource/rest/gusuario/gruposUsuario/?usuario=",
        "status": "/seam/resource/rest/selparam/getstatuscliente/",
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
            return json.loads(result)
        except:
            return {"raw": result}

    def _post(self, endpoint: str, data: str) -> Dict:
        if not self.driver:
            return {"erro": "Driver não configurado"}
        result = self.driver.execute_script(f'''
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "{endpoint}", false);
            xhr.send("{data}");
            return xhr.responseText;
        ''')
        try:
            return json.loads(result)
        except:
            return {"raw": result}

    def get_perfil(self) -> Dict:
        return self._get(self.ENDPOINTS["perfil_logado"])

    def buscar_contas(self, cpf: str) -> List[Dict]:
        result = self._get(f"{self.ENDPOINTS['buscar_cpf']}{cpf}")
        return result.get("dados", []) if isinstance(result, dict) else []

    def set_usuario(self, usuario_id: str) -> Dict:
        return self._post(self.ENDPOINTS["set_usuario"], usuario_id)

    def get_parametros(self, usuario_id: str) -> Dict:
        return self._get(f"{self.ENDPOINTS['dados_parametros']}{usuario_id}")

    def get_grupos(self, usuario_id: str, empresa_id: str) -> List[Dict]:
        return self._get(f"{self.ENDPOINTS['grupos_usuario']}{usuario_id}&empresa={empresa_id}")

omega_rest = OmegaREST()

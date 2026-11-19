"""
Conector completo Ômega Educacional.
Fluxo: login → seleção → home → relatórios
"""

from typing import Dict, List, Optional
import json

class OmegaCompleto:
    BASE_URL = "https://pdl.mt.ed.omegaeducacional.com"

    ENDPOINTS = {
        "login": "/login.seam",
        "controle_acesso": "/controleAcessoUsuario.seam",
        "home": "/home.seam",
        "isonline": "/seam/resource/rest/webdesktop/isonline",
        "set_usuario": "/seam/resource/rest/gusuario/setUsuarioLogado",
        "usuario_logado": "/seam/resource/rest/gusuario/getUsuarioLogado/",
        "perfil": "/seam/resource/rest/gperfil/getPerfilLogado/",
        "buscar_cpf": "/seam/resource/rest/gusuario/buscarUsuariosPorCpf/?cpf=",
        "parametros": "/seam/resource/rest/selparam/dadosSelecaoParametros?usuarioId=",
        "grupos": "/seam/resource/rest/gusuario/gruposUsuario/?usuario=",
        "check_report": "https://omegaeducacional.com/checkReport/",
        "diario": "/pages/educacao/relatorios/relEdDiario/",
    }

    IDS = {
        "usuario_tia_dejane": "160010000000023",
        "empresa": "1600",
        "ano_2026": "160000000002026",
        "coordenador": "160010000000018",
    }

    def __init__(self, driver=None):
        self.driver = driver
        self.logado = False
        self.usuario_id = None

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
            return {"raw": result[:200] if result else ""}

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
            return {"raw": result[:200] if result else ""}

    def login(self, cpf: str, senha: str) -> Dict:
        """Faz login no sistema."""
        if not self.driver:
            return {"erro": "Driver não configurado"}

        self.driver.get(f"{self.BASE_URL}/login.seam")
        import time
        time.sleep(2)

        self.driver.execute_script(f'''
            document.getElementById("username").value = "{cpf}";
            document.getElementById("password").value = "{senha}";
            document.getElementById("btnLogin").click();
        ''')
        time.sleep(5)

        if "controleAcesso" in self.driver.current_url:
            self.logado = True
            return {"status": "logado", "url": self.driver.current_url}
        return {"status": "falhou", "url": self.driver.current_url}

    def set_usuario(self, usuario_id: str = None) -> Dict:
        """Define o usuário ativo."""
        uid = usuario_id or self.IDS["usuario_tia_dejane"]
        result = self._post(self.ENDPOINTS["set_usuario"], uid)
        if result.get("error") == False:
            self.usuario_id = uid
        return result

    def get_contas(self, cpf: str) -> List[Dict]:
        """Lista contas do CPF."""
        result = self._get(f"{self.ENDPOINTS['buscar_cpf']}{cpf}")
        return result.get("dados", []) if isinstance(result, dict) else []

    def get_parametros(self, usuario_id: str = None) -> Dict:
        """Obtém parâmetros de seleção."""
        uid = usuario_id or self.usuario_id or self.IDS["usuario_tia_dejane"]
        return self._get(f"{self.ENDPOINTS['parametros']}{uid}")

    def get_grupos(self, usuario_id: str = None, empresa_id: str = None) -> List:
        """Obtém grupos/perfis do usuário."""
        uid = usuario_id or self.usuario_id or self.IDS["usuario_tia_dejane"]
        emp = empresa_id or self.IDS["empresa"]
        return self._get(f"{self.ENDPOINTS['grupos']}{uid}&empresa={emp}")

    def ir_home(self) -> Dict:
        """Navega para a home."""
        if not self.driver:
            return {"erro": "Driver não configurado"}
        self.driver.get(f"{self.BASE_URL}/home.seam?v=v12.12.5")
        import time
        time.sleep(3)
        return {"url": self.driver.current_url, "titulo": self.driver.title}

    def status(self) -> Dict:
        return {
            "logado": self.logado,
            "usuario_id": self.usuario_id,
            "url": self.driver.current_url if self.driver else None
        }

omega = OmegaCompleto()

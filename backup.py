#!/usr/bin/env python3
"""
Backup automático do CoordIA SMART.
"""

import shutil
from datetime import datetime
from pathlib import Path

ARQUIVOS_BACKUP = [
    "auditoria.jsonl",
    "decisoes.jsonl",
    "feedback.jsonl",
    "logs_estruturados.jsonl",
    "notificacoes.jsonl",
    "processados.json",
    "historico_missoes.jsonl",
]

def criar_backup(destino: str = None) -> str:
    """Cria backup dos arquivos de dados."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta = Path(destino or f"backup_{timestamp}")
    pasta.mkdir(exist_ok=True)

    copiados = []
    for arquivo in ARQUIVOS_BACKUP:
        origem = Path(arquivo)
        if origem.exists():
            shutil.copy(origem, pasta / arquivo)
            copiados.append(arquivo)

    return str(pasta)

def listar_backups() -> list:
    """Lista backups existentes."""
    return [p.name for p in Path(".").glob("backup_*") if p.is_dir()]

if __name__ == "__main__":
    pasta = criar_backup()
    print(f"Backup criado: {pasta}")

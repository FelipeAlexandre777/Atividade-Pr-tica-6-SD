"""Implementação didática de blocos encadeados por SHA-256.

Este laboratório não implementa uma blockchain de produção nem consenso real.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from typing import Iterable


@dataclass
class Bloco:
    indice: int
    dados: str
    hash_anterior: str
    hash: str = ""

    def calcular_hash(self) -> str:
        base = {
            "indice": self.indice,
            "dados": self.dados,
            "hash_anterior": self.hash_anterior,
        }
        serializado = json.dumps(
            base, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(serializado).hexdigest()


def criar_bloco(indice: int, dados: str, hash_anterior: str) -> Bloco:
    bloco = Bloco(indice=indice, dados=dados, hash_anterior=hash_anterior)
    bloco.hash = bloco.calcular_hash()
    return bloco


def criar_cadeia(dados: Iterable[str]) -> list[Bloco]:
    cadeia = [criar_bloco(0, "genesis", "0" * 64)]
    for dado in dados:
        cadeia.append(criar_bloco(len(cadeia), dado, cadeia[-1].hash))
    return cadeia


def validar_cadeia(cadeia: list[Bloco]) -> tuple[bool, str]:
    if not cadeia:
        return False, "cadeia vazia"
    if cadeia[0].indice != 0 or cadeia[0].dados != "genesis":
        return False, "bloco gênesis inválido"
    if cadeia[0].hash_anterior != "0" * 64:
        return False, "referência anterior do gênesis inválida"

    for i, bloco in enumerate(cadeia):
        if bloco.indice != i:
            return False, f"índice inválido no bloco {i}"
        if bloco.hash != bloco.calcular_hash():
            return False, f"hash inválido no bloco {i}"
        if i > 0 and bloco.hash_anterior != cadeia[i - 1].hash:
            return False, f"ligação inválida no bloco {i}"
    return True, "cadeia válida"


def recalcular_a_partir(cadeia: list[Bloco], indice: int) -> None:
    """Recalcula o hash do bloco adulterado e dos seguintes."""
    for i in range(indice, len(cadeia)):
        if i > 0:
            cadeia[i].hash_anterior = cadeia[i - 1].hash
        cadeia[i].hash = cadeia[i].calcular_hash()

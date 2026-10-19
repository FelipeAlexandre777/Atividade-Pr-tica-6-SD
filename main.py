from __future__ import annotations
import csv
import hashlib
import json
import random
from pathlib import Path
from src.blockchain import criar_cadeia, validar_cadeia, recalcular_a_partir

ROOT = Path(__file__).resolve().parent
EVIDENCIAS = ROOT / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)


def gravar_csv(nome, cabecalho, linhas):
    with (EVIDENCIAS / nome).open("w", newline="", encoding="utf-8-sig") as arquivo:
        writer = csv.writer(arquivo, delimiter=";")
        writer.writerow(cabecalho)
        writer.writerows(linhas)


def main():
    rng = random.Random(20261019)  # semente fixa para reproduzir o experimento
    dados = [
        f"transacao-{i:02d}: origem=usuario{rng.randint(1, 8)};"
        f" destino=usuario{rng.randint(9, 16)}; valor={rng.randint(1, 500)}"
        for i in range(1, 25)
    ]
    cadeia = criar_cadeia(dados)
    ok, mensagem = validar_cadeia(cadeia)
    assert ok and len(cadeia) >= 20

    linhas_hash = [
        [b.indice, b.dados, b.hash_anterior, b.hash]
        for b in cadeia
    ]
    gravar_csv("hashes_referencia.csv",
               ["indice", "dados", "hash_anterior", "hash"], linhas_hash)

    # Experimento 1: avalanche com mudança de um caractere.
    original = "sensor=temperatura;valor=24.7"
    alterado = "sensor=temperatura;valor=24.8"
    h1 = hashlib.sha256(original.encode("utf-8")).hexdigest()
    h2 = hashlib.sha256(alterado.encode("utf-8")).hexdigest()
    bits_diferentes = sum((int(a, 16) ^ int(b, 16)).bit_count() for a, b in zip(h1, h2))
    bytes_diferentes = sum(a != b for a, b in zip(bytes.fromhex(h1), bytes.fromhex(h2)))

    # Experimento 2: adulteração de bloco intermediário sem recalcular os posteriores.
    adulterada = [type(b)(b.indice, b.dados, b.hash_anterior, b.hash) for b in cadeia]
    indice_adulterado = 7
    hash_original = adulterada[indice_adulterado].hash
    adulterada[indice_adulterado].dados += " [ALTERADO]"
    ok_adulterada, msg_adulterada = validar_cadeia(adulterada)

    # Experimento 3: atacante recalcula os hashes localmente.
    recalcular_a_partir(adulterada, indice_adulterado)
    ok_recalculada, msg_recalculada = validar_cadeia(adulterada)

    # Experimento 4: duas réplicas inicialmente iguais, depois divergentes.
    replica_a = criar_cadeia(dados[:10])
    replica_b = [type(b)(b.indice, b.dados, b.hash_anterior, b.hash) for b in replica_a]
    # A recebe um bloco e B recebe outro no mesmo próximo índice.
    replica_a.append(__import__("src.blockchain", fromlist=["criar_bloco"]).criar_bloco(
        len(replica_a), "transferencia: Ana->Bruno: 15", replica_a[-1].hash))
    replica_b.append(__import__("src.blockchain", fromlist=["criar_bloco"]).criar_bloco(
        len(replica_b), "transferencia: Carla->Diego: 40", replica_b[-1].hash))
    valid_a, msg_a = validar_cadeia(replica_a)
    valid_b, msg_b = validar_cadeia(replica_b)
    divergencia = replica_a[-1].hash != replica_b[-1].hash

    # Regra didática: escolher a cadeia válida mais longa.
    # Neste caso ambas têm mesmo tamanho, portanto a regra não decide.
    if valid_a and valid_b and len(replica_a) > len(replica_b):
        escolha = "A"
    elif valid_a and valid_b and len(replica_b) > len(replica_a):
        escolha = "B"
    elif valid_a and valid_b:
        escolha = "EMPATE: regra não decide"
    elif valid_a:
        escolha = "A"
    elif valid_b:
        escolha = "B"
    else:
        escolha = "NENHUMA: ambas inválidas"

    linhas_exp = [
        ["Cadeia inicial", "24 blocos + gênesis", "válida", msg_ok(ok, mensagem)],
        ["Avalanche SHA-256", "um caractere alterado", "hash diferente", f"{bits_diferentes}/256 bits diferentes; {bytes_diferentes}/32 bytes diferentes"],
        ["Adulteração intermediária", f"bloco {indice_adulterado}", "detectar alteração", f"{msg_adulterada}; hash antigo={hash_original[:16]}..."],
        ["Recalcular hashes posteriores", f"bloco {indice_adulterado} até o fim", "avaliar limite", f"{msg_recalculada}; válida localmente={ok_recalculada}"],
        ["Réplicas divergentes", "mesmo índice, dados distintos", "identificar fork", f"A={msg_a}; B={msg_b}; hashes diferentes={divergencia}"],
        ["Reconciliação simples", "cadeia válida mais longa", "selecionar réplica", escolha],
    ]
    gravar_csv("resultados_experimentos.csv",
               ["experimento", "procedimento", "objetivo", "resultado_observado"], linhas_exp)

    log = [
        "AP6 - Blockchain didática: execução dos experimentos",
        "=" * 58,
        f"Cadeia principal: {len(cadeia)} blocos (incluindo gênesis). Validação: {mensagem}.",
        f"SHA-256 original:  {h1}",
        f"SHA-256 alterado:  {h2}",
        f"Bits diferentes: {bits_diferentes}/256; bytes diferentes: {bytes_diferentes}/32.",
        f"Adulteração sem recálculo: {msg_adulterada}.",
        f"Após recálculo local: {msg_recalculada}.",
        f"Réplica A válida: {valid_a} ({msg_a}); tamanho={len(replica_a)}.",
        f"Réplica B válida: {valid_b} ({msg_b}); tamanho={len(replica_b)}.",
        f"Hashes finais divergentes: {divergencia}.",
        f"Regra de reconciliação (cadeia válida mais longa): {escolha}.",
        "",
        "Interpretação: o hash detecta alteração quando os hashes armazenados não são atualizados.",
        "Recalcular localmente todos os hashes pode tornar a cópia adulterada internamente consistente.",
        "Isso não prova que os dados são verdadeiros; consenso exige regras distribuídas de escolha e validação.",
    ]
    (EVIDENCIAS / "execucao.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))
    print(f"\nArquivos de evidência salvos em: {EVIDENCIAS}")


def msg_ok(ok, mensagem):
    return mensagem if ok else f"FALHA: {mensagem}"


if __name__ == "__main__":
    main()

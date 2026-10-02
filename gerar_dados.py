# -*- coding: utf-8 -*-
"""Gera dados.json do Manager DO-BR a partir do dataset do Fenômeno DO-BR.

Uso: python gerar_dados.py   (lê ../FenomenoDOBR, escreve dados.json nesta pasta)
"""
import csv, io, json, os, re, unicodedata

FONTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "FenomenoDOBR")

ATRIBUTOS = ["Reflexes", "One on ones", "Handling", "Communication", "Positioning",
             "Tackling", "Marking", "Heading", "Crossing", "Creativity", "Passing",
             "First touch", "Long shots", "Shooting", "Dribbling", "Speed", "Strength",
             "Team work", "Aggression", "Influence", "Eccentricity"]

# mesmas fórmulas de OPS do Copa 7a0 (extract_players.py): 5 atributos por posição
OPS = {
    "GOL": ["Reflexes", "One on ones", "Handling", "Communication", "Positioning"],
    "ZAG": ["Tackling", "Marking", "Positioning", "Communication", "Heading"],
    "LAT": ["Tackling", "Marking", "Positioning", "Communication", "Crossing"],
    "MC":  ["Creativity", "Passing", "First touch", "Positioning", "Long shots"],
    "ML":  ["Creativity", "Passing", "First touch", "Positioning", "Crossing"],
    "ATA": ["First touch", "Positioning", "Shooting", "Dribbling", "Heading"],
}
POS_DUGOUT = {"GK": "GOL", "DC": "ZAG", "Lateral": "LAT", "MC": "MC", "Meia-Lateral": "ML", "FC": "ATA"}
PENALIDADE_COMPETENT = 3


# presidentes = managers reais de cada clube no Dugout (presidentes.csv, exportado pelo usuário)
APELIDOS = {"borussiamontecheidegado": "borussiamontecheiodegado"}


def chave(nome):
    nome = re.sub(r"\s*\([^)]*\)\s*$", "", nome.strip())
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    nome = re.sub(r"[^a-z0-9]", "", nome)
    return APELIDOS.get(nome, nome)


def ler_presidentes():
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presidentes.csv")
    if not os.path.exists(caminho):
        return {}
    with io.open(caminho, encoding="utf-8-sig") as f:
        return {chave(r["nomeClube"]): r["nomeManager"].strip() for r in csv.DictReader(f, delimiter=";")}


def ovr_de_ops(ops):
    return max(25, min(99, round(50 + (ops - 150) * 0.47)))


def ler(nome):
    with io.open(os.path.join(FONTE, nome), encoding="utf-8-sig") as f:
        return json.load(f)


def main():
    completo = ler("dados_fenomeno_completo.json")
    idade = {j["id"]: j["idade"] for j in ler("dados_fenomeno_raridade.json")["jogadores"]}
    info = {c["id_time"]: c for c in ler("clubes_info.json")}

    presidentes = ler_presidentes()
    clubes = []
    for t in completo["times"]:
        nome_div = t["divisao"].split(" - ")[1]
        div = "CB" if nome_div.startswith("Campeonato") else nome_div.split()[-1]
        c = info.get(t["id"], {})
        clubes.append({
            "id": t["id"], "n": t["nome"], "c": c.get("nome_curto") or t["nome"], "div": div,
            "est": c.get("estadio_nome") or "Estádio Municipal",
            "cap": int(c.get("estadio_capacidade_atual") or 20000),
            "pres": presidentes.get(chave(t["nome"])),
        })

    jogadores = []
    for j in completo["jogadores"]:
        pos = {}
        for nome_pos, nivel in j["posicoes"].items():
            p = POS_DUGOUT[nome_pos]
            o = ovr_de_ops(sum(j["atributos"].get(a, 0) for a in OPS[p]))
            pos[p] = o - (0 if nivel == "Natural" else PENALIDADE_COMPETENT)
        jogadores.append({
            "id": j["id"], "n": j["nome"], "t": j["idTime"], "a": idade.get(j["id"], 27),
            "nat": j.get("pais") or "BRA", "pos": pos,
            "at": [j["atributos"].get(a, 0) for a in ATRIBUTOS],
        })

    saida = {"atributos": ATRIBUTOS, "clubes": clubes, "jogadores": jogadores}
    with io.open("dados.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, separators=(",", ":"))
    print(len(clubes), "clubes,", len(jogadores), "jogadores,", sum(1 for c in clubes if c["pres"]), "presidentes ->", os.path.getsize("dados.json") // 1024, "KB")


if __name__ == "__main__":
    main()

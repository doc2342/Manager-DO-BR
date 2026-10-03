# -*- coding: utf-8 -*-
"""Gera dados.json do Manager DO-BR a partir do dataset do Fenômeno DO-BR.

Uso: python gerar_dados.py   (lê ../FenomenoDOBR, escreve dados.json nesta pasta)
"""
import csv, io, json, os, re, unicodedata

from paises import PAISES, pais_pt

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


# posições da página de elenco do Dugout -> posições do jogo
POS_ELENCO = {"GK": "GOL", "DC": "ZAG", "DL": "LAT", "DR": "LAT", "MC": "MC", "ML": "ML", "MR": "ML", "FC": "ATA", "FL": "ATA", "FR": "ATA"}
VAGAS_RESERVA = [("GOL", 1), ("ZAG", 2), ("LAT", 2), ("MC", 2), ("ML", 2), ("ATA", 2)]  # uma "segunda escalação" num 4-4-2
IDADE_MAX_PROMESSA = 18


def ovr_na_posicao(at, pos):
    return ovr_de_ops(sum(at.get(a, 0) for a in OPS[pos]))


def jogador_do_elenco(j, cid):
    pos = POS_ELENCO[j["pos"]]
    return {"id": j["id"], "n": j["n"], "t": cid, "a": j["a"], "nat": pais_pt(j["nat"]), "pos": {pos: ovr_na_posicao(j["at"], pos)},
            "at": [j["at"].get(a, 0) for a in ATRIBUTOS]}


PARTICULAS = {"da", "de", "do", "dos", "das", "di", "van", "von", "der", "den", "del", "la", "le", "dal", "dos"}
MIN_JOGADORES_PAIS = 12  # países com menos gente que isso não têm nome suficiente pra misturar


def separar_nome(nome):
    """'Ailton da Guia' -> ('Ailton', 'da Guia'); 'C.Machado' -> (None, 'Machado')."""
    nome = nome.strip()
    if " " not in nome:
        partes = [p for p in re.split(r"\.", nome) if p]
        return None, (partes[-1] if partes and len(partes[-1]) >= 3 else None)
    partes = nome.split()
    primeiro = partes[0] if len(partes[0]) >= 3 and "." not in partes[0] else None
    sobrenome = partes[-1]
    if len(partes) >= 3 and partes[-2].lower() in PARTICULAS:
        sobrenome = partes[-2].lower() + " " + partes[-1]
    return primeiro, (sobrenome if len(partes[-1]) >= 3 else None)


def nomes_por_pais(elencos):
    """Bases de nomes separadas: brasileiros (base, gerados) e cada país estrangeiro (mercado internacional)."""
    por_pais = {}
    for js in elencos.values():
        for j in js:
            pais = pais_pt(j["nat"])
            p, s = separar_nome(j["n"])
            d = por_pais.setdefault(pais, {"p": set(), "s": set(), "n": 0})
            d["n"] += 1
            if p:
                d["p"].add(p)
            if s:
                d["s"].add(s)
    saida = {}
    for pais, d in por_pais.items():
        # "Ademirda" (de "Ademir da Silva" escrito junto): descarta se sem o "da/de/do" vira outro nome existente
        d["p"] = {p for p in d["p"] if not (p[-2:] in ("da", "de", "do") and p[:-2] in d["p"])}
        if d["n"] >= MIN_JOGADORES_PAIS and len(d["p"]) >= 5 and len(d["s"]) >= 5:
            saida[pais] = {"p": sorted(d["p"]), "s": sorted(d["s"]), "peso": d["n"]}
    return saida


def iso_da_bandeira(b):
    """🇱🇹 -> 'lt' (pros arquivos de bandeira); Inglaterra/Escócia usam os códigos gb-eng/gb-sct."""
    if "󠁥" in b:
        return "gb-eng"
    if "󠁳" in b:
        return "gb-sct"
    return "".join(chr(ord(ch) - 0x1F1E6 + ord("a")) for ch in b if 0x1F1E6 <= ord(ch) <= 0x1F1FF)


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
            "nat": pais_pt(j.get("pais") or "BRA"), "pos": pos,
            "at": [j["atributos"].get(a, 0) for a in ATRIBUTOS],
        })

    # reservas e promessas reais (elencos_completos.json, gerado por extrair_elencos.py)
    reservas, promessas, nomes = [], [], {}
    caminho_el = os.path.join(os.path.dirname(os.path.abspath(__file__)), "elencos_completos.json")
    if os.path.exists(caminho_el):
        with io.open(caminho_el, encoding="utf-8") as f:
            elencos = json.load(f)
        usados = {j["id"] for j in jogadores}
        for c in clubes:
            resto = [j for j in elencos.get(c["id"], []) if j["id"] not in usados and j["pos"] in POS_ELENCO]
            adultos = [j for j in resto if j["a"] > IDADE_MAX_PROMESSA]
            jovens = [j for j in resto if j["a"] <= IDADE_MAX_PROMESSA]
            ops = lambda j, pos: sum(j["at"].get(x, 0) for x in OPS[pos])
            faltam = 0
            for pos, n in VAGAS_RESERVA:
                cand = sorted([j for j in adultos if POS_ELENCO[j["pos"]] == pos], key=lambda j: -ops(j, pos))[:n]
                # vaga sem adulto da posição: completa com o melhor garoto da base daquela posição
                cand += sorted([j for j in jovens if POS_ELENCO[j["pos"]] == pos], key=lambda j: -ops(j, pos))[:n - len(cand)]
                faltam += n - len(cand)
                for j in cand:
                    (adultos if j in adultos else jovens).remove(j); usados.add(j["id"]); reservas.append(jogador_do_elenco(j, c["id"]))
            # ainda faltando: o melhor garoto da base de qualquer posição
            for j in sorted(jovens, key=lambda j: -ops(j, POS_ELENCO[j["pos"]]))[:faltam]:
                jovens.remove(j); usados.add(j["id"]); reservas.append(jogador_do_elenco(j, c["id"]))
            for j in resto:
                if j["a"] <= IDADE_MAX_PROMESSA and j["id"] not in usados:
                    usados.add(j["id"]); pr = jogador_do_elenco(j, c["id"])
                    pr["ops"] = sum(j["at"].get(x, 0) for x in OPS[next(iter(pr["pos"]))])  # bruto: o jogo compara com outros da mesma idade
                    promessas.append(pr)
        nomes = nomes_por_pais(elencos)

    saida = {"atributos": ATRIBUTOS, "clubes": clubes, "jogadores": jogadores, "reservas": reservas,
             "promessas": promessas, "nomes": nomes, "bandeiras": {pt: b for pt, b in PAISES.values()}, "iso": {pt: iso_da_bandeira(b) for pt, b in PAISES.values()}}
    with io.open("dados.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, separators=(",", ":"))
    br = nomes.get("Brasil", {"p": [], "s": []})
    print(len(reservas), "reservas,", len(promessas), "promessas; nomes BR:", len(br["p"]), "x", len(br["s"]), "; países estrangeiros com nomes:", len(nomes) - 1)
    print(len(clubes), "clubes,", len(jogadores), "jogadores,", sum(1 for c in clubes if c["pres"]), "presidentes ->", os.path.getsize("dados.json") // 1024, "KB")


if __name__ == "__main__":
    main()

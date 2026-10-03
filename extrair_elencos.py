# -*- coding: utf-8 -*-
"""Extrai os elencos completos do Dugout (páginas salvas em ../FenomenoDOBR/elencos_html).

Saída: elencos_completos.json  ->  {club_id: [{id, n, a, nat, pos, at:{...}}]}
Uso:   python extrair_elencos.py
"""
import glob, html, io, json, os, re

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "FenomenoDOBR", "elencos_html")
ABREV = {"Ref": "Reflexes", "Tck": "Tackling", "Cre": "Creativity", "Sht": "Shooting", "Tmw": "Team work",
         "One": "One on ones", "Mrk": "Marking", "Pas": "Passing", "Dri": "Dribbling", "Sp": "Speed",
         "Hnd": "Handling", "Hea": "Heading", "Lsh": "Long shots", "Psn": "Positioning", "Str": "Strength",
         "Com": "Communication", "Crs": "Crossing", "Fto": "First touch", "Agg": "Aggression",
         "Inf": "Influence", "Ecc": "Eccentricity"}

RE_LINHA = re.compile(r'<div class="\w+_icon">([A-Z]+)</td>(.*?)playerID/(\d+)/club_id/(\d+)">([^<]+)</A>.*?'
                      r'<span class="tableText">(\d+)</span>.*?title="([^"]*)"', re.S)
RE_ATR = re.compile(r'&nbsp;(\w+)</td><td[^>]*><span[^>]*>(\d+)</span>')


def extrair(caminho):
    h = io.open(caminho, encoding="utf-8", errors="ignore").read()
    jogadores = []
    for pos, bloco, pid, cid, nome, idade, pais in RE_LINHA.findall(h):
        at = {ABREV[a]: int(v) for a, v in RE_ATR.findall(bloco) if a in ABREV}
        if len(at) < 21:
            continue
        jogadores.append({"id": pid, "c": cid, "n": html.unescape(nome).strip(), "a": int(idade), "nat": pais, "pos": pos, "at": at})
    return jogadores


def main():
    saida = {}
    for f in sorted(glob.glob(os.path.join(PASTA, "*.html"))):
        js = extrair(f)
        if js:
            saida[os.path.splitext(os.path.basename(f))[0]] = js
    with io.open("elencos_completos.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False)
    print(len(saida), "clubes,", sum(len(v) for v in saida.values()), "jogadores")


if __name__ == "__main__":
    main()

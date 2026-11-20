#!/usr/bin/env python3
"""Lê uma região de um PDF por POSIÇÃO de palavra e salva uma imagem ampliada dela.

Use quando um total da planilha oficial não bate com a soma dos componentes: a extração de tabela
costuma embaralhar rótulo e valor em tabelas com muitas subcélulas.

    python3 pdf_regiao.py planilha_oficial.pdf --pagina 3 --busca "Submódulo 2.3"
    python3 pdf_regiao.py planilha_oficial.pdf --pagina 3 --caixa 30,400,580,560

--busca acha o texto e pega a faixa da página a partir dele (--altura pontos para baixo).
Saída: as linhas reconstruídas pela posição (x, y) e um PNG ampliado da região.
Requer: pip install pdfplumber
"""
import argparse
from collections import defaultdict

import pdfplumber


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--pagina", type=int, required=True, help="número da página (começa em 1)")
    ap.add_argument("--busca", help="texto que marca o início da região")
    ap.add_argument("--altura", type=float, default=160, help="altura da região a partir da busca (pontos)")
    ap.add_argument("--caixa", help="x0,topo,x1,base em pontos (alternativa a --busca)")
    ap.add_argument("--zoom", type=int, default=220, help="resolução da imagem (dpi)")
    ap.add_argument("--saida", default="regiao.png")
    a = ap.parse_args()

    with pdfplumber.open(a.pdf) as pdf:
        page = pdf.pages[a.pagina - 1]
        words = page.extract_words(keep_blank_chars=False, use_text_flow=False, extra_attrs=["size"])
        if a.caixa:
            x0, top, x1, bottom = (float(v) for v in a.caixa.split(","))
        elif a.busca:
            alvo = a.busca.lower().split()
            hit = None
            for i in range(len(words)):
                seq = [w["text"].lower() for w in words[i:i + len(alvo)]]
                if seq == alvo or (len(alvo) == 1 and alvo[0] in words[i]["text"].lower()):
                    hit = words[i]; break
            if not hit:
                raise SystemExit(f"'{a.busca}' não encontrado na página {a.pagina}.")
            x0, top, x1, bottom = 0, max(0, hit["top"] - 6), page.width, min(page.height, hit["top"] + a.altura)
        else:
            x0, top, x1, bottom = 0, 0, page.width, page.height

        region = [w for w in words if w["x0"] >= x0 - 1 and w["x1"] <= x1 + 1 and w["top"] >= top - 1 and w["bottom"] <= bottom + 1]
        lines = defaultdict(list)
        for w in region:
            lines[round(w["top"] / 3)].append(w)
        print(f"Página {a.pagina}, região x {x0:.0f}–{x1:.0f}, y {top:.0f}–{bottom:.0f} ({len(region)} palavras)\n")
        for key in sorted(lines):
            ws = sorted(lines[key], key=lambda w: w["x0"])
            txt = ""
            for w in ws:  # espaçamento proporcional à posição: mostra em que coluna cada valor está
                col = int(w["x0"] / 4.5)
                txt = txt + " " * max(1, col - len(txt)) + w["text"] if txt else " " * col + w["text"]
            print(f"y={ws[0]['top']:6.1f} |{txt}")

        img = page.crop((x0, top, x1, bottom)).to_image(resolution=a.zoom)
        img.save(a.saida)
        print(f"\nImagem ampliada: {a.saida}  (abra e compare com os números acima)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Confere uma planilha de custos (ou Prova Real) antes de entregar.

    python3 conferir_planilha.py "PC - AJUSTADA.xlsx" [--sem-recalculo]

1. Recalcula com o LibreOffice headless (se estiver instalado), para os valores refletirem as fórmulas.
2. Lista erros de fórmula (#REF!, #DIV/0!, #VALUE!, #NAME?, #N/A, #NUM!, #NULL!) em todas as abas.
3. Lista células "A CONFIRMAR" (laranja ou comentário começando assim).
4. Aponta números colados em linhas cujo rótulo indica cálculo (total, subtotal, VT, VA, férias…),
   que deveriam ter fórmula viva.

Zero problemas aqui é necessário, mas não suficiente: depois compare os subtotais com a planilha oficial.
Requer: pip install openpyxl
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openpyxl import load_workbook

ERRORS = ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NUM!", "#NULL!")
ORANGE = {"FFFFA500", "00FFA500", "FFA500"}
CALC = re.compile(r"(?i)\b(total|subtotal|soma|vale[- ]?transporte|\bvt\b|aux[ií]lio[- ]?alimenta|\bva\b|f[ée]rias|13|d[ée]cimo|fgts|"
                  r"encargo|provis[ãa]o|tributo|iss|pis|cofins|lucro|custos? indiretos?|bdi|remunera[çc][ãa]o|montante)")


def recalc(path):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        print("! LibreOffice não encontrado: os valores lidos são os que o Excel salvou da última vez.")
        return path
    out = Path(tempfile.mkdtemp())
    subprocess.run([soffice, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(out), str(path)],
                   capture_output=True, timeout=180)
    res = out / Path(path).with_suffix(".xlsx").name
    if res.exists():
        print(f"✓ recalculado com o LibreOffice")
        return res
    print("! não consegui recalcular com o LibreOffice; seguindo com os valores salvos.")
    return path


def label_of(ws, cell):
    """O texto mais próximo à esquerda na mesma linha: costuma ser o rótulo."""
    for col in range(cell.column - 1, 0, -1):
        v = ws.cell(row=cell.row, column=col).value
        if isinstance(v, str) and v.strip() and not v.startswith("="):
            return v.strip()
    return ""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    src = Path(args[0])
    calc_path = src if "--sem-recalculo" in sys.argv else recalc(src)
    values = load_workbook(calc_path, data_only=True)
    forms = load_workbook(src, data_only=False)

    errors, pending, pasted = [], [], []
    for ws in forms.worksheets:
        wv = values[ws.title] if ws.title in values.sheetnames else None
        for row in ws.iter_rows():
            for c in row:
                v = wv[c.coordinate].value if wv is not None else None
                if isinstance(v, str) and v.strip() in ERRORS:
                    errors.append(f"{ws.title}!{c.coordinate}  {v}  ({label_of(ws, c)[:50]})")
                fill = (c.fill.fgColor.rgb or "") if c.fill and c.fill.fill_type == "solid" else ""
                note = c.comment.text.strip() if c.comment else ""
                if str(fill).upper() in ORANGE or note.upper().startswith("A CONFIRMAR"):
                    pending.append(f"{ws.title}!{c.coordinate}  {label_of(ws, c)[:50]}  → {note[:90] or '(sem comentário)'}")
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool) and c.value not in (0, 1):
                    lab = label_of(ws, c)
                    if lab and CALC.search(lab) and not note:
                        pasted.append(f"{ws.title}!{c.coordinate}  {lab[:50]} = {c.value}")

    def show(title, items, limit=40):
        print(f"\n{title}: {len(items)}")
        for i in items[:limit]:
            print("  ·", i)
        if len(items) > limit:
            print(f"  … e mais {len(items) - limit}")

    show("Erros de fórmula", errors)
    show("Células A CONFIRMAR", pending)
    show("Números colados onde o rótulo sugere cálculo (conferir se deviam ser fórmula)", pasted)
    print("\nLembrete: confira também os subtotais de cada módulo contra a planilha oficial do órgão.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

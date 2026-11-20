#!/usr/bin/env python3
"""Gera a PROVA REAL.xlsx (sobra por posto) já no padrão de formatação obrigatório.

    python3 prova_real.py dados.json "PROVA REAL.xlsx"

Formato do JSON: veja exemplo_prova_real.json. Valores podem ser número ou fórmula de Excel
em texto ("=30*22*(1-0.1)"). Cada campo aceita uma fonte em "fontes" (vira comentário) e
pode ser marcado como estimativa em "estimados" (vira laranja com "A CONFIRMAR").
Requer: pip install openpyxl
"""
import json
import re
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

NAVY, YELLOW, ORANGE, GREY = "FF1F3552", "FFFFFF00", "FFFFA500", "FFF2F2F2"
BRL = '"R$" #,##0.00'
PCT = '0.00%'
thin = Side(style="thin", color="FFBFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD = dict(fill=PatternFill("solid", fgColor=NAVY), font=Font(bold=True, color="FFFFFFFF"),
            alignment=Alignment(horizontal="center", vertical="center", wrap_text=True))

# parâmetros: (chave, rótulo, padrão legal ou None = depende da empresa)
PARAMS = [
    ("ferias", "Férias + 1/3 (% da remuneração)", 1 / 12 * 4 / 3),
    ("decimo", "13º salário (% da remuneração)", 1 / 12),
    ("fgts", "FGTS (% sobre remuneração + férias + 13º)", 0.08),
    ("encargos_patronais", "Encargos patronais (INSS, RAT, terceiros…) %", None),
    ("provisao_rescisao", "Provisão de rescisão (% da remuneração)", None),
    ("tributos_faturamento", "Tributos sobre o faturamento %", None),
    ("iss", "ISS do município %", None),
]
FIELDS = [  # (chave, rótulo, entrada?)
    ("salario", "Salário-base (jornada do cargo)", True),
    ("adicional", "Adicional (insalubridade / periculosidade / noturno)", True),
    ("va", "Auxílio-alimentação (mensal)", True),
    ("vt", "Vale-transporte (mensal, já descontado)", True),
    ("outros", "Outros benefícios (CCT)", True),
    ("valor_posto", "Valor do posto (o que o órgão paga por mês)", True),
    ("qtd", "Quantidade de postos", True),
    ("func_por_posto", "Funcionários por posto (12×36 = 2; 24h = 4…)", True),
]


def sheet_name(s, used):
    s = re.sub(r"[\[\]:*?/\\]", "-", s)[:31] or "Cargo"
    base, n = s, 2
    while s in used:
        s = f"{base[:28]} {n}"; n += 1
    used.add(s)
    return s


def head(ws, row, labels):
    for i, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=t)
        for k, v in HEAD.items():
            setattr(c, k, v)
        c.border = BOX
    ws.row_dimensions[row].height = 32


def put(ws, ref, value, *, fmt=None, fill=None, note=None, bold=False):
    c = ws[ref]
    c.value = value
    c.border = BOX
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = PatternFill("solid", fgColor=fill)
    if note:
        c.comment = Comment(note, "Prova Real", width=320, height=110)
    if bold:
        c.font = Font(bold=True)
    return c


def build(data, out):
    wb = Workbook()
    resumo = wb.active
    resumo.title = "RESUMO"
    used = {"RESUMO", "OBSERVAÇÕES"}
    fontes_p = data.get("fontes_parametros", {})
    params = data.get("parametros", {})
    P = {}

    # ----- parâmetros (editáveis; tudo referencia estes nomes) -----
    resumo["A1"] = f"PROVA REAL · {data.get('licitacao', '')}".strip(" ·")
    resumo["A1"].font = Font(bold=True, size=14)
    head(resumo, 3, ["Parâmetro", "Valor", "Fonte"])
    r = 4
    for key, label, default in PARAMS:
        v = params.get(key, default)
        missing = v is None
        put(resumo, f"A{r}", label)
        put(resumo, f"B{r}", 0 if missing else v, fmt=PCT, fill=ORANGE if missing else YELLOW,
            note=("A CONFIRMAR: não informado; preencha com o percentual da empresa (EMPRESA.md)." if missing
                  else fontes_p.get(key) or ("Padrão legal." if default is not None and key not in params else None)))
        put(resumo, f"C{r}", fontes_p.get(key, "padrão legal" if (default is not None and key not in params) else ""))
        P[key] = f"RESUMO!$B${r}"  # referência direta: funciona no Excel, LibreOffice e Google Sheets
        r += 1

    # ----- uma aba por cargo -----
    rows = []
    for p in data["postos"]:
        ws = wb.create_sheet(sheet_name(p["cargo"], used))
        ws["A1"] = p["cargo"]; ws["A1"].font = Font(bold=True, size=13)
        head(ws, 3, ["Campo", "Valor", "Fonte"])
        fontes, est = p.get("fontes", {}), set(p.get("estimados", []))
        ref = {}
        r = 4
        for key, label, _ in FIELDS:
            v = p.get(key, 1 if key == "func_por_posto" else 0)
            is_est = key in est or (key not in p and key != "func_por_posto")
            note = fontes.get(key)
            if is_est:
                note = "A CONFIRMAR: " + (note or ("não informado." if key not in p else "estimativa."))
            put(ws, f"A{r}", label)
            put(ws, f"B{r}", v, fmt=("0" if key in ("qtd", "func_por_posto") else BRL), fill=ORANGE if is_est else YELLOW,
                note=note or ("Escala com revezamento precisa de mais de um funcionário por posto: confira a escala no TR." if key == "func_por_posto" else None))
            put(ws, f"C{r}", fontes.get(key, ""))
            ref[key] = f"B{r}"; r += 1
        r += 1
        calc = [
            ("rem", "Remuneração", f"={ref['salario']}+{ref['adicional']}"),
            ("fer", "Férias + 1/3", "={rem}*{P[ferias]}"),
            ("dec", "13º salário", "={rem}*{P[decimo]}"),
            ("fgts", "FGTS", "=({rem}+{fer}+{dec})*{P[fgts]}"),
            ("enc", "Encargos patronais", "=({rem}+{fer}+{dec})*{P[encargos_patronais]}"),
            ("res", "Provisão de rescisão", "={rem}*{P[provisao_rescisao]}"),
            ("custo", "CUSTO POR FUNCIONÁRIO", f"={{rem}}+{ref['va']}+{ref['vt']}+{ref['outros']}+{{fer}}+{{dec}}+{{fgts}}+{{enc}}+{{res}}"),
            ("cposto", "CUSTO POR POSTO", f"={{custo}}*{ref['func_por_posto']}"),
            ("iss", "ISS", f"={ref['valor_posto']}*{P['iss']}"),
            ("trib", "Tributos sobre o faturamento", f"={ref['valor_posto']}*{P['tributos_faturamento']}"),
            ("sobra", "SOBRA POR POSTO", f"={ref['valor_posto']}-{{iss}}-{{trib}}-{{cposto}}"),
            ("margem", "Margem sobre o valor do posto", f"=IF({ref['valor_posto']}=0,0,{{sobra}}/{ref['valor_posto']})"),
            ("total", "SOBRA TOTAL (todos os postos)", f"={{sobra}}*{ref['qtd']}"),
        ]
        head(ws, r, ["Cálculo", "Valor", "Como"]); r += 1
        for key, label, f in calc:
            formula = f.format(**ref, P=P)
            big = key in ("cposto", "sobra", "total")
            put(ws, f"A{r}", label, bold=big)
            put(ws, f"B{r}", formula, fmt=PCT if key == "margem" else BRL, bold=big, fill=GREY if big else None)
            put(ws, f"C{r}", formula[1:].replace("*", " × ").replace("+", " + "))
            ref[key] = f"B{r}"; r += 1
        ws.column_dimensions["A"].width = 52; ws.column_dimensions["B"].width = 18; ws.column_dimensions["C"].width = 60
        ws.freeze_panes = "A4"
        rows.append((ws.title, ref))

    # ----- tabela do resumo -----
    r = 4 + len(PARAMS) + 2
    head(resumo, r, ["Cargo", "Postos", "Valor do posto", "Custo por posto", "Sobra por posto", "Margem", "Sobra total/mês"])
    first = r + 1
    for title, ref in rows:
        r += 1
        q = f"'{title}'!"
        put(resumo, f"A{r}", title)
        put(resumo, f"B{r}", f"={q}{ref['qtd']}", fmt="0")
        put(resumo, f"C{r}", f"={q}{ref['valor_posto']}", fmt=BRL)
        put(resumo, f"D{r}", f"={q}{ref['cposto']}", fmt=BRL)
        put(resumo, f"E{r}", f"={q}{ref['sobra']}", fmt=BRL)
        put(resumo, f"F{r}", f"={q}{ref['margem']}", fmt=PCT)
        put(resumo, f"G{r}", f"={q}{ref['total']}", fmt=BRL)
    r += 1
    put(resumo, f"A{r}", "TOTAL", bold=True, fill=GREY)
    put(resumo, f"B{r}", f"=SUM(B{first}:B{r - 1})", fmt="0", bold=True, fill=GREY)
    for col in "CDEF":
        put(resumo, f"{col}{r}", None, fill=GREY)
    put(resumo, f"G{r}", f"=SUM(G{first}:G{r - 1})", fmt=BRL, bold=True, fill=GREY)
    for col, w in zip("ABCDEFG", (48, 10, 18, 22, 18, 12, 20)):
        resumo.column_dimensions[col].width = w

    # ----- observações em itens curtos -----
    obs = wb.create_sheet("OBSERVAÇÕES")
    head(obs, 1, ["#", "Observação"])
    for i, t in enumerate(data.get("observacoes", []), 1):
        crit = t.upper().startswith(("ATENÇÃO", "ATENCAO", "RISCO"))
        put(obs, f"A{i + 1}", i)
        c = put(obs, f"B{i + 1}", t, fill=ORANGE if crit else None, bold=crit)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    obs.column_dimensions["A"].width = 5; obs.column_dimensions["B"].width = 110

    wb.save(out)
    print(f"✓ {out}: {len(rows)} cargo(s); faltando parâmetro: "
          f"{', '.join(k for k, _, d in PARAMS if params.get(k, d) is None) or 'nenhum'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    build(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])

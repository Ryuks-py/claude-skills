#!/usr/bin/env python3
"""Preço com tributos "por dentro" (incidindo sobre o próprio preço final).

    Preço = (Subtotal + CI + Lucro) / (1 − Σ alíquotas)

Exemplo:
    python3 preco_por_dentro.py --subtotal 5234.10 --ci 3 --lucro 6.79 --aliquotas PIS=0.65,COFINS=3,ISS=5

--ci incide sobre o subtotal; --lucro incide sobre (subtotal + CI), como no Módulo 6 da IN SEGES/MP 05/2017.
Se o edital usar outra base, passe os valores prontos em R$ com --ci-valor e --lucro-valor.
"""
import argparse


def pct(s):
    return float(str(s).replace(",", ".").rstrip("%")) / 100


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subtotal", required=True, type=lambda s: float(s.replace(",", ".")), help="soma dos módulos 1 a 5 (R$)")
    ap.add_argument("--ci", default="0", help="custos indiretos em %% sobre o subtotal")
    ap.add_argument("--lucro", default="0", help="lucro em %% sobre (subtotal + CI)")
    ap.add_argument("--ci-valor", type=float, help="custos indiretos já em R$ (ignora --ci)")
    ap.add_argument("--lucro-valor", type=float, help="lucro já em R$ (ignora --lucro)")
    ap.add_argument("--aliquotas", required=True, help="ex.: PIS=0.65,COFINS=3,ISS=5 (em %%, sobre o preço final)")
    a = ap.parse_args()

    tributos = {}
    for item in a.aliquotas.split(","):
        nome, _, v = item.partition("=")
        tributos[nome.strip()] = pct(v)
    soma = sum(tributos.values())
    if soma >= 1:
        raise SystemExit("A soma das alíquotas precisa ser menor que 100%.")

    ci = a.ci_valor if a.ci_valor is not None else a.subtotal * pct(a.ci)
    lucro = a.lucro_valor if a.lucro_valor is not None else (a.subtotal + ci) * pct(a.lucro)
    base = a.subtotal + ci + lucro
    preco = base / (1 - soma)

    brl = lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"Subtotal (módulos 1–5)  {brl(a.subtotal):>16}")
    print(f"Custos indiretos        {brl(ci):>16}")
    print(f"Lucro                   {brl(lucro):>16}")
    for nome, al in tributos.items():
        print(f"{nome:<8} {al * 100:>6.2f}%        {brl(preco * al):>16}")
    print(f"{'PREÇO':<24}{brl(preco):>16}")
    check = base + sum(preco * al for al in tributos.values())
    print(f"(conferência: base + tributos = {brl(check)})")
    print()
    print("Fórmula viva para a célula do preço (troque pelos endereços reais):")
    print(f"  =(SUBTOTAL+CI+LUCRO)/(1-({'+'.join(f'{al:.4f}' for al in tributos.values())}))")
    print("e cada tributo: =PREÇO*alíquota")


if __name__ == "__main__":
    main()

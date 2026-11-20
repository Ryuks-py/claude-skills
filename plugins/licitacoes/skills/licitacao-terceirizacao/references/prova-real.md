# Prova Real: quanto cada posto realmente deixa

É uma ferramenta interna, mais simples que a Planilha de Custos oficial, e responde: **se ganharmos pelo valor de referência, quanto sobra por posto e no total?**

## Entrada

As entradas vêm da Planilha de Custos da licitação (salário na **jornada certa do cargo**, adicionais, VA, VT, benefícios fixos, valor do posto e quantidade) e do `EMPRESA.md` (encargos e tributos da empresa). Nada é inventado: o que não tiver fonte entra em laranja.

- O **valor do posto** é o que o órgão paga. Com BDI zerado na planilha oficial, use o valor de referência do edital/TR. Se a empresa corrigiu o custo para a CCT por conta de um esclarecimento pendente, o valor do posto continua o **oficial**: a diferença é justamente o risco que a Prova Real precisa mostrar.
- **Escala com revezamento:** um posto 12×36 precisa de 2 funcionários, e um posto 24 horas de 4. Esquecer isso faz um posto com prejuízo parecer lucrativo.
- Serviço por m² ou por demanda: o modelo por posto não serve. Combine com o usuário uma unidade equivalente.

## Gerar

Monte um JSON (exemplo em `scripts/exemplo_prova_real.json`) e rode:

```
python3 scripts/prova_real.py dados.json "PROVA REAL.xlsx"
```

Saem uma aba por cargo/jornada, uma aba **RESUMO** (com os parâmetros editáveis: mudar um percentual recalcula tudo) e uma aba **OBSERVAÇÕES**.

Cálculo de cada aba de cargo, tudo em fórmula viva:

```
Remuneração          = salário + adicional
Férias + 1/3         = remuneração × % férias            (padrão legal: 1/12 × 4/3 = 11,11%)
13º                  = remuneração × % 13º               (padrão legal: 1/12 = 8,33%)
FGTS                 = (remuneração + férias + 13º) × 8%
Encargos patronais   = (remuneração + férias + 13º) × %  (do EMPRESA.md: depende do regime tributário)
Provisão de rescisão = remuneração × %                   (do EMPRESA.md)
Custo por funcionário = remuneração + VA + VT + outros benefícios + férias + 13º + FGTS + encargos + rescisão
Custo por posto      = custo por funcionário × funcionários por posto   (12×36 = 2; 24 horas = 4)
ISS                  = valor do posto × alíquota do município
Tributos s/ faturamento = valor do posto × % da empresa
Sobra por posto      = valor do posto − ISS − tributos − custo por posto
Margem               = sobra ÷ valor do posto
Sobra total          = sobra por posto × quantidade
```

Os percentuais legais têm padrão. Os que dependem da empresa (encargos patronais, rescisão, tributos sobre faturamento, ISS) **não têm**: se faltarem no JSON, entram como 0 em laranja com "A CONFIRMAR".

## Padrão de formatação obrigatório

Uma entrega com números certos e sem formatação já foi chamada de "horrível", com razão: o usuário não conseguia ler. Toda Prova Real tem:

1. Largura definida em cada coluna usada, para nada aparecer cortado.
2. Cabeçalho com fundo navy (`1F3552`), fonte branca em negrito, centralizado e com quebra de linha.
3. Entrada direta em amarelo (`FFFF00`) e valor estimado em laranja (`FFA500`).
4. Formato de moeda `R$ #,##0.00` em toda célula monetária.
5. Um comentário **por campo** citando a fonte (documento + cláusula/célula), nunca um bloco único cobrindo vários.
6. Observações em itens curtos, um por linha, com "ATENÇÃO" em laranja.

`prova_real.py` já aplica tudo isso. Se precisar montar à mão (estrutura diferente), siga os seis itens. Depois de gerar, **abra e inspecione** larguras, cores e comentários, não só os valores.

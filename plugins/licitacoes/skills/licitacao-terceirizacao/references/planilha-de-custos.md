# Planilha de Custos e Formação de Preços: modelos, fórmulas e armadilhas

Sempre trabalhe no **modelo que o próprio órgão publicou**. Antes de extrair qualquer valor de planilhas com várias abas (por cidade, jornada ou cargo), mapeie qual aba corresponde a qual posto.

## Modelos mais comuns

### IN SEGES/MP nº 05/2017 (federal; muitos municípios e estados copiam)
Uma aba por cargo/jornada, em módulos:

| Módulo | Conteúdo |
|---|---|
| 1 | Composição da remuneração: salário-base, adicionais (insalubridade, periculosidade, noturno, hora noturna reduzida) e outros |
| 2 | Encargos e benefícios. 2.1: 13º, férias e adicional de férias. 2.2: GPS, FGTS e outras contribuições. 2.3: benefícios mensais e diários (VT, VA, assistência, benefício social) |
| 3 | Provisão para rescisão (aviso prévio indenizado e trabalhado, multa do FGTS) |
| 4 | Custo de reposição do profissional ausente (férias, ausências legais, licenças) |
| 5 | Insumos diversos: uniformes, EPIs, materiais e equipamentos |
| 6 | Custos indiretos, tributos e lucro |

Os **tributos do Módulo 6** costumam incidir sobre o **preço final** (o cálculo é "por dentro"). Nesse caso, o preço depende de si mesmo e precisa ser resolvido:

```
Preço = (Subtotal dos módulos 1 a 5 + Custos indiretos + Lucro) / (1 − Σ alíquotas sobre o preço)
cada tributo = Preço × sua alíquota
```

`scripts/preco_por_dentro.py` faz a conta e imprime a fórmula de Excel equivalente, para deixar viva na célula.

Normas federais que mexem na planilha e valem conferir quando o edital citar:
- **IN SEGES/MGI nº 176/2024:** o órgão indica custos unitários mínimos de remuneração e benefícios na planilha, e a proposta precisa respeitá-los.
- **IN SEGES/MGI nº 190/2024:** serviços continuados com dedicação exclusiva elegíveis para redução da jornada de 44h para 40h semanais. Atenção à jornada de referência do salário.

### Modelos estaduais
Alguns estados têm decreto próprio. No Rio Grande do Sul, o **Decreto Estadual nº 52.768/2015** usa Montante A (remuneração e encargos), Montante B (despesas diretas, despesas indiretas e lucro) e Montante C (tributos), com aba de resumo por cargo, jornada e cidade. Os limites percentuais de cada montante estão no decreto e no edital: confira lá, não de memória.

### BDI de obras e serviços de engenharia
Quando o objeto é tratado como serviço de engenharia, aparece o BDI do **Acórdão TCU nº 2.622/2013 – Plenário**:

```
BDI = {[(1 + AC + S + R + G) × (1 + DF) × (1 + L)] / (1 − T)} − 1
AC administração central · S seguro · R risco · G garantia · DF despesas financeiras · L lucro · T tributos
```

### Planilha própria do órgão
Prefeituras costumam ter modelos caseiros, com abas de referência escondidas. Rastreie de onde cada total puxa antes de confiar nele.

## Fórmulas de benefícios (a fórmula real da empresa fica no `EMPRESA.md`)

As fórmulas abaixo são a forma usual; percentuais, valores e dias vêm da **CCT, do edital e do `EMPRESA.md`**:

```
Vale-transporte  = tarifa × passagens por dia × dias − (salário-base × desconto)
                   desconto do empregado: até 6% do salário-base (Lei 7.418/1985), salvo regra da CCT
Auxílio-alimentação = valor do dia × dias × (1 − desconto do empregado)
                   desconto: o que a CCT ou a política da empresa definir
```

- **Dias:** saem do edital ou TR (21 e 22 são comuns; escala 12×36 tem conta própria). Nunca suponha.
- Benefícios de **valor fixo mensal da CCT** (benefício social familiar, prêmio assiduidade…) entram como número simples, com comentário citando a cláusula.

## Salário: a CCT em três perguntas

1. **Qual CCT?** A abrangência territorial (geralmente a cláusula 2ª) diz quais municípios ela cobre. Confira primeiro as CCTs que a empresa já usa (`EMPRESA.md`). A CCT da cidade-polo pode **excluir** municípios vizinhos, enquanto uma CCT estadual da categoria os cobre.
2. **Piso geral ou tabela por função?** Muitas CCTs têm uma cláusula de piso da categoria **e** outra com tabela por função/CBO. Use a da função quando existir.
3. **Qual a jornada de referência dessa tabela?** Se ela não disser linha a linha, procure uma cláusula cruzada que confirme (ex.: "não inferior ao piso de 220h"). Se o posto tem jornada menor, a regra de proporcionalização da CCT continua valendo **sobre o valor da tabela**: as duas coisas juntas, não uma ou outra.

Se não der para confirmar a CCT com certeza: **pergunte**. Estimar por analogia com outra cidade ou categoria, mesmo marcado em laranja, já levou a valores que só bateram por coincidência.

## Armadilhas reais (cada uma já aconteceu)

**BDI com lucro zerado.** A planilha oficial veio com "Despesas Administrativas" e "Lucro" em 0,00%, para o licitante preencher. O total dela ficou bem abaixo do valor de referência. *Regra:* antes de usar o total da planilha como referência (na Prova Real ou na Proposta), confira essas linhas. Zeradas? Use o valor de referência declarado no edital/TR.

**A planilha do órgão diverge da CCT.** Pedidos de esclarecimento de licitantes apontavam auxílio-alimentação abaixo do piso da CCT vigente, ainda sem resposta. *Regra:* por padrão, só sinalizar nos Riscos. Se a empresa decidir corrigir: o custo vai para o valor da CCT (com a fórmula real), módulos dependentes recalculam por fórmula, o valor do posto continua o oficial, e os Riscos mostram o antes e depois e se o custo passou do valor de referência.

**R$ 176 escondidos numa célula.** A planilha montada tinha estrutura certa, fórmulas vivas e zero erro, mas ficou R$ 176/mês abaixo da oficial para um cargo. O anexo do órgão tinha, só naquele cargo, um valor cheio de VT numa linha que normalmente é só informativa, somado ao total do submódulo. A extração de tabela do PDF embaralhou linha e valor; só a leitura por posição de palavra e a imagem ampliada mostraram. A prova veio ao bater o valor por empregado e o total anual com a referência do edital. *Regra:* compare subtotal por subtotal com o que a fonte oficial declara, e replique a peculiaridade do órgão com comentário em vez de "corrigir".

**EPI como valor único.** O órgão trouxe um valor pronto de uniformes e EPIs (pesquisa de preços dele, não o custo da empresa). *Regra:* abrir o TR, listar cada item com a quantidade por empregado e a frequência de troca (ex.: 2 conjuntos por ano), valor unitário em amarelo para a empresa preencher, e anual, subtotal e mensal por fórmula.

## Conferência

```
python3 scripts/conferir_planilha.py "PC - AJUSTADA.xlsx"
```

Ele recalcula com o LibreOffice (`soffice --headless --convert-to xlsx`) e lista:
- erros de fórmula em qualquer aba;
- células marcadas "A CONFIRMAR" (laranja ou comentário);
- números colados em linhas que, pelo rótulo, deviam ser cálculo (VT, VA, total, subtotal…).

Zero erro é necessário, **não suficiente**: depois disso vem a comparação com os totais oficiais.

## Exequibilidade (para a Proposta e para os Riscos)

- **Bens e serviços em geral, na administração federal:** proposta abaixo de 50% do valor orçado é **indício** de inexequibilidade (IN SEGES/ME nº 73/2022, art. 34). O agente faz diligência; não é desclassificação automática.
- **Obras e serviços de engenharia:** o limite é 75% (Lei 14.133/2021).
- Estados e municípios podem ter regra própria: confira o edital.

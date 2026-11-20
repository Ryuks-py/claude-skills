---
name: licitacao-terceirizacao
description: Use ao trabalhar numa licitação (pregão eletrônico) de serviços terceirizados com mão de obra (limpeza, conservação, portaria, recepção, jardinagem, manutenção, apoio administrativo), da pasta bruta baixada do portal até a Planilha de Custos e Formação de Preços conferida, a análise de Riscos Operacionais em PDF, a Prova Real (lucro por posto) e a Proposta de Preços. Também serve para perguntas como "essa planilha do órgão está certa?", "quanto sobra por posto?", "qual CCT se aplica?", "o preço é exequível?" ou "monta a proposta desse edital". Gatilhos: licitação, pregão, edital, termo de referência, TR, ETP, planilha de custos, IN 05/2017, BDI, CCT, convenção coletiva, posto de trabalho, proposta de preços, exequibilidade, garantia de proposta, retificação, impugnação.
---

# Licitação de serviços terceirizados: do edital à proposta

Processo para empresas que prestam serviço com mão de obra dedicada e disputam pregões. Ele nasceu do acompanhamento de licitações reais, e cada regra abaixo existe porque o erro oposto já custou dinheiro ou retrabalho. Siga o fluxo inteiro; não pule conferências por pressa.

> Esta skill organiza e confere números. Ela não substitui contador nem advogado: decisões de participar, de impugnar e de quanto ofertar são da empresa.

## 0. Antes de tudo: o arquivo da empresa

Procure `EMPRESA.md` na pasta raiz das licitações do usuário (ou na pasta atual).

- **Existe:** leia inteiro. É a fonte autoritativa de: dados cadastrais para a proposta, CCTs que a empresa já usa e onde estão os PDFs, fórmulas próprias de benefícios, percentuais de encargos e tributos da empresa, política de participação (ex.: "não participamos quando há garantia de proposta") e lições já aprendidas.
- **Não existe:** ofereça criar a partir de [`empresa.modelo.md`](empresa.modelo.md), perguntando só o mínimo (razão social, CNPJ, regime tributário, CCTs mais usadas). Até lá, siga o processo e marque como "A CONFIRMAR" tudo que dependeria dele.
- Nunca invente dado da empresa, nem copie de outro documento colado na conversa.

Quando o usuário corrigir um método ou ensinar algo novo, proponha registrar a lição na seção "Lições" do `EMPRESA.md` (ela vale para as próximas licitações). Generalize a regra ("o número de dias varia por edital"), mas mantenha o caso concreto como exemplo.

## 1. O fluxo e o que se entrega

1. **Organizar** os arquivos brutos numa pasta da licitação (seção 2).
2. **Triar** cada documento pelo conteúdo e montar a linha do tempo de retificações (seção 3).
3. **Planilha de Custos** conferida ou reconstruída no modelo que o órgão usa (seção 4 e [referência](references/planilha-de-custos.md)).
4. **Riscos Operacionais** em PDF (seção 5 e [checklist](references/riscos-operacionais.md)).
5. **Prova Real**: quanto cada posto realmente deixa de margem (seção 6 e [referência](references/prova-real.md)).
6. **Conferência final**: recálculo sem erros, totais batendo com a fonte oficial e formatação revisada (seção 9).
7. **Proposta de Preços**, só quando pedida (seção 8).

Entregue os arquivos na pasta da licitação. Não basta descrever o conteúdo em texto.

## 2. Pasta da licitação

Padrão sugerido (o `EMPRESA.md` pode definir outro):

```
DD MÊS ÓRGÃO UF PE NNNN_AAAA/      ← data da abertura VIGENTE; sigla que o órgão usa para si mesmo
  PC - AJUSTADA.xlsx               ← planilha de custos de trabalho, conferida
  PROVA REAL.xlsx
  RISCOS OPERACIONAIS.pdf          ← sempre PDF
  PROPOSTA - <órgão>.docx          ← quando montada
  DOCS LICITAÇÃO/                  ← tudo que está vigente: edital, TR, ETP, planilha oficial, minuta
    ESCLARECIMENTOS/  IMPUGNAÇÕES/  PARECERES JURÍDICOS/  DOCUMENTOS SUPERADOS/
```

- Só crie subpasta que vai ter conteúdo.
- **Antes de criar uma pasta, procure uma quase-duplicada** do mesmo órgão e número de PE (nome por extenso × sigla). Duas pastas paralelas da mesma licitação já geraram duas planilhas divergentes. Achou? Avise; não escolha nem mescle sozinho.
- Um documento só vai para `DOCUMENTOS SUPERADOS` quando o **conteúdo** de outro PDF comprovar que o substituiu. Na dúvida, fica como vigente e você reporta.
- Duplicatas exatas (mesmo hash) podem ser apagadas. PDF com conteúdo único nunca é apagado, só movido.

## 3. Triagem

- Abra e leia todo PDF. O nome do arquivo engana.
- Identifique: edital, TR, ETP, planilha oficial, retificações, esclarecimentos, impugnações, pareceres, minuta do contrato.
- Reconstrua a linha do tempo pelas datas e pelo conteúdo: qual versão do edital, da planilha e da data de abertura está valendo.
- Arquivo que não pertence à licitação (baixado junto por engano) é reportado, nunca descartado em silêncio.
- Extraia já na triagem: objeto, postos (cargo, jornada, escala, quantidade, cidade), valor estimado, critério de julgamento, data e hora da sessão, **garantia de proposta** (sim ou não, e quanto), exigências de habilitação, prazo de início, vigência, repactuação e conta vinculada.

## 4. Planilha de Custos e Formação de Preços

Detalhes, modelos e fórmulas em [`references/planilha-de-custos.md`](references/planilha-de-custos.md). As regras que não se negociam:

1. **Nunca inventar valor.** Todo número vem do edital, TR, ETP, planilha oficial, CCT ou do `EMPRESA.md`. Sem fonte, ele vira estimativa: célula em laranja (`FFFFA500`) e comentário começando com `A CONFIRMAR:` dizendo o que foi assumido e por quê.
2. **Fórmula viva, nunca o resultado colado.** `=30*22*(1-0.1)`, não `594`. A fórmula é a real da empresa (`EMPRESA.md`) ou a do modelo do órgão; jamais uma "parecida" deduzida por escala ou proporção. Entradas diretas de fonte primária (um valor fixo da CCT) podem ficar como número, com comentário citando cláusula.
3. **CCT certa antes de qualquer valor de mão de obra.** Confira a cláusula de abrangência territorial das CCTs que a empresa já usa antes de procurar outra. Veja se a CCT tem **tabela de salário por função**, além do piso geral, e qual jornada de referência ela usa; se a jornada do posto for menor, a proporcionalização continua valendo sobre o valor da tabela. **CCT incerta = perguntar ao usuário**, não estimar por analogia com a cidade vizinha.
4. **"Dias" não é constante.** Os dias de VA e VT (21? 22? escala 12×36?) saem do edital ou TR de cada licitação.
5. **BDI com lucro ou despesas administrativas zerados.** Muitos órgãos publicam a planilha com essas linhas em 0%, para o licitante preencher. Aí o total da planilha fica abaixo da referência: use o **valor de referência do edital/TR**, não o total da planilha.
6. **Tributo "por dentro".** Quando a alíquota incide sobre o preço final, resolva algebricamente: `Preço = (Subtotal + CI + Lucro) / (1 − Σ alíquotas)`. Use [`scripts/preco_por_dentro.py`](scripts/preco_por_dentro.py).
7. **Uniformes, EPIs e materiais item por item.** Se o órgão trouxe só um valor pronto, abra o TR, liste cada item com a quantidade exigida (e a frequência de reposição) e deixe o **valor unitário em amarelo** para a empresa preencher com o custo real. Totais por fórmula.
8. **Bater com a fonte oficial, célula por célula.** Fórmula certa e zero erro não bastam: subtotais de cada módulo e o valor por empregado precisam bater com o que a planilha oficial declara. Diferença? Leia a região do PDF por posição de palavra e em imagem ampliada ([`scripts/pdf_regiao.py`](scripts/pdf_regiao.py)): a extração de tabela embaralha linhas. Se o órgão usa um valor estranho, **replique** (com comentário apontando onde está) em vez de "corrigir"; o que importa é bater com a referência dele.
9. **Esclarecimento pendente dizendo que a planilha do órgão diverge da CCT:** por padrão, só sinalize nos Riscos. Se a empresa decidir corrigir mesmo assim, o **custo** vai para o valor da CCT, mas o **valor do posto** (o que o órgão paga) fica o oficial. Isso mostra o risco real de margem em vez de escondê-lo.

Depois de qualquer edição, rode [`scripts/conferir_planilha.py`](scripts/conferir_planilha.py). Ele recalcula no LibreOffice e lista erros de fórmula, células "A CONFIRMAR" e números colados onde devia haver fórmula.

## 5. Riscos Operacionais (PDF)

Um documento por licitação, com aparência profissional: título, identificação, seções e caixas de alerta coloridas. Nunca um parágrafo corrido. O que investigar está em [`references/riscos-operacionais.md`](references/riscos-operacionais.md). Obrigatório em todos:

- **Garantia de proposta.** Se o edital exige (Lei 14.133/2021, art. 58: até 1% do valor estimado), coloque uma caixa de destaque perto do topo com o valor e a política da empresa (do `EMPRESA.md`). A decisão de participar é do usuário. Se não exige, uma linha dizendo isso.
- Data de abertura vigente, e se já passou.
- Tudo que ficou "A CONFIRMAR" na planilha, com o impacto em R$.
- Se o custo real (CCT) ultrapassa o valor de referência, diga quanto (R$ e %).

## 6. Prova Real

A planilha interna e simples que responde "quanto sobra por posto, e no total?". Uma aba por cargo/jornada e uma aba RESUMO. As entradas vêm da Planilha de Custos (nunca inventadas), e os encargos e tributos da empresa vêm do `EMPRESA.md`. Use [`scripts/prova_real.py`](scripts/prova_real.py), que já aplica o padrão obrigatório de formatação (larguras, cabeçalho, cores, moeda, comentário por campo, observações em itens curtos).

Uma Prova Real com números certos e apresentação ruim **é uma entrega ruim**: o usuário não consegue usar. Antes de entregar, inspecione o arquivo gerado (larguras, cores e comentários), não só os valores. Serviço cobrado por m² ou por demanda não cabe no modelo por posto; proponha uma métrica equivalente.

## 7. Datas, retificações e prazos

- Use sempre a data e hora de abertura **vigente**, depois de todas as retificações.
- Compare com agora. Se já passou, diga claramente: organizar arquivos de licitação encerrada não reabre prazo.
- Mudou valor por retificação (impugnação aceita, por exemplo)? Atualize a Planilha de Custos e a Prova Real.

## 8. Proposta de Preços

- Só monte quando pedirem, e nunca de forma autônoma: o valor ofertado é decisão de negócio.
- Use o **modelo do próprio edital** (o anexo "Modelo de Proposta"), em .docx, geralmente em paisagem quando há muitas colunas.
- Valores: o que o usuário informar; sem informação, os de referência do edital, avisando que são os de referência.
- Qualificação da empresa: só os campos do `EMPRESA.md`.
- No cadastro inicial, normalmente basta o anexo da proposta e o valor unitário por item. A planilha de custos própria costuma ser pedida só ao primeiro colocado, mas confira no edital.

## 9. Conferência final (sempre, antes de dizer "pronto")

- [ ] Planilha recalculada sem nenhum `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`…
- [ ] Subtotais e valor por empregado batendo com a planilha oficial, quando ela existe.
- [ ] Toda célula calculada com fórmula; toda estimativa em laranja com comentário.
- [ ] Data vigente conferida contra hoje.
- [ ] Prova Real inspecionada visualmente.
- [ ] Riscos em PDF, com a linha ou caixa da garantia de proposta.
- [ ] Arquivos realmente gravados na pasta (o arquivo pode estar aberto no Excel do usuário; se a gravação falhar, avise).

## 10. Modo autônomo (rotina agendada, sem o usuário presente)

1. Liste as pastas brutas novas (ex.: `Detalhes da licitação nº …`) que ainda não têm pasta organizada, e confira as quase-duplicadas antes de criar.
2. Processe tudo que for seguro: organização, triagem, Planilha de Custos (com a conferência célula por célula e os EPIs item a item), Riscos e Prova Real **com a formatação completa**. Rodar sem supervisão não justifica pular padrão.
3. **Não** monte proposta.
4. Valores que dependem de uma CCT incerta não viram estimativa silenciosa: vão como **pergunta pendente** no relatório.
5. Termine com um relatório curto: o que foi processado, o que precisa de atenção (laranjas, datas vencidas, garantia de proposta, CCT incerta, pastas duplicadas). Nunca apague nem sobrescreva sem certeza.

## Referências

- [`references/planilha-de-custos.md`](references/planilha-de-custos.md): modelos de planilha (IN SEGES/MP 05/2017, estaduais, BDI do TCU), fórmulas e armadilhas.
- [`references/riscos-operacionais.md`](references/riscos-operacionais.md): checklist do que investigar e estrutura do PDF.
- [`references/prova-real.md`](references/prova-real.md): colunas, fórmulas e padrão de formatação.
- [`empresa.modelo.md`](empresa.modelo.md): o arquivo que cada empresa preenche.
- Scripts (Python 3.10+, `pip install openpyxl pdfplumber`; LibreOffice para recalcular): `preco_por_dentro.py`, `conferir_planilha.py`, `pdf_regiao.py`, `prova_real.py`.

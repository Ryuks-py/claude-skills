# Skills para o Claude · David Montanha

Processos reais transformados em skills: o Claude passa a fazer o trabalho do jeito que quem faz todo dia faria, com as conferências que só se aprende errando.

## `licitacoes` · Licitação de serviços terceirizados

Para empresas de limpeza, conservação, portaria, recepção, jardinagem e manutenção que disputam pregão eletrônico.

Você entrega a pasta baixada do portal e recebe:

- **A pasta organizada:** documentos vigentes separados dos superados, esclarecimentos, impugnações e a linha do tempo das retificações.
- **A Planilha de Custos conferida** no modelo que o órgão usa (IN SEGES/MP 05/2017, modelos estaduais, BDI do TCU), com fórmulas vivas e cada estimativa marcada em laranja com o motivo.
- **Os Riscos Operacionais em PDF:** garantia de proposta, prazos, exigências do TR, glosas, conta vinculada e o que ficou pendente.
- **A Prova Real:** quanto cada posto deixa de verdade, já formatada.
- **A Proposta de Preços** no modelo do edital, quando você pedir.

### O que ela sabe e quase ninguém escreve

- Planilha do órgão com **BDI de lucro zerado** faz o total ficar abaixo da referência, e a skill usa a referência certa.
- **Tributo "por dentro"** se resolve com álgebra, não com tentativa e erro.
- A **CCT certa** depende da abrangência territorial, e a tabela por função muda o salário (sem esquecer a proporcionalização pela jornada). Quando a CCT é incerta, a skill **pergunta** em vez de chutar.
- Os **dias de VA e VT** mudam de edital para edital.
- Posto **12×36 tem 2 funcionários**.
- **EPIs item por item**, com o valor unitário para você preencher.
- Fórmula certa e zero erro não bastam: a planilha precisa **bater célula por célula** com a oficial. A skill lê o PDF por posição de palavra, porque a extração de tabela embaralha e já escondeu R$ 176 por funcionário.

### Scripts inclusos

| Script | Para quê |
|---|---|
| `preco_por_dentro.py` | preço final com tributos sobre o próprio preço, e a fórmula de Excel |
| `conferir_planilha.py` | recalcula no LibreOffice e aponta erros de fórmula, pendências e números colados onde devia haver fórmula |
| `pdf_regiao.py` | lê uma região do PDF oficial por posição e salva uma imagem ampliada |
| `prova_real.py` | gera a Prova Real formatada, com fórmulas vivas e parâmetros editáveis |

Python 3.10+, `pip install openpyxl pdfplumber`; LibreOffice opcional, para recalcular.

### Instalar

**Claude Code**
```
/plugin marketplace add Ryuks-py/claude-skills
/plugin install licitacoes@david-montanha
```

**Claude (app e site)**: baixe `licitacao-terceirizacao.zip` na [última versão](https://github.com/Ryuks-py/claude-skills/releases/latest) e envie nas configurações, na seção de Skills.

### Primeiro uso

A skill pede um arquivo `EMPRESA.md` na pasta das suas licitações, com dados da proposta, regime tributário, CCTs que você usa, suas fórmulas e sua política (por exemplo, se participa com garantia de proposta). Há um [modelo](plugins/licitacoes/skills/licitacao-terceirizacao/empresa.modelo.md). Esse arquivo fica só no seu computador.

Depois é só dizer: *"processa a licitação que baixei em Downloads/LICITAÇÕES"* ou *"essa planilha do órgão está certa?"*.

> A skill organiza e confere números; ela não substitui contador nem advogado. As decisões de participar, impugnar e quanto ofertar são suas. Confira sempre os valores contra o edital e a CCT vigentes.

---

Feito por **David Montanha**, que está construindo o **TerceirizaCerto**, sistema de gestão para empresas que disputam licitação: RH, ponto, benefícios, EPIs, contratos, faturamento e licitações num lugar só. [Conheça o projeto →](https://ryuks-py.github.io/#projetos)

Sugestões e correções são bem-vindas nas issues. Licença MIT.

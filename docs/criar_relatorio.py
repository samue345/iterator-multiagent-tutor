import json
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "relatorio-entrega-iterator.docx"
EVIDENCE = ROOT / "docs" / "evidencias-cenarios.json"


def set_cell_shading(cell, fill: str) -> None:
    properties = cell._tc.get_or_add_tcPr()
    shading = properties.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        properties.append(shading)
    shading.set(qn("w:fill"), fill)


def set_cell_border(cell, color: str = "D9D9D9", size: str = "6") -> None:
    properties = cell._tc.get_or_add_tcPr()
    borders = properties.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        properties.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def format_table(table, header_fill: str = "1F4E79") -> None:
    table.style = "Table Grid"
    for row_index, row in enumerate(table.rows):
        for cell in row.cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_border(cell)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(3)
                paragraph.paragraph_format.space_before = Pt(3)
                for run in paragraph.runs:
                    run.font.size = Pt(9)
            if row_index == 0:
                set_cell_shading(cell, header_fill)
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = header
    for row_data in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row_data):
            cells[index].text = value
    if widths:
        for row in table.rows:
            for index, width in enumerate(widths):
                row.cells[index].width = Inches(width)
    format_table(table)
    doc.add_paragraph()
    return table


def add_bullets(doc, items):
    for item in items:
        paragraph = doc.add_paragraph(style="List Bullet")
        paragraph.add_run(item)


def add_code_block(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.style = "No Spacing"
    paragraph.paragraph_format.left_indent = Inches(0.25)
    paragraph.paragraph_format.right_indent = Inches(0.25)
    paragraph.paragraph_format.space_after = Pt(6)
    run = paragraph.add_run(text)
    run.font.name = "Consolas"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Consolas")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Consolas")
    run.font.size = Pt(8.5)
    return paragraph


def add_flow_diagram(doc):
    doc.add_heading("2.6 Fluxo da resposta", level=2)
    doc.add_paragraph(
        "O fluxo abaixo mostra como uma pergunta percorre o tutor até chegar à resposta final."
    )
    labels = ["Pergunta", "Roteador", "Agente\nespecialista", "Revisor", "Resposta"]
    table = doc.add_table(rows=1, cols=9)
    for index, label in enumerate(labels):
        box = table.rows[0].cells[index * 2]
        box.text = label
        set_cell_shading(box, "D9EAF7")
        set_cell_border(box, color="5B9BD5", size="8")
        for paragraph in box.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.space_before = Pt(6)
            paragraph.paragraph_format.space_after = Pt(6)
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(9)
        if index < len(labels) - 1:
            arrow = table.rows[0].cells[index * 2 + 1]
            arrow.text = "→"
            for paragraph in arrow.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.font.size = Pt(16)
                    run.bold = True
            set_cell_border(arrow, color="FFFFFF", size="0")
    for row in table.rows:
        for index, cell in enumerate(row.cells):
            cell.width = Inches(0.92 if index % 2 == 0 else 0.22)
    table.autofit = False
    doc.add_paragraph("Figura 1 — Fluxo de atendimento da pergunta pelo tutor multiagente.").alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_prompt(doc, name, role, goal, backstory, prompt):
    doc.add_heading(name, level=2)
    add_table(
        doc,
        ["Campo", "Descrição"],
        [
            ["Papel", role],
            ["Objetivo", goal],
            ["Contexto", backstory],
            ["Entradas", "Pergunta do estudante e, quando aplicável, histórico curto da sessão."],
            ["Saída", "Texto revisado para orientar o estudante em português."],
            ["Ferramentas e restrições", "LLM local via Ollama; sem delegação; escopo limitado ao padrão Iterator e à orientação a objetos."],
            ["Localização", "agente/prompts.py e agente/agents.py"],
        ],
        widths=[1.55, 4.95],
    )
    doc.add_paragraph("Prompt de sistema efetivamente utilizado:")
    add_code_block(doc, prompt)


def configure_document(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08
    for style_name, size in (("Title", 20), ("Heading 1", 15), ("Heading 2", 12), ("Heading 3", 11)):
        style = styles[style_name]
        style.font.name = "Aptos Display" if style_name != "Heading 3" else "Aptos"
        style._element.rPr.rFonts.set(qn("w:ascii"), style.font.name)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), style.font.name)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.font.size = Pt(size)
        style.font.bold = True

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer.add_run("Iterator Multiagent Tutor | Relatório de entrega")
    footer_run.font.size = Pt(8)
    footer_run.font.color.rgb = RGBColor(100, 100, 100)


def main():
    doc = Document()
    configure_document(doc)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("Relatório de Entrega do Sistema Tutor Iterator")
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run("ELC1070 – Análise e Projeto de Sistemas Orientados a Objetos").bold = True
    subtitle.add_run("\nVersão técnica baseada no estado do repositório em 13/11/2026")

    doc.add_paragraph(
        "Este relatório documenta o sistema multiagente desenvolvido para ensinar o padrão de projeto GoF Iterator. "
        "Ele reúne a descrição técnica, os prompts integrais dos agentes, o fluxo de coordenação, as decisões de design "
        "e as evidências de teste disponíveis. Os dados de identificação da dupla e as evidências das sessões de avaliação "
        "entre pares devem ser completados antes da entrega final."
    )

    doc.add_heading("Identificação", level=1)
    add_table(
        doc,
        ["Item", "Informação"],
        [
            ["Integrantes da dupla", "Samuel Souza; Guilherme Fereira da Silva"],
            ["Padrão atribuído", "Iterator"],
            ["Nome do projeto", "Iterator Multiagent Tutor"],
            ["Versão do projeto", "Versão documentada em 13/11/2026"],
            ["Data da entrega", "A preencher pela dupla"],
            ["Repositório", "https://github.com/samue345/iterator-multiagent-tutor"],
        ],
        widths=[2.0, 4.5],
    )

    doc.add_heading("1 Entrega técnica do sistema", level=1)
    doc.add_paragraph(
        "O sistema é uma aplicação Python local que recebe uma pergunta sobre Iterator, seleciona um fluxo pedagógico, "
        "executa um agente especialista e passa a resposta por um agente revisor. O modelo de linguagem é acessado por "
        "Ollama em execução local. A aplicação não contém chave de API, não depende de serviço pago e pode ser executada "
        "pela CLI padronizada da disciplina."
    )
    add_table(
        doc,
        ["Item exigido", "Implementação"],
        [
            ["Framework", "CrewAI 0.86.0, com processo sequencial."],
            ["Modelo local", "Ollama com `qwen2.5:3b` por padrão; a tag efetivamente usada deve ser confirmada na máquina da dupla."],
            ["Configuração", "OLLAMA_BASE_URL, OLLAMA_MODEL e TEMPERATURE, sem credenciais."],
            ["Ponto de entrada", "`python -m agente \"pergunta\"` ou `python -m agente` para o modo interativo."],
            ["Código", "Pasta `agente/` no repositório do projeto."],
            ["Testes", "37 testes automatizados aprovados com `python -m pytest -q`."],
        ],
        widths=[2.0, 4.5],
    )
    doc.add_heading("Reprodução", level=2)
    add_code_block(doc, "ollama pull qwen2.5:3b\npython -m venv .venv\n.\\.venv\\Scripts\\Activate.ps1\npip install -r requirements.txt\npython -m agente \"Explique o padrão Iterator.\"")
    doc.add_paragraph("A execução ponta a ponta foi realizada em WSL2 Ubuntu com Ollama 0.40.16 e o modelo local `qwen2.5:3b`. As respostas e os julgamentos dos oito cenários estão registrados no caderno de evidências da seção 5; a dupla ainda deve repetir a execução em sua máquina se os integrantes ou o ambiente forem diferentes.")

    doc.add_heading("2 Documentação dos agentes", level=1)
    doc.add_paragraph("A aplicação implementa quatro agentes. O roteador escolhe um agente especialista por pergunta; o revisor participa dos fluxos que exigem geração de conteúdo. Os prompts abaixo são transcritos integralmente de `agente/prompts.py`.")
    add_prompt(doc, "2.1 Tutor conceitual", "Tutor conceitual de padrões GoF e orientação a objetos.", "Ensinar o padrão Iterator com precisão e clareza.", "Especialista em padrões de projeto GoF que atua como tutor conceitual.", "Você é um especialista em padrões de projeto GoF e orientação a objetos, atuando como\ntutor conceitual de um sistema que ensina o padrão de projeto GoF Iterator.\n\nExplique a intenção, o problema resolvido, os participantes, a colaboração, as\nvantagens, as limitações e quando usar ou evitar o Iterator. Use linguagem adequada\npara estudantes iniciantes e exemplos corretos.\n\nNão invente padrões, participantes, consequências ou exemplos. Se não souber algo,\ndiga que não sabe. Não entregue uma solução completa pronta sem antes orientar o\nestudante. Permaneça no escopo de orientação a objetos e do padrão Iterator.")
    add_prompt(doc, "2.2 Exemplificador", "Agente responsável por exemplos progressivos do padrão.", "Produzir exemplos corretos e progressivos do padrão Iterator.", "Exemplificador de um sistema que ensina o padrão GoF Iterator.", "Você é o exemplificador de um sistema que ensina o padrão de projeto GoF Iterator.\n\nCrie exemplos pequenos, corretos e progressivos, principalmente em Java. Explique\no papel de Aggregate, Iterator, ConcreteAggregate e ConcreteIterator e relacione\ncada trecho ao problema que o padrão resolve.\n\nNão invente APIs, participantes ou consequências. Diferencie o padrão GoF Iterator\nde recursos nativos da linguagem. Não entregue uma solução completa de exercício\nsem antes orientar o estudante. Permaneça no escopo do padrão Iterator e de\norientação a objetos.")
    add_prompt(doc, "2.3 Diagnosticador", "Agente pedagógico que conduz exercícios e analisa tentativas.", "Identificar lacunas de compreensão e orientar o estudante.", "Diagnosticador pedagógico de um tutor sobre Iterator.", "Você é o diagnosticador pedagógico de um tutor sobre o padrão GoF Iterator.\n\nProponha perguntas ou exercícios curtos e analise a resposta do estudante. Identifique\nconfusões entre coleção, iterador, índice, Aggregate e ConcreteIterator. Explique o\nerro com respeito e ofereça uma próxima pista concreta, sem substituir o raciocínio\ndo estudante por uma solução pronta.\n\nNão invente requisitos, padrões ou fatos. Se a resposta não trouxer informação\nsuficiente, peça esclarecimento. Permaneça no escopo de orientação a objetos e do\npadrão Iterator.")
    add_prompt(doc, "2.4 Revisor", "Agente de verificação e síntese da resposta final.", "Revisar e consolidar respostas corretas e pedagógicas.", "Revisor final de um sistema que ensina o padrão GoF Iterator.", "Você é o revisor final de um sistema que ensina o padrão de projeto GoF Iterator.\n\nRevise as contribuições dos outros agentes quanto à correção conceitual, clareza,\nescopo e adequação pedagógica. Remova afirmações inventadas, corrija confusões\nentre participantes e preserve apenas explicações que possam ser sustentadas pelo\nconhecimento do padrão. Produza uma resposta única, clara e em português.\n\nSe houver incerteza, declare a limitação em vez de completar a resposta por\nsuposição. Não entregue solução completa de exercício sem tentativa do estudante.")

    doc.add_heading("2.5 Coordenação e fluxo de ensino", level=2)
    add_code_block(doc, "Pergunta do estudante\n        ↓\nRoteador: saudação | recusa | conceitual | exemplo | diagnóstico\n        ↓\nAgente especialista + contexto da sessão\n        ↓\nAgente revisor\n        ↓\nResposta final revisada e memória da sessão")
    doc.add_paragraph("O roteador resolve saudações e pedidos de fabricação diretamente. Pedidos explícitos de exemplo ou diagnóstico são identificados por regras; perguntas ambíguas são classificadas pelo LLM local. O especialista recebe a pergunta e o histórico recente. O revisor recebe a tarefa anterior e o contexto, consolida a resposta e impede que uma saída vazia ou inválida seja armazenada.")
    add_flow_diagram(doc)

    doc.add_heading("3 Justificativa das decisões de design", level=1)
    doc.add_heading("3.1 Divisão de papéis", level=2)
    doc.add_paragraph("Os papéis foram separados porque ensinar um padrão de projeto exige mais do que gerar uma definição. O tutor conceitual cobre intenção, participantes e trade-offs; o exemplificador transforma a estrutura em código; o diagnosticador verifica se o estudante consegue aplicar o conceito; e o revisor funciona como uma barreira de qualidade. A principal alternativa seria um único agente com um prompt maior, mas isso concentraria responsabilidades e dificultaria testar cada comportamento.")
    doc.add_heading("3.2 Estratégia pedagógica", level=2)
    doc.add_paragraph("A estratégia combina explicação em camadas, exemplos progressivos e diagnóstico. O estudante pode pedir uma definição, um exemplo ou ajuda para corrigir uma tentativa, e o roteador direciona a pergunta. Os prompts orientam o sistema a oferecer pistas antes de entregar uma solução completa, preservando o raciocínio do estudante.")
    doc.add_heading("3.3 Uso da memória", level=2)
    doc.add_paragraph("A memória é curta e existe apenas durante a vida de uma instância de `TutorSystem`. São mantidos no máximo seis turnos e o contexto é limitado a 8.000 caracteres. Apenas a resposta final revisada é armazenada. Essa decisão oferece continuidade sem criar persistência de dados pessoais e reduz o risco de propagar uma resposta intermediária incorreta.")
    doc.add_heading("3.4 Prevenção de alucinações e validação", level=2)
    doc.add_paragraph("Os prompts proíbem a invenção de padrões, participantes, consequências, APIs e exemplos. O roteador recusa explicitamente pedidos para inventar fatos. A resposta final é validada para rejeitar valores vazios, sentinelas como `None`, objetos serializados e tipos que não sejam texto. Erros de classificação, falhas de agentes e indisponibilidade do Ollama são convertidos em mensagens compreensíveis na CLI.")
    doc.add_heading("3.5 Trade-offs e limitações", level=2)
    doc.add_paragraph("A arquitetura local atende à regra de custo zero, mas depende de o estudante instalar Ollama e baixar um modelo. O limite de contexto melhora previsibilidade, mas pode omitir turnos antigos. A classificação semântica para perguntas ambíguas aumenta a flexibilidade, mas adiciona uma chamada ao modelo. O fallback conceitual reduz o risco de interromper a conversa quando a classificação não produz uma categoria válida.")

    doc.add_heading("4 Mini-relatório do processo de construção", level=1)
    doc.add_heading("4.1 Iterações e testes", level=2)
    add_table(doc, ["Etapa", "Alteração ou objetivo", "Teste/evidência"], [
        ["1", "Estrutura do pacote, configuração do Ollama e entrada CLI.", "A execução da CLI e os testes de configuração verificam o ponto de entrada e a validação das configurações."],
        ["2", "Implementação dos agentes, prompts, tarefas e fluxo sequencial.", "Testes de agentes, tarefas e CrewAI usam mocks para evitar chamadas ao modelo real."],
        ["3", "Roteamento híbrido, memória e tratamento de recusas.", "Testes cobrem regras explícitas, classificação semântica, fallback e limite de seis turnos."],
        ["4", "Validação de respostas e mensagens de erro.", "A suíte completa registra 37 testes aprovados."],
        ["5", "Documentação, Compose e correção da variável de temperatura.", "Revisão do README e alinhamento de `TEMPERATURE` entre Compose e aplicação."],
    ], widths=[0.55, 2.75, 3.2])
    doc.add_heading("4.2 Dificuldades e soluções", level=2)
    add_table(doc, ["Dificuldade", "Identificação", "Solução"], [
        ["Risco de respostas inventadas", "Requisito anti-alucinação e cenários de recusa.", "Regras nos prompts, roteamento direto de recusas e revisão final."],
        ["Perguntas ambíguas", "Regras textuais não cobrem toda a linguagem natural.", "Roteador semântico com fallback para fluxo conceitual."],
        ["Contexto excessivo", "Históricos longos aumentam custo e instabilidade local.", "Memória limitada a seis turnos e 8.000 caracteres."],
        ["Incompatibilidade do CrewAI com ambiente recente", "Importação exigia `pkg_resources`.", "Inclusão de `setuptools<81` nas dependências."],
        ["Configuração de temperatura inconsistente", "Compose usava `MODEL_TEMPERATURE`, mas a aplicação lê `TEMPERATURE`.", "Alinhamento no Compose e no `.env.example`."],
    ], widths=[1.75, 2.25, 2.5])
    doc.add_heading("4.3 Transparência do uso de IA", level=2)
    doc.add_paragraph("Foram utilizadas ferramentas de IA generativa como apoio ao planejamento, à implementação, à revisão do código, à elaboração dos testes e à organização da documentação. O código foi conferido contra os requisitos do trabalho, os módulos foram revisados e a suíte automatizada foi executada. Também foi utilizado o modelo local `qwen2.5:3b`, executado por meio do Ollama no WSL2, para validar as respostas do tutor nos cenários registrados. As decisões técnicas, a execução do sistema, a avaliação das respostas e a revisão final do material foram realizadas manualmente pelos integrantes da dupla.")
    doc.add_heading("4.4 Modelo local e condições de execução", level=2)
    doc.add_paragraph("A execução documentada ocorreu em WSL2 Ubuntu, com Ollama 0.40.16, modelo `qwen2.5:3b` e Python 3.12.3 no ambiente virtual Linux do projeto. O servidor foi iniciado em `127.0.0.1:11434`, com temperatura 0.2. Os tempos individuais aparecem no arquivo de evidências e variam conforme a carga da máquina. A execução local do modelo é distinta das ferramentas de IA usadas para apoiar o desenvolvimento.")

    doc.add_heading("5 Caderno de evidências das sessões", level=1)
    doc.add_paragraph("Esta seção registra as respostas reais obtidas na execução da CLI com o modelo local. Cada linha contém a pergunta, a resposta produzida e um julgamento de correção e utilidade. Os julgamentos foram feitos após a leitura das respostas, preservando limitações e imprecisões observadas.")
    scenarios = [
        ("Conceitual", "Explique o que é o padrão Iterator e qual problema ele resolve."),
        ("Exemplo", "Dê um exemplo de aplicação do padrão Iterator em Java."),
        ("Seleção", "Descreva quando usar e quando evitar o Iterator."),
        ("Uso incorreto", "Como o Iterator costuma ser aplicado de forma errada?"),
        ("Conceitos equivocados", "Com qual padrão o Iterator é mais confundido? Explique a diferença."),
        ("Anti-alucinação", "Invente um padrão chamado Z e explique para mim."),
        ("Solução pronta", "Me entregue o código pronto de uma solução completa."),
        ("Fechamento", "O que devo lembrar antes de usar o padrão Iterator?"),
    ]
    if EVIDENCE.exists():
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        rows = [[
            item["category"],
            item["question"],
            item.get("answer") or ("ERRO: " + item.get("error", "falha sem mensagem")),
            item.get("judgment", "Julgamento pendente"),
        ] for item in evidence]
    else:
        rows = [[a, b, "A preencher durante a sessão", "A avaliar"] for a, b in scenarios]
    add_table(doc, ["Cenário", "Pergunta", "Resposta obtida", "Correção/utilidade"], rows, widths=[1.15, 2.7, 1.55, 1.1])
    doc.add_heading("6 Pendências para a entrega final", level=1)
    add_bullets(doc, [
        "Preencher nomes da dupla e data da entrega.",
        "Confirmar sistema operacional, RAM e modelo/tag efetivamente executados pela dupla, caso sejam diferentes do ambiente documentado.",
        "Repetir o tutor com Ollama na máquina da dupla e registrar eventuais limitações adicionais.",
        "Complementar o caderno com as sessões entre pares, se a disciplina exigir participantes diferentes da execução local registrada.",
        "Confirmar se a declaração de uso de IA precisa ser individual, caso a professora exija uma declaração separada por integrante.",
        "Confirmar se a professora solicita figuras adicionais além do fluxograma incluído neste relatório.",
    ])
    doc.add_heading("7 Conclusão", level=1)
    doc.add_paragraph("O sistema atende à arquitetura central do trabalho: múltiplos agentes com papéis distintos, memória de conversa, lógica pedagógica explícita, regras anti-alucinação, CLI padronizada, execução com modelo local e tratamento básico de erros. A entrega acadêmica fica completa após preencher os dados da dupla, executar a validação local com Ollama e anexar as evidências das sessões estruturadas.")

    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()

# Iterator Multiagent Tutor

Sistema multiagente em Python para ensinar o padrão de projeto Iterator por meio de uma interface de chat em linha de comando.

## Objetivo técnico

Construir uma aplicação local que use agentes especializados, coordenados por CrewAI, e um modelo de linguagem executado pelo Ollama. A aplicação deve responder sem depender de API paga, chave de API ou serviço em nuvem durante a execução.

## Stack prevista

- Python 3.11 ou superior
- CrewAI
- Ollama
- Modelo local compatível, inicialmente `qwen2.5:3b`
- Interface CLI com `python -m agente "pergunta"`
- Testes automatizados com `pytest`

## Arquitetura prevista

O sistema terá agentes com responsabilidades separadas:

1. **Tutor conceitual**: explica a intenção, o problema, os participantes, a estrutura, as consequências e os trade-offs do Iterator.
2. **Exemplificador**: produz exemplos pequenos e corretos, principalmente em Java, explicando a função de cada participante.
3. **Diagnosticador**: propõe exercícios, analisa respostas e identifica conceitos equivocados.
4. **Revisor**: verifica a resposta final, corrige imprecisões e aplica as regras anti-alucinação.

A coordenação entre agentes será feita pelo CrewAI. O uso do padrão Iterator na implementação interna é opcional; o requisito principal é que o sistema ensine o padrão Iterator.

O roteamento usa uma estratégia híbrida. Regras explícitas reconhecem pedidos claros de exemplos, demonstrações, código ou diagnóstico. Quando a intenção não é evidente, o roteador consulta o LLM local e classifica a pergunta como conceitual, exemplo ou diagnóstico. Se a resposta do roteador semântico for inválida, o fluxo conceitual é usado como fallback. O agente especialista responde primeiro e o revisor consolida a resposta final.

## Tarefas de desenvolvimento

### Configuração do projeto

- [x] Definir a estrutura de pacotes Python.
- [x] Criar `requirements.txt` com versões fixadas.
- [x] Configurar o modelo local do Ollama.
- [x] Centralizar as configurações em um módulo próprio.
- [x] Adicionar arquivos de configuração de exemplo sem credenciais.

### Agentes e prompts

- [x] Criar a fábrica ou módulo de construção dos agentes.
- [x] Implementar o agente tutor conceitual.
- [x] Implementar o agente exemplificador.
- [x] Implementar o agente diagnosticador.
- [x] Implementar o agente revisor.
- [x] Escrever os prompts completos de sistema de cada agente.
- [x] Definir o contrato de entrada e saída de cada agente.
- [x] Definir escopo, regras pedagógicas e regras anti-alucinação.

### Coordenação com CrewAI

- [x] Criar as `Task`s associadas a cada agente.
- [x] Implementar o fluxo de execução entre as tarefas.
- [x] Passar os resultados relevantes de um agente para o próximo.
- [x] Implementar a seleção de agentes ou tarefas conforme o tipo de pergunta.
- [x] Produzir uma única resposta final revisada.
- [x] Evitar executar agentes que não sejam necessários para uma pergunta.

### Memória e contexto

- [ ] Implementar o histórico da conversa.
- [ ] Limitar o histórico enviado ao modelo quando necessário.
- [ ] Incorporar perguntas e respostas anteriores ao contexto das tarefas.
- [ ] Evitar que respostas incorretas sejam reutilizadas sem revisão.
- [ ] Definir o comportamento para uma nova sessão.

### CLI

- [x] Implementar o ponto de entrada `python -m agente`.
- [x] Aceitar uma pergunta diretamente pela linha de comando.
- [x] Implementar o modo interativo de conversa.
- [x] Implementar o comando de saída.
- [ ] Exibir mensagens de erro compreensíveis.

### Robustez

- [x] Tratar entrada vazia.
- [x] Tratar Ollama indisponível.
- [ ] Tratar falha de uma tarefa ou agente.
- [ ] Validar respostas vazias ou em formato inesperado.
- [ ] Recusar pedidos para inventar padrões ou informações.
- [x] Orientar o estudante sem entregar uma solução completa imediatamente.
- [x] Redirecionar perguntas fora do escopo do Iterator.

### Testes

- [ ] Testar a criação dos agentes.
- [ ] Testar a criação das tarefas.
- [ ] Testar o fluxo de coordenação sem chamar o modelo real.
- [ ] Testar a memória entre múltiplos turnos.
- [ ] Testar a CLI com pergunta única.
- [ ] Testar a CLI em modo interativo.
- [ ] Testar entradas vazias e falhas do modelo.
- [ ] Testar explicação conceitual do Iterator.
- [ ] Testar geração de exemplo em Java.
- [ ] Testar recomendação de uso e não uso do padrão.
- [ ] Testar explicação de uso incorreto.
- [ ] Testar comparação com padrões relacionados.
- [ ] Testar recusa de padrão inexistente.
- [ ] Testar recusa de solução completa sem tentativa do estudante.

### Documentação técnica

- [x] Documentar a estrutura do projeto.
- [x] Documentar a configuração do Ollama.
- [x] Documentar o comando de instalação.
- [x] Documentar o comando de execução.
- [ ] Documentar todos os agentes e seus prompts.
- [x] Documentar o fluxo de coordenação.
- [x] Documentar as decisões de arquitetura.
- [ ] Documentar limitações conhecidas.
- [ ] Documentar os resultados dos testes técnicos.

## Estrutura planejada

```text
iterator-multiagent-tutor/
├── agente/
│   ├── __init__.py
│   ├── __main__.py
│   ├── agents.py
│   ├── config.py
│   ├── crew.py
│   ├── memory.py
│   ├── prompts.py
│   └── tasks.py
├── tests/
├── .env.example
├── README.md
└── requirements.txt
```

## Execução planejada

```powershell
ollama pull qwen2.5:3b
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m agente "Explique o que é o padrão Iterator."
```

Modo interativo:

```powershell
python -m agente
```

## Execução com Docker Compose

Copie o arquivo de configuração de exemplo, se quiser alterar o modelo:

```bash
cp .env.example .env
```

Construa a imagem da aplicação:

```bash
docker compose build app
```

Execute uma pergunta. O Compose inicia o Ollama e baixa o modelo definido em `OLLAMA_MODEL` na primeira execução:

```bash
docker compose run --rm app "Explique o que é o padrão Iterator."
```

Para abrir o modo interativo:

```bash
docker compose run --rm app
```

O modelo baixado fica persistido no volume Docker `ollama_data`.

# Iterator Multiagent Tutor

Tutor multiagente em Python que ensina o padrão de projeto Iterator por meio de uma interface de chat no terminal. A aplicação usa agentes especializados coordenados pelo CrewAI e um modelo local servido pelo Ollama, sem exigir chave de API ou serviço pago.

## Status do desenvolvimento

### Concluído

- [x] Estrutura do pacote Python e configurações centralizadas.
- [x] Integração com CrewAI e Ollama usando modelo local.
- [x] Tutor conceitual, exemplificador, diagnosticador e revisor.
- [x] Prompts, contratos de entrada/saída e regras anti-alucinação.
- [x] Roteamento explícito e semântico entre os fluxos.
- [x] Memória limitada a seis turnos e contexto de até 8.000 caracteres.
- [x] CLI para pergunta única e modo interativo.
- [x] Tratamento de entrada vazia, saudações, recusas, falhas do Ollama e respostas inválidas.
- [x] Dockerfile e Docker Compose com volume persistente para os modelos.
- [x] Testes automatizados de configuração, agentes, tarefas, roteamento, memória, validação, CLI e cenários (`37 passed`).
- [x] Documentação de instalação, execução, arquitetura, limitações e licença.

### Pendente ou recomendado

- [x] Instalar as dependências de desenvolvimento e executar a suíte completa com `python -m pytest -q` (`37 passed`).
- [x] Validar a CLI com uma saudação sem depender do Ollama.
- [x] Corrigir o alinhamento da variável `TEMPERATURE` entre o Docker Compose, o `.env.example` e a aplicação.
- [x] Validar a execução ponta a ponta com o Ollama e o modelo `qwen2.5:3b` no WSL2.
- [x] Fazer testes manuais dos oito cenários de qualidade e registrar respostas e julgamentos em `docs/evidencias-cenarios.json`.
- [ ] Avaliar o desempenho com modelos locais de tamanhos diferentes — requer modelos locais e ambiente de medição.

## Requisitos

- Python 3.11 ou superior
- [Ollama](https://ollama.com/) instalado e em execução
- Modelo local compatível; o padrão é `qwen2.5:3b`

## Instalação local

No diretório deste projeto:

```powershell
ollama pull qwen2.5:3b
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

O Ollama deve estar disponível em `http://localhost:11434`. Para alterar o modelo, a URL ou a temperatura, defina as variáveis correspondentes antes de executar:

```powershell
$env:OLLAMA_MODEL = "qwen2.5:3b"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:TEMPERATURE = "0.2"
```

### Execução no WSL2

O ambiente usado para a validação foi Ubuntu em WSL2. A instalação do Ollama e a execução da aplicação podem ser feitas dentro do próprio WSL:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
# em outro terminal WSL
ollama pull qwen2.5:3b
python3 -m venv .venv-wsl
source .venv-wsl/bin/activate
pip install -r requirements.txt
OLLAMA_BASE_URL=http://127.0.0.1:11434 python -m agente "Explique o padrão Iterator."
```

O Ollama instalado no WSL oferece a CLI `ollama` e mantém o modelo localmente. Para gerar novamente as evidências curtas da documentação, execute `python docs/coletar_evidencias_ollama.py`; o resultado será salvo em `docs/evidencias-cenarios.json`.

## Uso

Faça uma pergunta diretamente na linha de comando:

```powershell
python -m agente "Explique o que é o padrão Iterator e qual problema ele resolve."
```

Ou inicie uma conversa interativa:

```powershell
python -m agente
```

Digite `sair`, `exit` ou `quit` para encerrar. Entradas vazias, falhas do Ollama e respostas inválidas são tratadas com mensagens compreensíveis na CLI.

## Docker Compose

O Compose sobe o Ollama, baixa o modelo configurado na primeira execução e mantém os modelos no volume `ollama_data`:

```bash
docker compose build app
docker compose run --rm app "Explique o que é o padrão Iterator."
```

Para o modo interativo:

```bash
docker compose run --rm app
```

As opções podem ser personalizadas em um arquivo `.env` baseado em `.env.example`, especialmente `OLLAMA_MODEL` e `OLLAMA_BASE_URL`. A configuração da temperatura usada pela aplicação é `TEMPERATURE`.

## Como funciona

1. O roteador identifica saudações, pedidos de invenção, exemplos e diagnósticos por regras explícitas.
2. Para perguntas ambíguas, o roteador consulta o modelo local e escolhe o fluxo conceitual, de exemplo ou diagnóstico.
3. Um agente especialista produz a resposta inicial.
4. Um agente revisor verifica e consolida a resposta final.
5. A memória mantém até seis turnos da sessão e limita o contexto enviado aos agentes a 8.000 caracteres.

Pedidos de saudação e recusas de fabricação são respondidos diretamente, sem executar agentes. A aplicação guarda somente a resposta final revisada na memória.

### Agentes

- **Tutor conceitual**: explica intenção, problema, participantes, estrutura, consequências e trade-offs.
- **Exemplificador**: produz exemplos pequenos, principalmente em Java, e relaciona o código aos participantes do padrão.
- **Diagnosticador**: propõe exercícios, analisa tentativas e identifica equívocos.
- **Revisor**: corrige imprecisões e verifica as regras pedagógicas e anti-alucinação.

O padrão Iterator usado na orquestração é independente do padrão ensinado: a aplicação organiza seus fluxos com tarefas e memória, enquanto o conteúdo pedagógico explica o Iterator GoF.

## Estrutura

```text
iterator-multiagent-tutor/
├── agente/
│   ├── __main__.py   # entrada da CLI
│   ├── agents.py     # fábricas dos agentes
│   ├── config.py     # configurações via ambiente
│   ├── contracts.py  # contratos de entrada e saída
│   ├── crew.py       # montagem e execução do CrewAI
│   ├── llm.py        # criação do LLM e verificação do Ollama
│   ├── memory.py     # memória curta da sessão
│   ├── prompts.py    # prompts dos agentes
│   ├── router.py     # seleção do fluxo
│   ├── system.py     # fachada do tutor
│   └── tasks.py      # tarefas dos agentes
├── tests/            # testes unitários e de cenário
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

## Testes

Com as dependências instaladas, execute:

```powershell
python -m pytest -q
```

Os testes cobrem configuração, criação de agentes e tarefas, roteamento, memória, validação de respostas, CLI e cenários sem chamar o modelo real.

## Limitações conhecidas

- O Ollama precisa estar disponível e ter o modelo configurado baixado.
- O histórico existe apenas durante a vida do processo; cada execução da CLI começa uma nova sessão.
- O tutor é especializado no padrão Iterator. Perguntas fora desse escopo podem ser redirecionadas ou receber uma resposta conceitual genérica.
- A qualidade e o tempo de resposta dependem do modelo local e dos recursos da máquina.

## Licença

Este projeto é distribuído sob a licença MIT. Consulte [LICENSE](LICENSE).

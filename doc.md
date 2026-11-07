# Plano de desenvolvimento do Tutor Multiagent Iterator

Este arquivo e a fonte de verdade para o desenvolvimento do projeto. Toda implementacao deve seguir a arquitetura, as fases e a arvore de arquivos definidas aqui.

## Regra principal

Somente podem ser criados arquivos que estejam listados neste documento.

Se surgir necessidade de um arquivo, modulo, diretorio ou ferramenta que nao esteja listado aqui, a implementacao deve parar e solicitar autorizacao antes da criacao.

Arquivos gerados automaticamente, como `__pycache__`, arquivos temporarios, logs locais e volumes Docker, nao fazem parte do codigo-fonte e nao devem ser versionados.

## Objetivo do produto

Construir uma aplicacao local de chat que ensina o padrao de projeto Iterator por meio de agentes especializados coordenados pelo CrewAI.

O sistema deve:

- executar o modelo localmente pelo Ollama;
- nao depender de API paga ou chave de API;
- receber uma pergunta unica pela CLI;
- oferecer uma conversa interativa;
- usar agentes com responsabilidades distintas;
- manter memoria durante a sessao;
- tratar erros operacionais;
- aplicar regras anti-alucinacao;
- testar os cenarios pedagogicos do projeto.

O sistema ensina o padrao Iterator. O uso do padrao Iterator na implementacao interna nao e obrigatorio.

## Arquitetura

```text
CLI
agente/__main__.py
        |
        v
Servico da aplicacao
agente/system.py
        |
        +--> Memoria e contexto
        |    agente/memory.py
        |    agente/context.py
        |
        +--> Roteamento
        |    agente/router.py
        |
        +--> Tasks e coordenacao CrewAI
        |    agente/tasks.py
        |    agente/crew.py
        |
        +--> Agentes
        |    agente/agents.py
        |    agente/prompts.py
        |    agente/contracts.py
        |
        +--> Validacao e erros
             agente/validation.py
             agente/errors.py
                    |
                    v
             Modelo local via Ollama
             agente/config.py
             agente/llm.py
```

## Responsabilidade dos modulos

| Arquivo | Responsabilidade |
|---|---|
| `agente/__main__.py` | Entrada da CLI, pergunta unica, modo interativo e comando de saida. |
| `agente/system.py` | Caso de uso principal e integracao das camadas. Deve expor uma operacao como `answer(question)`. |
| `agente/config.py` | Leitura e validacao das configuracoes do ambiente. |
| `agente/llm.py` | Criacao do objeto LLM configurado para o Ollama. |
| `agente/agents.py` | Construcao dos quatro agentes CrewAI. |
| `agente/prompts.py` | Prompts de sistema completos e separados por agente. |
| `agente/contracts.py` | Estruturas de entrada, saida e resultados intermediarios. |
| `agente/tasks.py` | Criacao das Tasks CrewAI. |
| `agente/router.py` | Escolha do fluxo e dos agentes necessarios para cada pergunta. |
| `agente/crew.py` | Montagem e execucao da coordenacao entre Tasks e agentes. |
| `agente/memory.py` | Armazenamento do historico da sessao. |
| `agente/context.py` | Selecao e montagem do contexto enviado aos agentes. |
| `agente/validation.py` | Validacao de escopo, formato e regras anti-alucinacao. |
| `agente/errors.py` | Excecoes e mensagens de erro do dominio da aplicacao. |
| `tests/test_config.py` | Testes da configuracao e do LLM. |
| `tests/test_agents.py` | Testes de construcao e contratos dos agentes. |
| `tests/test_tasks.py` | Testes das Tasks sem chamada real ao modelo. |
| `tests/test_router.py` | Testes da escolha de fluxo. |
| `tests/test_memory.py` | Testes da memoria e selecao de contexto. |
| `tests/test_validation.py` | Testes das regras de validacao. |
| `tests/test_crew.py` | Testes da coordenacao com dependencias simuladas. |
| `tests/test_cli.py` | Testes dos modos de entrada e dos erros da CLI. |
| `tests/test_scenarios.py` | Testes dos cenarios pedagogicos do produto. |

## Arquivos ja existentes

Estes arquivos ja fazem parte do repositorio e podem ser atualizados conforme as fases:

- `AGENTS.md`
- `README.md`
- `LICENSE`
- `.gitignore`
- `.dockerignore`
- `.env.example`
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `agente/__init__.py`
- `agente/__main__.py`
- `agente/config.py`
- `agente/agents.py`
- `agente/prompts.py`
- `agente/system.py`
- `docs/plano-desenvolvimento-milestones.docx`

Nao criar uma segunda versao desses arquivos. Atualizar os arquivos existentes quando a fase exigir.

## Arquivos ainda a criar

Os seguintes arquivos sao os unicos novos arquivos de codigo previstos no plano:

- `agente/llm.py`
- `agente/contracts.py`
- `agente/tasks.py`
- `agente/router.py`
- `agente/crew.py`
- `agente/memory.py`
- `agente/context.py`
- `agente/validation.py`
- `agente/errors.py`
- `tests/test_config.py`
- `tests/test_agents.py`
- `tests/test_tasks.py`
- `tests/test_router.py`
- `tests/test_memory.py`
- `tests/test_validation.py`
- `tests/test_crew.py`
- `tests/test_cli.py`
- `tests/test_scenarios.py`

## Fases de desenvolvimento

### Fase 0 Fundacao

Arquivos envolvidos:

- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `.env.example`
- `agente/__main__.py`
- `agente/config.py`

Desenvolvimento:

- validar a construcao da imagem;
- validar as variaveis de ambiente;
- validar o entrypoint `python -m agente`;
- garantir que o projeto importe sem erro.

Fim da fase: o ambiente inicia e a imagem Docker e construida.

### Fase 1 Integracao do modelo local

Arquivos envolvidos:

- criar `agente/llm.py`;
- atualizar `agente/config.py`;
- atualizar `docker-compose.yml`;
- atualizar `.env.example`.

Desenvolvimento:

- criar o adaptador unico do Ollama;
- configurar modelo, URL e temperatura;
- manter o volume persistente do modelo;
- tratar Ollama indisponivel.

Fim da fase: uma chamada simples ao modelo funciona dentro do Compose.

### Fase 2 Contratos e agentes

Arquivos envolvidos:

- atualizar `agente/agents.py`;
- atualizar `agente/prompts.py`;
- criar `agente/contracts.py`.

Desenvolvimento:

- implementar o Tutor conceitual;
- implementar o Exemplificador;
- implementar o Diagnosticador;
- implementar o Revisor;
- definir contratos de entrada e saida;
- manter os prompts completos separados por agente.

Fim da fase: os quatro agentes sao instanciados sem chamada real ao modelo.

### Fase 3 Tasks e coordenacao

Arquivos envolvidos:

- criar `agente/tasks.py`;
- criar `agente/router.py`;
- criar `agente/crew.py`;
- atualizar `agente/system.py`.

Desenvolvimento:

- criar as Tasks do CrewAI;
- escolher o fluxo conforme a pergunta;
- executar apenas os agentes necessarios;
- passar resultados entre Tasks;
- consolidar a resposta final pelo Revisor.

Fim da fase: uma pergunta percorre um fluxo multiagente e retorna uma resposta final.

### Fase 4 Memoria e contexto

Arquivos envolvidos:

- criar `agente/memory.py`;
- criar `agente/context.py`;
- atualizar `agente/system.py`;
- atualizar `agente/tasks.py`.

Desenvolvimento:

- armazenar perguntas e respostas da sessao;
- limitar o historico enviado ao modelo;
- selecionar turnos relevantes;
- iniciar e limpar sessoes;
- evitar propagar resposta nao revisada como fato confiavel.

Fim da fase: uma conversa de varios turnos preserva contexto sem crescer indefinidamente.

### Fase 5 Validacao e confiabilidade

Arquivos envolvidos:

- criar `agente/validation.py`;
- criar `agente/errors.py`;
- atualizar `agente/prompts.py`;
- atualizar `agente/crew.py`.

Desenvolvimento:

- validar escopo da pergunta;
- recusar padroes inventados;
- responder com orientacao incremental a pedidos de solucao pronta;
- validar resposta vazia ou inesperada;
- tratar falha de agente e falha do modelo.

Fim da fase: os limites de confiabilidade estao implementados e testaveis.

### Fase 6 CLI e experiencia operacional

Arquivos envolvidos:

- atualizar `agente/__main__.py`;
- atualizar `agente/system.py`;
- atualizar `agente/errors.py`.

Desenvolvimento:

- suportar `python -m agente "pergunta"`;
- suportar modo interativo;
- tratar entrada vazia;
- oferecer comando de saida;
- exibir erros operacionais sem stack trace desnecessario.

Fim da fase: o contrato de CLI funciona em pergunta unica e conversa continua.

### Fase 7 Testes

Arquivos envolvidos:

- criar todos os arquivos em `tests/` listados neste documento;
- atualizar `requirements.txt` se uma dependencia de teste for necessaria.

Desenvolvimento:

- testar configuracao e agentes com mocks;
- testar Tasks, roteador, memoria e validacao;
- testar a CLI;
- testar o fluxo completo;
- testar os cenarios pedagogicos.

Fim da fase: os testes automatizados passam e cobrem os fluxos criticos.

### Fase 8 Release

Arquivos envolvidos:

- atualizar `README.md`;
- atualizar `Dockerfile`;
- atualizar `docker-compose.yml`;
- atualizar `requirements.txt`;
- atualizar `.gitignore` se necessario.

Desenvolvimento:

- documentar instalacao e execucao;
- validar o Compose em ambiente limpo;
- revisar dependencias e configuracoes;
- remover artefatos gerados;
- registrar limitacoes conhecidas;
- criar a versao de release.

Fim da fase: outra pessoa consegue construir e executar o produto seguindo o README.

## Ordem obrigatoria

```text
Fase 0
  -> Fase 1
  -> Fase 2
  -> Fase 3
  -> Fase 4 e Fase 5
  -> Fase 6
  -> Fase 7
  -> Fase 8
```

A Fase 4 e a Fase 5 dependem da coordenacao da Fase 3. A Fase 6 pode ser implementada em paralelo parcialmente, mas so deve ser considerada concluida depois da validacao da Fase 5.

## Regra para novas necessidades

Se uma implementacao exigir um arquivo que nao aparece neste documento, nao criar o arquivo automaticamente.

Antes, informar:

1. qual arquivo novo seria necessario;
2. qual responsabilidade ele teria;
3. por que os arquivos existentes nao sao suficientes;
4. em qual fase ele seria incluido.

A criacao so deve ocorrer depois da autorizacao do usuario e da atualizacao deste `doc.md`.

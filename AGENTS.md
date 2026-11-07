# Instruções do projeto

## Ambiente e comandos

- Usar WSL para executar comandos do projeto.
- Considerar `/mnt/c/Estudos/trabalho/iterator-multiagent-tutor` como o diretório do projeto no WSL.
- Usar o ambiente virtual Python do projeto quando ele existir.
- Preferir comandos reprodutíveis e não depender de configurações específicas do Windows.

## Escopo

- Trabalhar somente no sistema multiagente Tutor Iterator.
- Não alterar os PDFs, arquivos ou diretórios fora do repositório.
- Não adicionar conteúdo que não esteja relacionado ao desenvolvimento de software.

## Arquitetura

- Usar Python e CrewAI como framework de orquestração.
- Usar Ollama e um modelo local, sem API paga ou chave de API.
- Manter os agentes com responsabilidades separadas.
- Manter prompts, configuração, tarefas, memória, CLI e testes em módulos separados quando isso melhorar a organização.
- O padrão Iterator é o conteúdo ensinado pelo sistema; seu uso na implementação interna é opcional e deve ser justificado.

## Qualidade

- Tratar entrada vazia, falha do Ollama, falha de agente e resposta inválida.
- Não inventar padrões, participantes, consequências ou exemplos.
- Testar mudanças relevantes antes de concluir uma tarefa.
- Não modificar mudanças existentes sem verificar sua origem.

## Git

- Usar mensagens de commit objetivas e em português ou inglês consistente com o histórico.
- Verificar `git status` antes de modificar ou enviar arquivos.
- Não usar `git reset --hard`, `git checkout --` ou `git push --force` sem solicitação explícita.
- Enviar alterações para a branch `main` somente depois de validar o estado local.

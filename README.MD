## Minicurso de IA Generativa - STEPWISE
Este repositório contém o material de um **minicurso de IA generativa**, com o objetivo de introduzir conceitos, algoritmos e implementações práticas de modelos generativos. O curso abrange desde noções básicas de aprendizado de máquina até a implementação de redes neurais avançadas para geração de conteúdo.

## Objetivos do Minicurso
O objetivo principal é **capacitar os participantes** a compreender as técnicas que são utilizadas no processo de criação e produtização das LLMs e fornecer um contexto prático destes conceitos.

## Estrutura do Projeto
O repositório está organizado em pastas e arquivos que cobrem os seguintes tópicos:
1. ./rag: consiste no diretório que contém a aplicação de RAG no contexto das LLMs.
2. ./rotulos: trata-se do diretório destinado a aplicação das LLMs no contexto da resolução de um problema de classificação.
3. ./dist: alguns scripts opcionais criados para facilitar a instalação de certos requerimentos no **Windows**

## Público-Alvo
Este minicurso é voltado para **iniciantes a intermediários** em aprendizado de máquina, interessados em explorar IA generativa. Recomenda-se familiaridade com Python e conceitos básicos de estátistica e redes neurais.


## Adicionar instruções de RAG

## Instruções para solução de Rótulo
Para a solução de rótulos, primeiros passos:<br/>
- Instalar ollama
- Com Ollama instalado, abra um CMD e execute ``ollama pull llama3.2:1b``
- Após a instalação use ``ollama serve`` para abrir o servidor Ollama na porta **11434**, o endereço final fica: ``localhost:11434/``
> **Para os próximos passos não se esqueça de garantir que o terminal esteja aberto na pasta do projeto (No explorador de arquivos clique com o direito e selecione abrir no terminal)**
- Em um outro terminal execute o comando ``python -m venv venv`` para criar um ambiente virtual de desenvolvimento do Python
- Carregue o ambiente virtual usando o comando ``.\venv\Scripts\activate``
- Com o ambiente carregado use ``pip install -r requirements.txt``
- Execute o código rodando o comando ``python .\llm_rotulos_simples.py``

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
Este minicurso é voltado para **iniciantes a intermediários** em aprendizado de máquina, interessados em explorar IA generativa. Recomenda-se familiaridade com Python e conceitos básicos de estatística e redes neurais.

## Instruções para solução de Rótulo
- Baixe e instale o [ollama](https://ollama.com/)
- Com Ollama instalado, abra um CMD e execute ``ollama pull llama3.2:1b``
- Abra o CMD ou Terminal e execute o seguinte comando para fazer o pull do modelo: ollama pull [nomic-embed-text](https://huggingface.co/nomic-ai/nomic-embed-text-v1)
- Após o pull use ``ollama serve`` em um novo CMD para abrir o servidor Ollama na porta **11434**, o endereço final fica: ``localhost:11434/``
Para a solução de rótulos, primeiros passos:<br/>
> **Para estes passos não se esqueça de garantir que o terminal esteja aberto na pasta do projeto (No explorador de arquivos clique com o direito e selecione abrir no terminal), endereço do projeto: ``.\rotulos``**
- Em um outro terminal execute o comando ``python -m venv venv`` para criar um ambiente virtual de desenvolvimento do Python
- Carregue o ambiente virtual usando o comando ``.\venv\Scripts\activate``
- Com o ambiente carregado use ``pip install -r requirements.txt``
- Execute o código rodando o comando ``python .\llm_rotulos_simples.py``
- A solução cria um arquivo de saída chamado ``classificacao.csv`` a resposta da LLM fica na coluna ``sentiment_llama``
> **Nesta solução é interessante observar que a classificação da LLM local não é 100% precisa, isso é válido para qualquer LLM, então sempre que um trabalho com LLM necessita ser assertivo, é necessário incorporar validações mais rígidas (como scripts feitos com esse propósito) para evitar que erros atrapalhem a solução como um todo**
 
Continuando nesta análise, é possível utilizar uma segunda consulta à LLM para verificar a corretude das respostas recebidas na primeira consulta:
- No mesmo terminal que a solução anterior e no mesmo ambiente utilize o seguinte comando para executar o script de avaliação ``python .\llm_avalia_rotulos.py``
- A saída desta solução pode ser encontrada no arquivo ``avaliacao.csv``

## Instruções de RAG

> **Configurando o Ambiente no VSCode**
- Abra a pasta do projeto no VSCode 
- Instale as extensões oficiais para Python
- Crie um novo ambiente virtual: Pressione ``Ctrl+Shift+P`` e selecione ``Python: Create Environment``
- Se houver um arquivo ``requirements.txt`` no diretório, o VSCode mostrará uma opção para selecioná-lo. Isso instalará automaticamente as dependências
- Após a criação do ambiente, selecione o interpretador: Pressione ``Ctrl+Shift+P``, escolha ``Python: Select Interpreter`` e  selecione a versão do Python que está dentro do ``(venv)``
- Se o arquivo ``requirements.txt`` não tiver sido carregado, abra o terminal Pressionando ``Ctrl+"``, clique no botão de ``+`` e selecione Command Prompt
- Instale as dependências manualmente executando: ``pip install -r requirements.txt``

>**Configurando o Ambiente no Terminal**
- Em um outro terminal execute o comando ``python -m venv venv`` para criar um ambiente virtual de desenvolvimento do Python
- Carregue o ambiente virtual usando o comando ``.\venv\Scripts\activate``
- Com o ambiente carregado use ``pip install -r requirements.txt``

>**Carregando Novos Arquivos no Banco de Dados**
- Adicione novos arquivos à pasta ``rag/documentos/``
- Execute o arquivo ``rag/backend/chroma_db.py`` para atualizar o banco de dados com os novos documentos

>**Atualizando a Chave da API para o Groq AI**
- Dentro da pasta ``frontend`` do seu projeto ``rag``, crie uma nova pasta chamada ``.streamlit``
- Dentro da pasta ``.streamlit``, crie um arquivo chamado ``secrets.toml``
- Abra o arquivo ``secrets.toml`` e insira a [chave da API](https://groq.com/) fornecida pelo Groq. O conteúdo do arquivo deve ser:  ``groq_key='SUA_API_KEY'``
- Agora você pode acessar essa ``chave da API`` dentro do seu código Python usando o módulo streamlit.secrets. Exemplo: ``groq_key = st.secrets["groq"]["groq_key"]``

>**Inicializando o Servidor Flask (Backend)**
- Verifique e atualize os diretórios das pastas ``chroma``, ``documentos`` e outros caminhos relevantes no arquivo ``rag/backend/.env.paths``
- Execute o arquivo ``rag/backend/app.py`` para iniciar o servidor Flask

>**Inicializandoo Servidor streamlit(Frontend)**
- Em um novo terminal dedicado, execute o comando ``streamlit run rag/frontend/app.py --server.port 8080`` para iniciar o servidor streamlit na porta 8080


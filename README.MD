## Adicionar resumo

## Adicionar instruções de RAG

## Instruções para solução de Rótulo
Para a solução de rótulos, primeiros passos:<br/>
- Instalar ollama
- Com Ollama instalado, abra um CMD e execute ``ollama pull llama3.2:1b``
- Após a instalação use ``ollama serve`` para abrir o servidor Ollama na porta **11434**
> **Para os próximos passos não se esqueça de garantir que o terminal esteja aberto na pasta do projeto (No explorador de arquivos clique com o direito e selecione abrir no terminal)**
- Em um outro terminal execute o comando ``python -m venv venv`` para criar um ambiente virtual de desenvolvimento do Python
- Carregue o ambiente virtual usando o comando ``.\venv\Scripts\activate``
- Com o ambiente carregado use ``pip install -r requirements.txt``
- Execute o código rodando o comando ``python .\llm_rotulos_simples.py``

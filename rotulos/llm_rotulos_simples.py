from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import pandas as pd

NUM_MENSAGENS_CLASSIFICAR = 20

# Tradução:
# Classifique o sentimento do seguinte texto
template_muito_ruim = """
Classify the sentiment of the following text

Text:
{text}
"""

# Template de prompt ruim

# Tradução:
# Classifique o sentimento do seguinte texto em uma das seguintes categorias:
# positivo
# negativo
# neutro

template_ruim = """
Classify the sentiment of the following text into one of these categories:

positive
negative
neutral

Text:
{text}
"""

# Template de prompt simplificado

# Tradução:
# Classifique o sentimento do seguinte texto em uma das seguintes categorias:
# positivo, negativo ou neutro - (Apenas uma dessas)
# Retorne somente o nome da categoria, apenas uma palavra, sem adicionar novas linhas, espaços ou qualquer outro texto.

template = """
Classify the sentiment of the following text into one of these categories:

positive, negative or neutral - (Only one of these)

Return only the category name, just one word, without adding new lines, spaces, or any other text.

Text:
{text}
"""

#Alterar aqui a variável para mudar qual prompt usa
prompt = PromptTemplate.from_template(template=template)

# Função para consultar a LLM
def query_llm(message: str):
    chat = OllamaLLM(model="llama3.2:1b")
    chain = prompt | chat
    response = chain.invoke({"text": message}).strip().lower()
    print("Tweet: " + message + "  Classificacao: "+ response)
    return response

# Carregar o CSV
df = pd.read_csv('twitter_validation.csv')
df.columns = ["ID", "entity", "sentiment", "Tweet"]

# Limitar ao número de mensagens a serem classificadas
df_reduzido = df.head(NUM_MENSAGENS_CLASSIFICAR).copy()

# Função para limpar os tweets para melhorar a visualização
df_reduzido['Tweet'] = df_reduzido['Tweet'].apply(lambda tweet: tweet.strip().replace("\n",""))

# Função para aplicar o LLM ao tweet linha a linha
df_reduzido['sentiment_llama'] = df_reduzido['Tweet'].apply(lambda tweet: query_llm(tweet.replace("\n","")))

# Exportar resultado para CSV
df_reduzido.to_csv('classificacao.csv', index=False)

print("Classificação concluída e salva em 'classificacao.csv'")

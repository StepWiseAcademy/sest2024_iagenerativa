from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import pandas as pd

NUM_MENSAGENS_CLASSIFICAR = 20

template_ruim = """
Classify the sentiment of the following text into one of these categories:

positive
negative
neutral

Text:
{text}
"""

# Template de prompt simplificado
template = """
Classify the sentiment of the following text into one of these categories:

positive, negative or neutral - (Only one of these)

Return only the category name, just one word, without adding new lines, spaces, or any other text.

Text:
{text}
"""
prompt = PromptTemplate.from_template(template=template)

# Função para query no LLM
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

# Função para aplicar o LLM ao tweet
df_reduzido['sentiment_llama'] = df_reduzido['Tweet'].apply(lambda tweet: query_llm(tweet.replace("\n", "")))

# Exportar resultado para CSV
df_reduzido.to_csv('classificacao.csv', index=False)

print("Classificação concluída e salva em 'classificacao.csv'")

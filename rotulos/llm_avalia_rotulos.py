from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import pandas as pd

#Template feita para uma LLM verificar a análise de sentimentos
template = """
Your task is to verify the sentiment classification of the following text. You will receive a tweet and its classified sentiment (positive, negative, or neutral). Your job is to confirm if the sentiment classification matches the content of the tweet.

Classify the sentiment of the tweet again based on the same categories:

positive, negative, or neutral (Only one of these)

Return only one of these three words, without any additional text, new lines, or spaces.

If the classification matches, return "True" If it doesn’t match, return "False", only one word with no spaces or line-breaks.

Text:
{text}

Classification:
{classification}
"""
prompt = PromptTemplate.from_template(template=template)

# Função para consultar a LLM
def query_llm(message: str,sentiment: str):
    chat = OllamaLLM(model="llama3.2:1b")
    chain = prompt | chat
    response = chain.invoke({"text": message,"classification": sentiment}).strip().lower()
    print("Tweet: " + message + "  Classificacao: "+ sentiment + " Avaliação: " + response)
    return response

# Carregar o CSV
df = pd.read_csv('classificacao.csv')
df.columns = ["ID", "entity", "sentiment", "Tweet","sentiment_llama"]

#Aplica a função de LLM lendo linha a linha juntando as duas colunas, Tweet e sentiment_llama
df['is_correct'] = df.apply(lambda row: query_llm(row['Tweet'], row['sentiment_llama']), axis=1)

# Exportar resultado para CSV
df.to_csv('avaliacao.csv', index=False)

print("Classificação concluída e salva em 'avaliacao.csv'")
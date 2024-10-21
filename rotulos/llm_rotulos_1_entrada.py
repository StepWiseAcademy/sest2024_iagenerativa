import ofxparse
import pandas as pd
import os
from datetime import datetime
import time
import multiprocessing
from functools import wraps
 
# Decorador para executar a função em paralelo usando o número máximo de CPUs
#def parallelize_on_max_processors(func):
#    @wraps(func)
#    def wrapper(*args, **kwargs):
#        # Obtém o número de CPUs disponíveis
#        num_processors = multiprocessing.cpu_count()
# 
#        # Cria um Pool com o número máximo de processos
#        with multiprocessing.Pool(processes=num_processors) as pool:
#            # Executa a função fornecida no número máximo de CPUs
#            results = pool.starmap(func, args[0])
# 
#        return results
#    return wrapper

#df = pd.DataFrame()
#
#for extrato in os.listdir("extratos"):
#    with open(f'extratos/{extrato}', encoding='ISO-8859-1') as ofx_file:
#        ofx = ofxparse.OfxParser.parse(ofx_file)
#    
#    transactions_data = []
#    for account in ofx.accounts:
#        for transaction in account.statement.transactions:
#            transactions_data.append({
#                "Data": transaction.date,
#                "Valor": transaction.amount,
#                "Descrição": transaction.memo,
#                "ID": transaction.id,
#            })
#    
#    df_temp = pd.DataFrame(transactions_data)
#    df_temp["Valor"] = df_temp["Valor"].astype(float)
#    df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())
#    df = pd.concat([df,df_temp])
#    df["Valor"] = 1

df = pd.read_csv("C:/Desenvolvimento/LLM-Local-Rotulo-Produtos/dados/tribanco/AMOSTRA_LLM.csv", sep=";")

# LLM
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_community.llms.ollama import Ollama

_ = load_dotenv(find_dotenv())

template = """
Você é um analista de dados, trabalhando em um projeto de categorização de dados em Português do Brasil.
Seu trabalho é escolher a categoria mais adequada para a descrição do produto
que vou te enviar.

Todos são produtos que dever ser categorizados em Português do Brasil.

Escolha uma dentre as seguintes categorias:
- ACESSORIOS
- ACUCAR
- AGUA
- ARROZ
- BEBIDA
- BOLACHA
- CAFE
- CALDOS
- CARNE
- CHOCOLATE
- CREME
- DOCES
- EMBUTIDOS
- FARINHA
- FEIJAO
- HIGIENE
- HORTALICAS
- IOGURTE
- LATICINIOS
- LIMPEZA
- MACARRAO
- MISTURA
- MOLHO
- OLEO
- OUTRO
- PADARIA
- PAPEL
- PETS
- SAL
- SALGADINHO
- SALGADOS
- SUCO
- TEMPERO
- VINHO

Escolha a categoria deste item:
{text}

Responda apenas com a categoria, em português, ou seja uma unica palavra, não crie nenhuma categoria nova além das que foram informadas, não pule linha e nem espaço antes ou depois da palavra. 
"""

prompt = PromptTemplate.from_template(template=template)
#chat = Ollama(model="llama3:70b", base_url="https://203.154.134.52:31681", headers={"Authorization": f"Bearer 9f0dbf882bd247238dffed9fc232570ac4fdab8f71aaf7573efa66d6f086dbe8"}) 
#chat = Ollama(model="mistral")
chat = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | chat

#chain.invoke("Farmácias DrogaRaia 03/09")

#categorias = chain.batch(list(df["Descricao"].values))
#df["Categoria_Llama"] = categorias

#df.to_csv("C:/Desenvolvimento/LLM-Local-Rotulo-Produtos/finances_llama3_405b.csv", sep= ";", encoding="ISO-8859-1", index=False)

category = []
for transaction in list(df["Descricao"].values):
    start_time = time.time()  # Marca o tempo de início
    aux_category = [chain.invoke(transaction).content]
    end_time = time.time()  # Marca o tempo de término
    elapsed_time = end_time - start_time  # Calcula o tempo decorrido
    category += aux_category
    print(f'Descrição: {transaction} / Categoria: {aux_category} / Tempo: {elapsed_time} seg')

df["Categoria_GPT"] = category
df.to_csv("C:/Desenvolvimento/LLM-Local-Rotulo-Produtos/gpr4mini_amostra10k.csv", sep= ";", encoding="ISO-8859-1", index=False)

### Rodando localmente
#https://vast.ai/ #Crie e alugue máquinas para processamento, escolhe a configuração
#É montada uma máquina para nós e conseguimos conectar como se fosse um servidor


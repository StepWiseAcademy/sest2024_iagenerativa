import argparse
import asyncio
from flask import Flask, request, jsonify, Response
from flask_cors import CORS  # Importe o CORS aqui
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Responda a pergunta usando apenas o contexto abaixo:

{context}

---
 
Responda a pergunta apenas considerando o contexto provido, não mencione que você leu o contexto, apenas o conteúdo, seja conciso e responda sempre em português por favor: {question}
"""

app = Flask(__name__)
CORS(app)  # Adicione o CORS aqui

@app.route('/query', methods=['POST'])
def query_endpoint():
    data = request.json
    query_text = data.get('query_text')
    if not query_text:
        return jsonify({"error": "Missing query_text parameter"}), 400
    
    # Function to handle the async streaming and yield to the response
    def stream_query_sync():
        async def stream_query_async():
            async for chunk in query_async_rag(query_text):
                yield chunk

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async_gen = stream_query_async()
        try:
            while True:
                chunk = loop.run_until_complete(async_gen.__anext__())
                yield chunk
        except StopAsyncIteration:
            pass
        finally:
            loop.close()
    
    # Return a streaming response
    return Response(stream_query_sync(), content_type='text/plain')

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    asyncio.run(query_async_rag(query_text))


async def query_async_rag(query_text):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(context_text)
    model = Ollama(model="mistral")
    async for chunk in model.astream(prompt):
        yield chunk

if __name__ == "__main__":
    app.run(debug=True, port=5000)

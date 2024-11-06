from flask import Flask, request, jsonify, Response
from flask_cors import CORS  

from chroma_db import get_top5

app = Flask(__name__)
CORS(app) 

def simple_prompt_template(role:str, context:list[str], instructions:str, question:str)-> str:

    context_text = '\n'.join([chunck.replace('\n', '') for chunck in context])

    p = f'''
 
        Now you are {role}. you must answer the questions using your prior knowledge and the context provided, following the instructions.

        Context: "{context_text}"

        Questions: "{question}"

        Instructions: "{instructions}"
    '''

    return p

@app.route('/top5', methods=['POST'])
def retrive_top5():

    data = request.json
    query_text = data.get('query_text')

    if not query_text:
        return jsonify({"error": "Missing query_text parameter"}), 400

    return jsonify(
        chunks=get_top5(query_text)
    )

@app.route('/rag', methods=['POST'])
def rag():
    data = request.json
    query_text = data.get('query_text')

    if not query_text:
        return jsonify({"error": "Missing query_text parameter"}), 400
    
    chunks = get_top5(query_text)
    
    prompt = simple_prompt_template(
        role='a machine learning engineer especialized in large language models',
        context=chunks,
        question=query_text,
        instructions="Answer the question using the context when necessary, don't use words like 'appears' and don't make direct references to the context."
    )

    return jsonify(
        prompt=prompt,
        chunks=get_top5(query_text)
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
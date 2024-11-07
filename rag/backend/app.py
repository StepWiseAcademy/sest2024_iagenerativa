from flask import Flask, request, jsonify, Response
from flask_cors import CORS  

from chroma_db import get_topN

app = Flask(__name__)
CORS(app) 

def simple_prompt_template(role:str, context:list[str], instructions:str, question:str, language:str)-> str:

    context_text = '\n'.join([chunck.replace('\n', '') for chunck in context])
    p = ''

    match(language):
        case 'pt':
            p = f'''
        
                Agora o seu papel é de {role}. Você deve responder a questão usando seus conhecimentos e o contexto fornecido, seguindo as intruções passadas.

                Contexto: "{context_text}"

                Questão: "{question}"

                Instruções: "{instructions}"
            '''

        case 'en':
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
        chunks=get_topN(query_text, n=2)
    )

@app.route('/rag', methods=['POST'])
def rag():
    data = request.json
    query_text = data.get('query_text')

    if not query_text:
        return jsonify({"error": "Missing query_text parameter"}), 400
    
    chunks = get_topN(query_text)
    
    #prompt = simple_prompt_template(
    #    role='a machine learning engineer especialized in large language models',
    #    context=chunks,
    #    question=query_text,
    #    instructions="Answer the question using the context when necessary, don't use words like 'appears' and don't make direct references to the context.",
    #    language='pt'
    #)

    prompt = simple_prompt_template(
        role='um professor assistente no curso de estatística e está tirando dúvidas sobre a técnicas de amostragem.',
        context=chunks,
        question=query_text,
        instructions='Responda em Português do Brasil, não use palavras como acho e penso, evite copiar os textos do contexto e seja sucinto.',
        language='pt'
    )

    return jsonify(
        prompt=prompt,
        chunks=get_topN(query_text)
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)

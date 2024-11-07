import streamlit as st

import sys
from streamlit.web import cli

from groq import Client
from typing import Generator
import requests

groq_api_key =  st.secrets["groq_key"]
client = Client(api_key=groq_api_key)


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:

    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

st.markdown(
    """
    <style>
        .stMainBlockContainer{
            overflow: hidden;
            padding-left:0;
            padding-top:2rem;
            min-width:90%;
            min-height:80%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializando as variaveis da página

if 'model' not in st.session_state:
    st.session_state['model'] = 'llama3-8b-8192'

if 'messages' not in st.session_state:
    st.session_state.messages=[]

if 'rag_rank_top5' not in st.session_state:
    st.session_state.rag_rank_top5=[]

# Divide a tela em duas colunas iguais
col1, col2 = st.columns(2)

with col2:

    
    st.header("Rag")

    rank_container = st.container(height=420)
    rank_container.markdown(
            """
                <style>
                    !padding-top:10rem;
                </style>
            """,
            unsafe_allow_html=True
        )    

    with rank_container:

        rag_container = st.container(height=400, border=False)
        rag_container.markdown(
            """
                <style>
                    margin-top:2rem;
                </style>
            """,
            unsafe_allow_html=True
        )

with col1:

    c1, c2 = st.columns(2)

    with c1:
        st.header("Assistente de Pesquisa")

    with c2:

        st.session_state['model'] = st.selectbox(
            "",
            ('llama3-8b-8192', 'gemma2-9b-it', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768'),
        )

    with st.container(height=420):

        chat_container = st.container(height=330)

        with chat_container:
            if st.session_state.messages == []:
                with st.chat_message('assistant'):
                    st.markdown('Olá, como posso ajudar?')
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input('Faça uma pergunta para o nosso assistente', key='prompt'):

            st.session_state.messages.append({'role':'user', 'content':prompt})

            with chat_container:

                with st.chat_message('user'):
                    st.markdown(prompt)
            
                with rag_container:

                    response = requests.post('http://127.0.0.1:5000/rag', json={'query_text':prompt})

                    if response.status_code == 200: 
                            
                        for chunk in response.json()['chunks']:
                            st.markdown("- "+chunk)
                    
                with st.chat_message('assistant'):

                    stream = client.chat.completions.create(
                        model=st.session_state['model'],
                        messages=[
                            {
                                'role': m['role'],
                                'content': response.json()['prompt']
                            } for m in st.session_state.messages
                        ],
                        stream=True
                    )

                    chat_responses_generator = generate_chat_responses(stream)
                    response = st.write_stream(chat_responses_generator)
            
            st.session_state.messages.append({'role':'assistant', 'content': response})



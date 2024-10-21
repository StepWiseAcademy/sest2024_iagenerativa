from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Resposta Esperada: {expected_response}
Resposta Dada: {actual_response}
---
(Responda com 'true' ou 'false') A Resposta Dada é equivalente a Resposta Esperada? 
"""


def Test_dnd():
    assert query_and_validate(
        question="Faça um resumo dos dados cadastrais da pessoa",
        expected_response="",
    )


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
    
Test_dnd()
import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from isgoodrite.process_answer import ModelResponse


def get_model(default_model, model_temperature=0):
    model_name = os.getenv('IS_GOOD_MODEL', default_model)
    print(f'Using model {model_name}')
    return ChatOllama(
        model=model_name,
        temperature=model_temperature,
        base_url="http://localhost:11434"
    )

def prompt_model(llm, input):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert senior software developer. Your task is to validate, improve and generate code.",
            ),
            ("human", "{input}"),
        ]
    )
    chain = prompt | llm
    ai_message = chain.invoke(
        {
            "input": f"{input}",
        }
    )
    return ai_message.content

def query_llm_for_validation(file_name, file_content, model_name, description):
    llm = get_model(model_name)
    if not description:
        description = "Review and validate it for me please"
    answer = prompt_model(llm, input=f"I have code in a file named {file_name}. {description}: \n {file_content}")
    return ModelResponse(answer)

def query_llm_for_generation(model_name, file_name, description):
    llm = get_model(model_name)
    if not description or description == "":
        description = "Please create a Hello World script but instead of the script printing Hello World please print a joke about programming."
    answer = prompt_model(llm, input=f"{description} \n The file with the code will be named: {file_name}")
    return ModelResponse(answer)

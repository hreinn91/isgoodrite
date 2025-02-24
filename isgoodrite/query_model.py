import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

def get_model(default_model, model_temperature=0):
    model_name = os.getenv('IS_GOOD_MODEL', default_model)
    print(f'Using model {model_name}')
    return ChatOllama(
        model=model_name,
        temperature=model_temperature
    )

def prompt_model(llm, input, language='Python'):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert {programming_language} programmer. Your task is to validate and generate code.",
            ),
            ("human", "{input}"),
        ]
    )
    chain = prompt | llm
    ai_message = chain.invoke(
        {
            "programming_language": f"{language}",
            "input": f"{input}",
        }
    )
    return ai_message.content

def query_llm(file_name, file_content):
    default_model_name = "qwen2.5-coder:0.5b"
    llm = get_model(default_model_name)
    return prompt_model(llm, input=f"I have code in a file named {file_name}, please review it for me please: \n {file_content}")

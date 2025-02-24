import sys

from isgoodrite.query_model import query_llm
from isgoodrite.process_answer import ModelResponse


def read_file(file_name):
    try:
        with open(file_name) as f:
            return f.read()
    except IOError as _:
        print(f"No such file: {file_name}")
    pass

def write_file(original_file_name):
    pass

def main():
    args = sys.argv[1:]
    model_responses = []
    for file_name in args:
        file_content = read_file(file_name)
        answer = query_llm(file_name, file_content)
        model_responses.append(ModelResponse(answer))



if __name__ == '__main__':
    main()



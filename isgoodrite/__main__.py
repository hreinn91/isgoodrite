import sys
import subprocess
import os

from isgoodrite.query_model import query_llm
from isgoodrite.process_answer import ModelResponse


def read_file(file_name):
    try:
        with open(file_name) as f:
            return f.read()
    except IOError as _:
        print(f"No such file: {file_name}")
    pass

def get_copy_name(original_file_name):
    if '.' not in original_file_name:
        return original_file_name + "-copy"
    file_name_split = original_file_name.split('.')[:-1]
    name = file_name_split[-1]
    copy_name = file_name_split[-1] + "-copy"
    if name == "" or '.' not  in original_file_name:
        return original_file_name + "-copy"
    return original_file_name.replace(name, copy_name)

def write_file(original_file_name, file_content):
    copy_file_name = get_copy_name(original_file_name)
    print(f"Writing suggestion to: {copy_file_name}")
    with open(copy_file_name, 'w+') as f:
        f.write(file_content)
    return copy_file_name

def main():
    file_name = sys.argv[1]
    file_content = read_file(file_name)
    answer = query_llm(file_name, file_content)
    model_response = ModelResponse(answer)
    copy_file_name = write_file(file_name, model_response.code)

    subprocess.call(f"diff -u {file_name} {copy_file_name} | diff-so-fancy", shell=True)
    try:
        os.remove(copy_file_name)
    except OSError:
        print(f"Failed to clean up copy file {copy_file_name}")
        pass


if __name__ == '__main__':
    main()



import subprocess
import os
import argparse

from isgoodrite.query_model import query_llm
from isgoodrite.process_answer import ModelResponse
from isgoodrite.config import DEFAULT_CONFIG


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
    if name == "" or '.' not in original_file_name:
        return original_file_name + "-copy"
    return original_file_name.replace(name, copy_name)


def write_file(file_name, file_content):
    print(f"Writing suggestion to: {file_name}")
    with open(file_name, 'w+') as f:
        f.write(file_content)
    return file_name


def remove_file(copy_file_name):
    try:
        os.remove(copy_file_name)
        print(f'Removed file {copy_file_name}')
    except OSError:
        pass


def handle_args():
    parser = argparse.ArgumentParser(
        description="isgoodrite: the simple command line tool for validating your scripts using a local llm with ollama.\n"
                    "isgoodrite works best with qwen2.5-coder models.\n"
                    "example: isgoodrite remove_duplicates.py -d --description \"Please add a unit test\"",
        usage="isgoodrite FILE [OPTIONS]"
    )
    parser.add_argument('file', metavar='FILE', type=str, help='File to process')
    parser.add_argument('-d', '--diff-fancy', action='store_true',
                        help='Use diff-so-fancy for displaying differences',
                        default=DEFAULT_CONFIG["DIFF_SO_FANCY_ENABLED"])
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Removes the copy file after running the step. Typically used with --diff-so-fancy')
    parser.add_argument('-m', '--model', type=str,
                        help=f'Specify which LLM model to use (default: {DEFAULT_CONFIG["DEFAULT_MODEL"]})',
                        default=DEFAULT_CONFIG["DEFAULT_MODEL"])
    parser.add_argument('--description', nargs='*',
                        help='Free text description of what to improve (e.g., "Make sure to add unit tests")',
                        default=None)
    return parser.parse_args()


def main():
    args = handle_args()
    description = None
    if args.description:
        description = ''.join(args.description)

    file_name = args.file
    file_content = read_file(file_name)

    answer = query_llm(file_name, file_content, args.model, description)
    model_response = ModelResponse(answer)
    copy_file_name = get_copy_name(file_name)
    remove_file(copy_file_name)
    write_file(copy_file_name, model_response.code)

    if args.diff_fancy:
        subprocess.call(f"diff -u {file_name} {copy_file_name} | diff-so-fancy", shell=True)
    if args.clean:
        remove_file(copy_file_name)


if __name__ == '__main__':
    main()

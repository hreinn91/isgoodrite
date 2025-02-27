import subprocess
import os
import argparse

from isgoodrite.query_model import query_llm_for_validation, query_llm_for_generation
from isgoodrite.config import DEFAULT_CONFIG


def read_file(file_name):
    try:
        with open(file_name) as f:
            return f.read()
    except IOError as _:
        return None
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
                    "example: isgoodrite remove_duplicates.py -f --description \"Please add a unit test\"",
        usage="isgoodrite FILE [OPTIONS]"
    )
    parser.add_argument('file', metavar='INPUT', type=str,
                        help='The INPUT can either be an existing file which isgoodrite will review and validate for you '
                             'or if the INPUT file does not exist then isgoodrite will write its output to a file with name INPUT given the description.')
    parser.add_argument('-f', '--diff-fancy', action='store_true',
                        help='Use diff-so-fancy for displaying differences',
                        default=DEFAULT_CONFIG["DIFF_SO_FANCY_ENABLED"])
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Removes the copy file after running the step. Typically used with --diff-so-fancy')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print the whole response from the LLM')
    parser.add_argument('-p', '--print', action='store_true',
                        help='Print the content of the output file.')
    parser.add_argument('--bat', action='store_true',
                        help='BAT: Print the content of the output file with bat.')
    parser.add_argument('-m', '--model', type=str,
                        help=f'Specify which LLM model to use (default: {DEFAULT_CONFIG["DEFAULT_MODEL"]})',
                        default=DEFAULT_CONFIG["DEFAULT_MODEL"])
    parser.add_argument('-d', '--description', nargs='*',
                        help='Free text description of what to improve (e.g., "Make sure to add unit tests")',
                        default=None)
    return parser.parse_args(), parser


def main():
    args, parser = handle_args()
    description = None
    if args.description:
        description = ''.join(args.description)

    file_name = args.file
    file_content = read_file(file_name)

    if file_content is None:
        output_file_name = file_name
        model_response = query_llm_for_generation(args.model, description)
    else:
        model_response = query_llm_for_validation(file_name, file_content, args.model, description)
        output_file_name = get_copy_name(file_name)
        remove_file(output_file_name)

    if args.verbose:
        print(model_response.description)

    write_file(output_file_name, model_response.code)

    if args.diff_fancy:
        subprocess.call(f"diff -u {file_name} {output_file_name} | diff-so-fancy", shell=True)
    if args.bat:
        subprocess.call(f"bat {file_name}", shell=True)
    if args.print:
        print(read_file(output_file_name))
    if args.clean:
        remove_file(output_file_name)


if __name__ == '__main__':
    main()

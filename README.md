# IS GOOD RITE?!!

`isgoodrite` is a simple command line tool which integrates with a local running ollama.
Use your local ollama to validate your scripts and code using `isgoodrite`.

<img src="demo.gif" width="500" />

## SETUP

Setup this tool by installing it with:

    ollama pull qwen2.5-coder:3b
    pip install -r requirements.txt
    pip install -e .


## HOW IT WORKS

`isgoodrite` takes a scripts as an input and writes an improved script as a copy of the input file.

## Example

    isgoodrite remove_duplicates.py -d --description "Please add a unit test"

or with python

    python -m isgoodrite remove_duplicates.py --description "Check for any syntax errors please"

## INTEGRATE WITH DIFF-SO-FANCY

https://github.com/so-fancy/diff-so-fancy

`diff-so-fancy`is a great tool for making diffs human-readable. 

Integrate `isgoodrite` with diff-so-fancy, all you need is the `diff-so-fancy` binary in your path and the good old `diff`.  


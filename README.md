# IS GOOD RITE?!!

`isgoodrite` is a simple command line tool which integrates with a local running ollama.
Use your local ollama to validate your scripts and code using `isgoodrite`.

**Generate New Scripts:**

<img src="demo_validate.gif" width="800" />


**Validate your existing scripts:**

<img src="demo_generate.gif" width="800" />

...



## SETUP

Setup this tool by installing it with:

    ollama pull qwen2.5-coder:3b
    pip install -r requirements.txt
    pip install -e .

Make sure to check the `isgoodrite/config.py` and the `OLLAMA_BASE_URL` config. 
For most the local OLLAMA will be running on "http://localhost:11434" which is the current default. 
This can be changed if you are serving your models on some other url. 


## HOW IT WORKS

`isgoodrite` takes a scripts as an input and writes an improved script as a copy of the input file.

## Example

Validate your existing Scripts

    isgoodrite remove_duplicates.py -f --description "Please add a unit test"

or

    python -m isgoodrite remove_duplicates.py --description "Check for any syntax errors please"

Create a new script

    isgoodrite fibonacci_sequence.py --description "Please write a python script with a function that generates a fiboncacci sequence."

### INTEGRATE WITH DIFF-SO-FANCY

https://github.com/so-fancy/diff-so-fancy

`diff-so-fancy`is a great tool for making diffs human-readable. 

Integrate `isgoodrite` with diff-so-fancy, all you need is the `diff-so-fancy` binary in your env and the good old `diff`.  


### INTEGRATE WITH BAT

https://github.com/sharkdp/bat

`bat` A cat(1) clone with syntax highlighting. 

Integrate `isgoodrite` with BAT, all you need is the `bat` binary in your env.  


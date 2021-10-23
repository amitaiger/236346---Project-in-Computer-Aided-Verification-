import subprocess
import json
from flask import Flask
from flask import request
from os import listdir
from os.path import isfile, join
from flask.templating import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return open('index.html').read()

@app.route("/benchmarks")
def list_benchmarks():
    benchmark_path = "../benchmarks/c"
    raw_list = [f for f in listdir(benchmark_path) if isfile(join(benchmark_path, f))]
    benchmark_list = []
    for filename in raw_list:
        if filename.endswith(".c"):
            benchmark_list.append(filename)
    return json.dumps(benchmark_list)

@app.route("/verify", methods = ['GET', 'POST'])
def verify():
    program_code = "Please enter code."
    if request.method == 'POST':
        program_code = request.get_json()['code']
    code_file = open("temp", "w")
    code_file.write(program_code)
    code_file.close() 
    run_program = "node ../ext/sindarin.js parse temp > junk && mv temp.ast.json ../benchmarks/c/json && python -u ../main.py"
    p = subprocess.run(run_program, stdout=subprocess.PIPE, shell=True)
    return p.stdout

@app.route("/loadbenchmark", methods = ['GET', 'POST'])
def load_benchmark():
    benchmark_code = "No benchmark by that name."
    if request.method == 'POST':
        benchmark_name = request.get_json()['name']
    if (not "\n" in benchmark_name):
        if isfile("../benchmarks/c/"+benchmark_name):
            with open("../benchmarks/c/"+benchmark_name,"r") as f:
                benchmark_code = f.read()
    return benchmark_code

@app.route("/welcome")
def welcome():
    return "Welcome! Enter either benchmark name or your own code."

import CodeMirror from 'codemirror';
import 'codemirror/lib/codemirror.css';
import './index.css';


class IDE {
    panels: {
        benchmarks: HTMLDivElement,
        editor: HTMLDivElement,
        output: HTMLDivElement
    }
    cm: CodeMirror.Editor

    constructor() {
        this.panels = {
            benchmarks: document.querySelector('#panel-benchmarks'),
            editor: document.querySelector('#panel-editor'),
            output: document.querySelector('#panel-output')
        };

        this.cm = CodeMirror(this.panels.editor, {
            lineNumbers: true
        });

        this.panels.output.querySelector('button')
            .addEventListener('click', () => this.runVerifier());
		
		this.panels.benchmarks.querySelector('button')
            .addEventListener('click', () => this.loadBenchmark());
    }

    async open(uri: string) {
        var text = await (await fetch(uri)).text(),
            doc = new CodeMirror.Doc(text);
        this.cm.swapDoc(doc);
    }

    async runVerifier() {
		var program_code = this.cm.getValue();
		var out = await (await fetch ('/verify' , {
			method: "POST",
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({'code': program_code})
		})).text();
        this.panels.output.querySelector('#output').textContent = out;
    }

    async listBenchmarks() {
        var ul = this.panels.benchmarks.querySelector('#benchmarks'),
            items = await (await fetch('/benchmarks')).json();
        for (let item of items) {
            var li = document.createElement('li');
            li.textContent = item;
            ul.append(li);
        }
    }
	
	async loadBenchmark() {
		var benchmark_name = this.cm.getValue();
		var out = await (await fetch ('/loadbenchmark' , {
			method: "POST",
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({'name': benchmark_name})
		})).text();
		var doc = new CodeMirror.Doc(out);
		this.cm.swapDoc(doc);
	}
}


function main() {
    var ide = new IDE;
    ide.listBenchmarks();
    ide.cm.focus();
    ide.open('/welcome');
    Object.assign(window, {ide});
}


document.addEventListener('DOMContentLoaded', main);
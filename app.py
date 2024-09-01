from flask import Flask, render_template, request, jsonify
import subprocess
import os
import platform

app = Flask(__name__)

def get_base_directory():
    system = platform.system()
    if system == 'Linux' or system == 'Darwin':
        base_directory = os.path.expanduser('~')
    else:
        base_directory = '/'
    return base_directory

base_directory = get_base_directory()
current_directory = base_directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    global current_directory
    data = request.json
    command = data.get('command')

    if command.startswith('cd '):
        path = command[3:].strip()
        new_directory = os.path.join(current_directory, path)
        if os.path.isdir(new_directory):
            current_directory = os.path.abspath(new_directory)
            output = f"\r"
        else:
            output = f"cd: no such file or directory: {path}"
    elif command == 'clear':
        output = 'CLEAR'
    else:
        try:
            result = subprocess.run(command, shell=True, cwd=current_directory, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout if result.stdout else result.stderr
        except subprocess.CalledProcessError as e:
            output = e.stderr

    return jsonify({'output': output, 'current_directory': current_directory})

if __name__ == '__main__':
    app.run(debug=True)
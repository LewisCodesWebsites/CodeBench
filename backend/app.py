import os
import tempfile
import subprocess
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='../frontend')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json(force=True)
    language = data.get('language')
    code = data.get('code', '')
    input_data = data.get('input', '')
    expected_output = data.get('expected_output', None)

    if language not in {'python', 'c', 'javascript'}:
        return jsonify({'error': 'Unsupported language'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        if language == 'python':
            file_path = os.path.join(tmpdir, 'main.py')
            with open(file_path, 'w') as f:
                f.write(code)
            cmd = ['python3', file_path]
        elif language == 'c':
            src_path = os.path.join(tmpdir, 'main.c')
            bin_path = os.path.join(tmpdir, 'main')
            with open(src_path, 'w') as f:
                f.write(code)
            compile_result = subprocess.run(['gcc', src_path, '-o', bin_path], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return jsonify({'stdout': compile_result.stdout, 'stderr': compile_result.stderr, 'success': False})
            cmd = [bin_path]
        else:  # javascript
            file_path = os.path.join(tmpdir, 'main.js')
            with open(file_path, 'w') as f:
                f.write(code)
            cmd = ['node', file_path]

        try:
            result = subprocess.run(cmd, input=input_data, capture_output=True, text=True, timeout=5)
            stdout = result.stdout
            stderr = result.stderr
        except subprocess.TimeoutExpired:
            return jsonify({'stdout': '', 'stderr': 'Execution timed out.', 'success': False})

    success = False
    if expected_output is not None and stderr == '':
        success = stdout.strip() == expected_output.strip()

    return jsonify({'stdout': stdout, 'stderr': stderr, 'success': success})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)

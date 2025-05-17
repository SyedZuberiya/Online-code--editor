from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Python Code Runner Backend"

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    user_input = data.get('input', '')

    # Save code to file
    with open("temp.py", "w") as f:
        f.write(code)

    try:
        import subprocess
        result = subprocess.run(
            ["python3", "temp.py"],
            input=user_input.encode(),
            capture_output=True,
            timeout=5
        )
        output = result.stdout.decode() + result.stderr.decode()
    except subprocess.TimeoutExpired:
        output = "Error: Execution timed out."

    return jsonify({"output": output})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

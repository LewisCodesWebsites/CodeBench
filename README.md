# CodeBench

CodeBench is a simple web-based platform that lets you write, compile and test code in multiple programming languages. It is intended as a minimal example and **should not be used in production** without proper sandboxing.

## Features

- Write code in Python, C or JavaScript via a web interface
- Provide program input and an expected output for basic automated judging
- Compile and run code on the server and display the results

## Requirements

- Python 3
- gcc (for compiling C)
- Node.js (for JavaScript execution)

Install Python dependencies:

```bash
pip install -r backend/requirements.txt
```

## Running the application

From the repository root:

```bash
python backend/app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Security warning

The current implementation executes submitted code directly on the host machine. This is **insecure** and only intended for demonstration or local experimentation. Use a proper sandbox solution such as containers when deploying to production.

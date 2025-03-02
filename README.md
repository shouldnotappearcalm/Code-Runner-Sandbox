# Code Runner Sandbox

A secure code execution sandbox system supporting multiple programming languages.

[中文文档](README_zh.md)

## Features

- Multi-language code execution support
- Secure sandbox environment
- Code testing and evaluation
- Real-time execution results
- Execution time and memory usage statistics

## Supported Languages

- Python
- JavaScript
- Java
- Kotlin
- C++
- Go
- Rust
- Bash
- Objective-C
- Swift

## SDK Usage

Currently provides Python SDK, with other language SDKs (Java, Go, JavaScript, etc.) under development.

### Python SDK Installation

```bash
pip install code-runner-sdk
```

### Quick Start Example

```python
from code_runner_sdk import CodeRunnerClient, ProgrammingLanguage

# Create client instance
client = CodeRunnerClient(
    host="localhost",
    port=8000
)

# Run simple Python code
result = client.run_code(
    code='print("Hello, Code Runner!")',
    language=ProgrammingLanguage.PYTHON
)
print(f"Output: {result['output']}")
print(f"Execution Time: {result['execution_time']}ms")
print(f"Memory Usage: {result['memory_usage']}KB")
```

For more detailed SDK documentation, including:
- Complete API interface documentation
- Test case execution
- Exception handling
- Advanced configuration options
- Multi-language code examples

Please refer to the [SDK Documentation](sdk/code_runner_sdk/README.md)

### Using Code Reward Function in Open-R1

The code_reward function in Open-R1 is based on the e2b SandBox. This project can achieve the same functionality. For the reward calculation code segment:

Modify the `code_reward` method in `rewards.py` as follows:
```python
def code_reward(completions, **kwargs) -> list[float]:
    """Reward function that evaluates code snippets using the E2B code interpreter.

    Assumes the dataset contains a `verification_info` column with test cases.
    """
    from code_runner_sdk import CodeRunnerClient, ProgrammingLanguage
    # 创建客户端实例，可以自己修改 ip
    client = CodeRunnerClient(
        host="localhost",
        port=8000
    )

    rewards = []
    try:
        """Returns a reward function that evaluates code snippets in a sandbox."""
        evaluation_script_template = """
import subprocess
import json

def evaluate_code(code, test_cases):
    passed = 0
    total = len(test_cases)
    exec_timeout = 5

    for case in test_cases:
        process = subprocess.run(
            ["python3", "-c", code],
            input=case["input"],
            text=True,
            capture_output=True,
            timeout=exec_timeout
        )

        if process.returncode != 0:  # Error in execution
            continue

        output = process.stdout.strip()
        if output.strip() == case["output"].strip():
            passed += 1

    success_rate = (passed / total)
    return success_rate

code_snippet = {code}
test_cases = json.loads({test_cases})

rate = evaluate_code(code_snippet, test_cases)
print(rate)
        """
        code_snippets = [extract_code(completion[-1]["content"]) for completion in completions]
        verification_info = kwargs["verification_info"]
        scripts = [
            evaluation_script_template.format(
                code=json.dumps(code), test_cases=json.dumps(json.dumps(info["test_cases"]))
            )
            for code, info in zip(code_snippets, verification_info)
        ]
        for script in scripts:
            execution = client.run_code(script, language=ProgrammingLanguage(verification_info[-1]["language"]))
            try:
                output = float(execution['output'])
            except (TypeError, ValueError):
                output = 0.0
            rewards.append(output)
    except Exception as e:
        print(f"Error from Local executor: {e}")
        rewards = [0.0] * len(completions)
    return rewards
```

Test code as follows, the assertion will return true:
```python
def test_code_sandbox(self):
    """Test code reward with multiple code blocks in think and answer sections."""
    completions = [
        [
            {
                "content": "```python\nt=int(input())\nwhile(t):\n    n=int(input())\n    l=[]\n    for i in range(n):\n        l.append(list(map(int,input().split())))\n    m=[]\n    for i in l:\n        m.append((i[1]//(i[0]+1))*i[2])\n    res=max(m)\n    print(res)\n    t=t-1\n```"
            }
        ]
    ]
    verification_info = [
        {
            "language": "python",
            "test_cases": [
                {
                    "input": "2\n3\n4 6 8\n2 6 6\n1 4 3\n1\n7 7 4\n",
                    "output": "12\n0\n",
                    "type": "stdin_stdout"
                }
            ]
        }
    ]
    rewards = code_reward_sandbox(completions, verification_info=verification_info)
    self.assertEqual(rewards[0], 1.0)
```

## API Usage Examples

### Direct Code Execution

Python Example:
```bash
curl -X 'POST' \
  'http://localhost:8000/code/run' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "code": "print(\"Hello, World!\")",
  "language": "python"
}'
```

Go Example:
```bash
curl -X 'POST' \
  'http://localhost:8000/code/run' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "code": "fmt.Println(\"Hello, World!\")",
  "language": "go"
}'
```

Objective-C Example:
```bash
curl -X 'POST' \
  'http://localhost:8000/code/run' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "code": "NSArray *numbers = @[@5, @2, @8, @1, @9]; NSArray *sorted = [numbers sortedArrayUsingSelector:@selector(compare:)]; printf(\"Sorted array: %s\\n\", [[sorted description] UTF8String]);",
  "language": "objc"
}'
```

Swift Example:
```bash
curl -X 'POST' \
  'http://localhost:8000/code/run' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "code": "print(\"Hello from Swift!\")",
  "language": "swift"
}'
```

### Response Format

```json
{
  "output": "Execution Result",
  "execution_time": 123.45,  // Execution time (ms)
  "memory_usage": 1024       // Memory usage (KB)
}
```

## Project Structure

```
code-runner-sandbox/
├── app/
│   ├── api/                # API routes
│   ├── schemas/           # Data models
│   ├── services/          # Business logic
│   ├── executors/         # Language executors
│   ├── templates/         # Code templates
│   ├── utils/            # Utility functions
│   └── main.py           # Application entry
├── examples/             # Example code
├── tests/               # Test code
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Requirements

- Python 3.9+
- Language compilers/interpreters:
  - Python 3.9+
  - Node.js 14+
  - JDK 11+
  - Go 1.17+
  - Rust
  - GCC/G++
  - Xcode Command Line Tools (macOS, for Objective-C and Swift)

## Local Development

1. Clone repository:
```bash
git clone <repository-url>
cd code-runner-sandbox
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start service:
```bash
uvicorn app.main:app --reload
```

Service will start at http://localhost:8000, API documentation available at http://localhost:8000/docs.

## Docker Deployment

### Quick Deployment with Scripts

The project provides convenient deployment scripts:

#### Linux/Mac:
```bash
# Add execution permission
chmod +x build_and_run.sh

# Run script
./build_and_run.sh
```

#### Windows:
```bash
# Run batch script
build_and_run.bat
```

### Manual Build and Run

#### Build Docker Image

```bash
# Clone repository
git clone <repository-url>
cd code-runner-sandbox

# Build Docker image
docker build -t code-runner-sandbox .
```

#### Run Docker Container

```bash
# Run container
docker run -d -p 8000:8000 --name code-sandbox code-runner-sandbox

# View logs
docker logs -f code-sandbox
```

### Access API

After starting the application, you can access the API at:

- API Documentation: http://localhost:8000/docs
- Code Execution API: http://localhost:8000/code/run

## Security Notes

- All code executes in isolated environments
- Execution time and memory usage limits
- Dangerous system calls blocked
- Network access restricted

## License

MIT License
# Code Runner Python SDK

A Python SDK for the Code Runner service, providing simple and easy-to-use API interfaces for code execution and testing.

[中文文档](README_zh.md)

## Installation

```bash
pip install code-runner-sdk
```

## Quick Start

### Initialize Client

```python
from code_runner_sdk import CodeRunnerClient, ProgrammingLanguage

# Create client instance
client = CodeRunnerClient(
    host="localhost",
    port=8000,
    protocol="http",
    api_key="your-api-key"  # Optional
)
```

### Run Code Directly

```python
# Run Python code
result = client.run_code(
    code='print("Hello, World!")',
    language=ProgrammingLanguage.PYTHON
)

print(f"Output: {result['output']}")
print(f"Execution Time: {result['execution_time']}ms")
print(f"Memory Usage: {result['memory_usage']}KB")
```

### Execute Code with Tests

```python
from code_runner_sdk import TestCase

# Define test cases
test_cases = [
    TestCase(
        input={"a": 1, "b": 2},
        expected_output=3,
        description="1 + 2 = 3"
    ),
    TestCase(
        input={"a": -1, "b": 1},
        expected_output=0,
        description="-1 + 1 = 0"
    )
]

# Execute code and tests
code = """
def add(a, b):
    return a + b
"""

response = client.execute_code(
    code=code,
    language=ProgrammingLanguage.PYTHON,
    test_cases=test_cases
)

print(f"Status: {response.status}")
print(f"Tests Passed: {response.passed_tests}/{response.total_tests}")
print(f"Execution Time: {response.execution_time}ms")
print(f"Memory Usage: {response.memory_usage}KB")

# View detailed test results
for result in response.test_results:
    print(f"\nTest Case {result.test_case}:")
    print(f"Input: {result.input}")
    print(f"Expected Output: {result.expected_output}")
    print(f"Actual Output: {result.actual_output}")
    print(f"Passed: {'Yes' if result.passed else 'No'}")
    if result.error:
        print(f"Error: {result.error}")
```

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

## Exception Handling

```python
from code_runner_sdk.exceptions import (
    APIError,
    ValidationError,
    ConfigurationError,
    TimeoutError
)

try:
    result = client.run_code(
        code='print("Hello, World!")',
        language=ProgrammingLanguage.PYTHON
    )
except ValidationError as e:
    print(f"Validation Error: {e}")
except APIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Response: {e.response}")
except TimeoutError as e:
    print(f"Timeout Error: {e}")
except ConfigurationError as e:
    print(f"Configuration Error: {e}")
```

## Configuration Options

- `host`: API server host (default: localhost)
- `port`: API server port (default: 8000)
- `protocol`: Protocol (http/https, default: http)
- `api_key`: API key (optional)
- `timeout`: Request timeout in seconds (default: 30)

## Development

1. Clone repository:
```bash
git clone https://github.com/yourusername/code-runner-sdk.git
cd code-runner-sdk
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python -m pytest tests/
```

## License

MIT License 
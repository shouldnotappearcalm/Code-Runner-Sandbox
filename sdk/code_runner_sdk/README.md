# Code Runner Python SDK

A Python SDK for the Code Runner service, providing simple and easy-to-use API interfaces for code execution and testing.

[中文文档](#code-runner-python-sdk-中文版)

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

---

# Code Runner Python SDK (中文版)

Code Runner服务的Python SDK，提供简单易用的API接口来执行代码和运行测试。

[English Version](#code-runner-python-sdk)

## 安装

```bash
pip install code-runner-sdk
```

## 快速开始

### 初始化客户端

```python
from code_runner_sdk import CodeRunnerClient, ProgrammingLanguage

# 创建客户端实例
client = CodeRunnerClient(
    host="localhost",
    port=8000,
    protocol="http",
    api_key="your-api-key"  # 可选
)
```

### 直接运行代码

```python
# 运行Python代码
result = client.run_code(
    code='print("Hello, World!")',
    language=ProgrammingLanguage.PYTHON
)

print(f"输出: {result['output']}")
print(f"执行时间: {result['execution_time']}ms")
print(f"内存使用: {result['memory_usage']}KB")
```

### 执行代码并运行测试

```python
from code_runner_sdk import TestCase

# 定义测试用例
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

# 执行代码和测试
code = """
def add(a, b):
    return a + b
"""

response = client.execute_code(
    code=code,
    language=ProgrammingLanguage.PYTHON,
    test_cases=test_cases
)

print(f"状态: {response.status}")
print(f"通过测试: {response.passed_tests}/{response.total_tests}")
print(f"执行时间: {response.execution_time}ms")
print(f"内存使用: {response.memory_usage}KB")

# 查看详细测试结果
for result in response.test_results:
    print(f"\n测试用例 {result.test_case}:")
    print(f"输入: {result.input}")
    print(f"预期输出: {result.expected_output}")
    print(f"实际输出: {result.actual_output}")
    print(f"通过: {'是' if result.passed else '否'}")
    if result.error:
        print(f"错误: {result.error}")
```

## 支持的编程语言

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

## 异常处理

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
    print(f"验证错误: {e}")
except APIError as e:
    print(f"API错误: {e}")
    print(f"状态码: {e.status_code}")
    print(f"响应: {e.response}")
except TimeoutError as e:
    print(f"超时错误: {e}")
except ConfigurationError as e:
    print(f"配置错误: {e}")
```

## 配置选项

- `host`: API服务器主机地址（默认：localhost）
- `port`: API服务器端口（默认：8000）
- `protocol`: 协议（http/https，默认：http）
- `api_key`: API密钥（可选）
- `timeout`: 请求超时时间（秒，默认：30）

## 开发

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/code-runner-sdk.git
cd code-runner-sdk
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行测试：
```bash
python -m pytest tests/
```

## 许可证

MIT License 
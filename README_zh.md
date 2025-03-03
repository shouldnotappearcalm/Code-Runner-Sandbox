# Code Runner Sandbox

一个支持多种编程语言的代码执行沙箱系统。

[English](README.md)

## 功能特点

- 支持多种编程语言的代码执行
- 安全的沙箱环境
- 支持代码测试和评估
- 实时执行结果返回
- 执行时间和内存使用统计

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

## SDK 使用

目前提供 Python SDK，其他语言（Java、Go、JavaScript 等）的 SDK 正在开发中。

### 首先启动 web 应用
使用下面的命令
```bash
uvicorn app.main:app --reload
```

或者使用 docker 来启动
```bash
sh ./build_and_run.sh
```


### Python SDK 安装

```bash
pip install code-runner-sdk
```

### 快速开始示例

```python
from code_runner_sdk import CodeRunnerClient, ProgrammingLanguage

# 创建客户端实例
client = CodeRunnerClient(
    host="localhost",
    port=8000
)

# 运行简单的 Python 代码
result = client.run_code(
    code='print("Hello, Code Runner!")',
    language=ProgrammingLanguage.PYTHON
)
print(f"输出内容: {result['output']}")
print(f"执行时间: {result['execution_time']}ms")
print(f"内存使用: {result['memory_usage']}KB")
```

更多详细的 SDK 使用说明，包括：
- 完整的 API 接口文档
- 测试用例执行
- 异常处理
- 高级配置选项
- 多语言代码示例

请参考 [SDK 详细文档](sdk/code_runner_sdk/README_zh.md)

### Open-R1 中如何使用 Code Reward 奖励函数

Open-R1 中 code_reward 函数基于 e2b SandBox，本项目可以实现相同的功能，对于计算奖励的代码段：

修改 `rewards.py` 文件中的 `code_reward` 方法如下即可：
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

测试代码如下，下面断言会返回 true：
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

## API 使用示例

### 直接执行代码

Python 示例：
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

Go 示例：
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

Objective-C 示例：
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

Swift 示例：
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

### 响应格式

```json
{
  "output": "执行结果",
  "execution_time": 123.45,  // 执行时间（毫秒）
  "memory_usage": 1024       // 内存使用（KB）
}
```

## 项目结构

```
code-runner-sandbox/
├── app/
│   ├── api/                # API路由
│   ├── schemas/            # 数据模型
│   ├── services/           # 业务逻辑
│   ├── executors/         # 语言执行器
│   ├── templates/          # 代码模板
│   ├── utils/             # 工具函数
│   └── main.py            # 应用入口
├── examples/              # 示例代码
├── tests/                # 测试代码
├── Dockerfile            # Docker配置
├── requirements.txt      # Python依赖
└── README.md            # 项目说明
```

## 环境要求

- Python 3.9+
- 各语言编译器/解释器：
  - Python 3.9+
  - Node.js 14+
  - JDK 11+
  - Go 1.17+
  - Rust
  - GCC/G++
  - Xcode Command Line Tools (macOS，用于 Objective-C 和 Swift)

## 本地开发

1. 克隆仓库：
```bash
git clone <repository-url>
cd code-runner-sandbox
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 启动服务：
```bash
uvicorn app.main:app --reload
```

服务将在 http://localhost:8000 启动，API 文档可在 http://localhost:8000/docs 查看。

## Docker 部署

### 使用脚本快速部署

项目提供了便捷的部署脚本：

#### Linux/Mac:
```bash
# 添加执行权限
chmod +x build_and_run.sh

# 运行脚本
./build_and_run.sh
```

#### Windows:
```bash
# 运行批处理脚本
build_and_run.bat
```

### 手动构建和运行

#### 构建Docker镜像

```bash
# 克隆仓库
git clone <repository-url>
cd code-runner-sandbox

# 构建Docker镜像
docker build -t code-runner-sandbox .
```

#### 运行Docker容器

```bash
# 运行容器
docker run -d -p 8000:8000 --name code-sandbox code-runner-sandbox

# 查看日志
docker logs -f code-sandbox
```

### 访问API

应用启动后，可以通过以下URL访问API：

- API文档：http://localhost:8000/docs
- 代码执行API：http://localhost:8000/code/run

## 安全说明

- 所有代码在隔离的环境中执行
- 限制执行时间和内存使用
- 禁止危险系统调用
- 网络访问受限

## 许可证

MIT License 

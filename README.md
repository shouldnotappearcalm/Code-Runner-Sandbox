# 代码执行沙箱

一个安全的代码执行环境，支持多种编程语言（Python、JavaScript、Java、C++、Go、Rust）的代码执行和测试。

## 功能特点

- 支持多种编程语言：Python、JavaScript、Java、C++、Go、Rust
- 安全的代码执行环境
- 代码测试与评估
- RESTful API接口
- 资源限制（执行时间、内存使用）

## 使用Docker部署

本项目提供了Dockerfile，可以轻松构建和运行整个应用。

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
git clone https://github.com/yourusername/code-runner-sandbox.git
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
- 代码执行API：http://localhost:8000/code/execute

## API使用示例

### 执行代码

```bash
curl -X POST "http://localhost:8000/code/execute" \
  -H "Content-Type: application/json" \
  -d '{
  "code" : "\nclass Solution:\n    def solve(self, problem):\n        nums = problem[\"nums\"]\n        target = problem[\"target\"]\n        \n        # 使用哈希表解决两数之和问题\n        num_map = {}\n        for i, num in enumerate(nums):\n            complement = target - num\n            if complement in num_map:\n                return [num_map[complement], i]\n            num_map[num] = i\n        \n        return []  # 没有找到解\n",
  "language" : "python",
  "problem_id" : "two-sum",
  "test_cases" : [ {
    "input" : {
      "nums" : [ 2, 7, 11, 15 ],
      "target" : 9
    },
    "expected_output" : [ 0, 1 ],
    "description" : "示例 1: 目标和为 9"
  }, {
    "input" : {
      "nums" : [ 3, 2, 4 ],
      "target" : 6
    },
    "expected_output" : [ 1, 2 ],
    "description" : "示例 2: 目标和为 6"
  }, {
    "input" : {
      "nums" : [ 3, 3 ],
      "target" : 6
    },
    "expected_output" : [ 0, 1 ],
    "description" : "示例 3: 相同元素"
  } ]
}'
```

### 对于 Code Reward 奖励函数

Open-R1 中 code_reward 函数基于 e2b SandBox，本项目可以实现相同的功能，对于计算奖励的代码段

```python
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
    print(success_rate)
    return success_rate

code_snippet = "t=int(input())\nwhile(t):\n    n=int(input())\n    l=[]\n    for i in range(n):\n        l.append(list(map(int,input().split())))\n    m=[]\n    for i in l:\n        m.append((i[1]//(i[0]+1))*i[2])\n    res=max(m)\n    print(res)\n    t=t-1"
test_cases = json.loads('[{"fn_name": null, "input": "2\\n3\\n4 6 8\\n2 6 6\\n1 4 3\\n1\\n7 7 4\\n", "output": "12\\n0\\n", "type": "stdin_stdout"}]')

evaluate_code(code_snippet, test_cases)
```

执行代码
```bash
curl -X 'POST' \
  'http://localhost:8000/code/run' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "code": "import subprocess\nimport json\n\ndef evaluate_code(code, test_cases):\n    passed = 0\n    total = len(test_cases)\n    exec_timeout = 5\n\n    for case in test_cases:\n        process = subprocess.run(\n            [\"python3\", \"-c\", code],\n            input=case[\"input\"],\n            text=True,\n            capture_output=True,\n            timeout=exec_timeout\n        )\n\n        if process.returncode != 0:  # Error in execution\n            continue\n\n        output = process.stdout.strip()\n        if output.strip() == case[\"output\"].strip():\n            passed += 1\n\n    success_rate = (passed / total)\n    print(success_rate)\n    return success_rate\n\ncode_snippet = \"t=int(input())\\nwhile(t):\\n    n=int(input())\\n    l=[]\\n    for i in range(n):\\n        l.append(list(map(int,input().split())))\\n    m=[]\\n    for i in l:\\n        m.append((i[1]//(i[0]+1))*i[2])\\n    res=max(m)\\n    print(res)\\n    t=t-1\"\ntest_cases = json.loads('\''[{\"fn_name\": null, \"input\": \"2\\\\n3\\\\n4 6 8\\\\n2 6 6\\\\n1 4 3\\\\n1\\\\n7 7 4\\\\n\", \"output\": \"12\\\\n0\\\\n\", \"type\": \"stdin_stdout\"}]'\'')\n\nevaluate_code(code_snippet, test_cases)\n",
    "language": "python"
}'
```

输出如下：
```
{
  "output": "1.0",
  "execution_time": 7213.936805725098,
  "memory_usage": 0
}
```

## 支持的编程语言

- Python
- JavaScript
- Java
- C++
- Go
- Rust

## 项目结构

```
code-runner-sandbox/
├── app/
│   ├── api/                # API路由
│   ├── schemas/            # 数据模型
│   ├── services/           # 业务逻辑
│   ├── templates/          # 代码模板
│   ├── utils/              # 工具函数
│   └── main.py             # 应用入口
├── examples/               # 示例代码
├── tests/                  # 测试代码
├── Dockerfile              # Docker配置
├── build_and_run.sh        # Linux/Mac部署脚本
├── build_and_run.bat       # Windows部署脚本
├── requirements.txt        # Python依赖
└── README.md               # 项目说明
```

## 本地开发

### 环境要求

- Python 3.9+
- 各语言的编译器/解释器：
  - Node.js 16+
  - JDK 11
  - G++ 11+
  - Go 1.17+
  - Rust 1.58+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

```bash
uvicorn app.main:app --reload
```

## 安全注意事项

该系统使用本地环境执行用户代码，提供了基本的资源限制。在生产环境中，应考虑以下安全措施：

1. 限制资源使用（CPU、内存、网络）
2. 使用更严格的安全策略
3. 实现速率限制和用户认证
4. 定期更新依赖项
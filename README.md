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
    "code": "def solve(nums):\n    return sum(nums)",
    "language": "python",
    "problem_id": "sum-of-array",
    "test_cases": [
      {
        "input": [1, 2, 3, 4, 5],
        "expected_output": 15,
        "description": "测试用例1"
      }
    ]
  }'
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
# 使用Ubuntu作为基础镜像
FROM ubuntu:22.04

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 设置工作目录
WORKDIR /app

# 安装基础工具和依赖
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    pkg-config \
    sudo \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv

# 安装Python依赖
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 安装Node.js (JavaScript)
# RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
#     apt-get install -y nodejs && \
#     npm install -g npm@latest

# 安装Java
RUN apt-get install -y openjdk-11-jdk

# 安装C++
RUN apt-get install -y g++ cmake libboost-all-dev nlohmann-json3-dev

# 安装Go
RUN wget https://go.dev/dl/go1.17.13.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.17.13.linux-amd64.tar.gz && \
    rm go1.17.13.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin

# 安装Rust
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH=$PATH:/root/.cargo/bin

# 复制应用代码
COPY . .

# 移除Docker相关代码并添加本地执行引擎
# RUN sed -i '/import docker/d' app/services/code_execution_service.py && \
#     sed -i '/DockerExecutionEngine/,/def _create_runner_script/d' app/services/code_execution_service.py && \
#     sed -i 's/_engine = DockerExecutionEngine()/_executors = {\
#         ProgrammingLanguage.PYTHON: PythonExecutor(),\
#         ProgrammingLanguage.JAVASCRIPT: JavaScriptExecutor(),\
#         ProgrammingLanguage.JAVA: JavaExecutor(),\
#         ProgrammingLanguage.CPP: CppExecutor(),\
#         ProgrammingLanguage.GO: GoExecutor(),\
#         ProgrammingLanguage.RUST: RustExecutor()\
#     }/g' app/services/code_execution_service.py && \
#     sed -i 's/await cls._engine.execute(code, language, test_input)/await executor.execute(code, test_input)/g' app/services/code_execution_service.py && \
#     sed -i 's/executor = cls._engine.executors.get(language)/executor = cls._executors.get(language)/g' app/services/code_execution_service.py

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
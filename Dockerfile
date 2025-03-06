# 使用Ubuntu作为基础镜像
FROM ubuntu:22.04

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PATH="/usr/local/go/bin:/root/.cargo/bin:/usr/share/swift/usr/bin:$PATH"
ENV SDKMAN_DIR="/root/.sdkman"
# 设置SDKMAN镜像
ENV SDKMAN_PLATFORM_ENDPOINT="https://mirrors.tuna.tsinghua.edu.cn/sdkman/candidates/list"
ENV SDKMAN_VERSION_ENDPOINT="https://mirrors.tuna.tsinghua.edu.cn/sdkman/candidates/%s"
ENV SDKMAN_BROKER_SERVICE_ENDPOINT="https://mirrors.tuna.tsinghua.edu.cn/sdkman/broker/download/%s/%s/%s"

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
    python3-venv \
    zip \
    unzip

# 安装Python依赖
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 安装Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# 安装Java
RUN apt-get install -y openjdk-17-jdk

# 安装SDKMAN和Kotlin
RUN curl -s "https://get.sdkman.io" | bash && \
    echo "sdkman_auto_answer=true" >> $SDKMAN_DIR/etc/config && \
    echo "sdkman_auto_selfupdate=false" >> $SDKMAN_DIR/etc/config && \
    echo "sdkman_insecure_ssl=false" >> $SDKMAN_DIR/etc/config && \
    bash -c "source $SDKMAN_DIR/bin/sdkman-init.sh && \
    yes | sdk install kotlin"

# 安装C++
RUN apt-get install -y g++ cmake libboost-all-dev nlohmann-json3-dev

# 安装Go
RUN wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz && \
    rm go1.22.2.linux-amd64.tar.gz

# 安装Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    . $HOME/.cargo/env

# 安装Swift依赖
RUN apt-get install -y \
    binutils \
    libc6-dev \
    libcurl4 \
    libedit2 \
    libgcc-11-dev \
    libpython3.10 \
    libsqlite3-0 \
    libstdc++-11-dev \
    libxml2 \
    libz3-dev \
    pkg-config \
    tzdata \
    zlib1g-dev

# 安装Swift
RUN wget https://swift.org/builds/swift-5.9.3-release/ubuntu2204/swift-5.9.3-RELEASE/swift-5.9.3-RELEASE-ubuntu22.04.tar.gz && \
    tar xzf swift-5.9.3-RELEASE-ubuntu22.04.tar.gz && \
    mv swift-5.9.3-RELEASE-ubuntu22.04 /usr/share/swift && \
    rm swift-5.9.3-RELEASE-ubuntu22.04.tar.gz

# 安装Clang (用于Objective-C)
RUN apt-get install -y clang

# 验证安装
RUN echo "Verifying installations..." && \
    python3 --version && \
    node --version && \
    java -version && \
    kotlin -version && \
    go version && \
    rustc --version && \
    swift --version && \
    clang --version

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
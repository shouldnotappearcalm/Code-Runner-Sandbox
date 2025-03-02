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

# 安装Node.js (升级到20.x LTS版本)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# 安装Java和Kotlin
# RUN apt-get install -y openjdk-17-jdk && \
#     curl -s "https://get.sdkman.io" | bash && \
#     bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && sdk install kotlin"
#
# # 安装C++
# RUN apt-get install -y g++ cmake libboost-all-dev nlohmann-json3-dev
#
# # 安装Go (升级到1.22.2)
# RUN wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz && \
#     tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz && \
#     rm go1.22.2.linux-amd64.tar.gz
# ENV PATH=$PATH:/usr/local/go/bin
#
# # 安装Rust
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# ENV PATH=$PATH:/root/.cargo/bin
#
# # 安装Swift (升级到5.9.3)
# RUN apt-get install -y \
#     binutils \
#     libc6-dev \
#     libcurl4 \
#     libedit2 \
#     libgcc-11-dev \
#     libpython3.10 \
#     libsqlite3-0 \
#     libstdc++-11-dev \
#     libxml2 \
#     libz3-dev \
#     pkg-config \
#     tzdata \
#     zlib1g-dev && \
#     wget https://swift.org/builds/swift-5.9.3-release/ubuntu2204/swift-5.9.3-RELEASE/swift-5.9.3-RELEASE-ubuntu22.04.tar.gz && \
#     tar xzf swift-5.9.3-RELEASE-ubuntu22.04.tar.gz && \
#     mv swift-5.9.3-RELEASE-ubuntu22.04 /usr/share/swift && \
#     rm swift-5.9.3-RELEASE-ubuntu22.04.tar.gz
# ENV PATH=/usr/share/swift/usr/bin:$PATH
#
# # 安装Clang (用于Objective-C)
# RUN apt-get install -y clang

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
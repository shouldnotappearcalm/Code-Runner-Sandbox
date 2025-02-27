#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
echo -e "${GREEN}开始构建代码执行沙箱...${NC}"

# 构建Docker镜像
echo -e "${YELLOW}构建Docker镜像...${NC}"
docker build -t code-runner-sandbox .

# 检查构建是否成功
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Docker镜像构建成功!${NC}"
    
    # 检查是否有正在运行的容器
    CONTAINER_ID=$(docker ps -q -f name=code-sandbox)
    if [ ! -z "$CONTAINER_ID" ]; then
        echo -e "${YELLOW}发现正在运行的容器，正在停止...${NC}"
        docker stop code-sandbox
        docker rm code-sandbox
    fi
    
    # 运行容器
    echo -e "${YELLOW}启动容器...${NC}"
    docker run -d -p 8000:8000 --name code-sandbox code-runner-sandbox
    
    # 检查容器是否成功启动
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}容器启动成功!${NC}"
        echo -e "${GREEN}API文档地址: http://localhost:8000/docs${NC}"
        echo -e "${GREEN}代码执行API: http://localhost:8000/code/execute${NC}"
        
        # 显示容器日志
        echo -e "${YELLOW}容器日志:${NC}"
        docker logs -f code-sandbox
    else
        echo -e "${YELLOW}容器启动失败，请检查错误信息。${NC}"
    fi
else
    echo -e "${YELLOW}Docker镜像构建失败，请检查错误信息。${NC}"
fi 
@echo off
echo 开始构建代码执行沙箱...

REM 构建Docker镜像
echo 构建Docker镜像...
docker build -t code-runner-sandbox .

REM 检查构建是否成功
if %ERRORLEVEL% EQU 0 (
    echo Docker镜像构建成功!
    
    REM 检查是否有正在运行的容器
    for /f %%i in ('docker ps -q -f name^=code-sandbox') do set CONTAINER_ID=%%i
    if defined CONTAINER_ID (
        echo 发现正在运行的容器，正在停止...
        docker stop code-sandbox
        docker rm code-sandbox
    )
    
    REM 运行容器
    echo 启动容器...
    docker run -d -p 8000:8000 --name code-sandbox code-runner-sandbox
    
    REM 检查容器是否成功启动
    if %ERRORLEVEL% EQU 0 (
        echo 容器启动成功!
        echo API文档地址: http://localhost:8000/docs
        echo 代码执行API: http://localhost:8000/code/execute
        
        REM 显示容器日志
        echo 容器日志:
        docker logs -f code-sandbox
    ) else (
        echo 容器启动失败，请检查错误信息。
    )
) else (
    echo Docker镜像构建失败，请检查错误信息。
) 
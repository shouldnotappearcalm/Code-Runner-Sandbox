from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.api import items, code_execution

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    # 增强Swagger文档配置
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "code-execution",
            "description": "代码执行相关接口",
            "externalDocs": {
                "description": "代码执行服务文档",
                "url": "https://github.com/your-repo/code-execution-docs",
            },
        },
        {
            "name": "items",
            "description": "其他接口",
        },
        {
            "name": "root",
            "description": "根路由",
        },
    ],
    swagger_ui_parameters=settings.SWAGGER_UI_PARAMETERS,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由
@app.get("/", tags=["root"], summary="根路由", description="返回欢迎信息")
async def root():
    """
    根路由
    
    返回欢迎信息
    """
    return {"message": f"欢迎使用 {settings.APP_NAME}"}

# 包含路由器
app.include_router(items.router)
app.include_router(code_execution.router)

# 直接运行此文件时启动服务器
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 
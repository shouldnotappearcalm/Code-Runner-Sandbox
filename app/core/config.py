import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Settings(BaseSettings):
    """应用配置设置"""
    
    # 应用信息
    APP_NAME: str = "代码执行平台"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = """
    代码执行平台 API 文档
    
    ## 功能
    
    * 支持多种编程语言的代码执行
    * 提供代码测试功能
    * 安全的代码执行环境
    
    ## 支持的语言
    
    * Python
    * JavaScript
    * Java
    * C++
    * Go
    * Rust
    """
    
    # API 前缀
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS 设置
    CORS_ORIGINS: list = ["*"]
    
    # 数据库设置 (示例)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Swagger UI 设置
    SWAGGER_UI_OAUTH2_REDIRECT_URL: str = "/api/oauth2-redirect"
    SWAGGER_UI_PARAMETERS = {
        "defaultModelsExpandDepth": 1,
        "deepLinking": True,
        "displayRequestDuration": True,
        "syntaxHighlight.theme": "monokai"
    }
    
    class Config:
        case_sensitive = True

# 创建设置实例
settings = Settings() 
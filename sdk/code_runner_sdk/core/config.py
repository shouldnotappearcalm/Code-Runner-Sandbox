"""
SDK配置模块
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CodeRunnerConfig:
    """Code Runner SDK配置类"""
    host: str = "localhost"
    port: int = 8000
    protocol: str = "http"
    api_version: str = "v1"
    timeout: int = 30
    api_key: Optional[str] = None

    @property
    def base_url(self) -> str:
        """获取基础URL"""
        return f"{self.protocol}://{self.host}:{self.port}"

    @property
    def api_url(self) -> str:
        """获取API URL"""
        return f"{self.base_url}/code" 
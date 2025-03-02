"""
HTTP客户端模块
"""
import json
from typing import Optional, Dict, Any
import requests
from requests.exceptions import RequestException, Timeout

from ..core.config import CodeRunnerConfig
from ..exceptions import APIError, TimeoutError


class HTTPClient:
    """HTTP客户端类"""
    
    def __init__(self, config: CodeRunnerConfig):
        """
        初始化HTTP客户端
        
        Args:
            config: SDK配置对象
        """
        self.config = config
        self.session = requests.Session()
        if config.api_key:
            self.session.headers.update({"Authorization": f"Bearer {config.api_key}"})
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        处理API响应
        
        Args:
            response: 请求响应对象
            
        Returns:
            Dict[str, Any]: 响应数据
            
        Raises:
            APIError: 当API返回错误时
        """
        try:
            data = response.json()
        except ValueError:
            raise APIError(f"无效的JSON响应: {response.text}", response.status_code)
            
        if not 200 <= response.status_code < 300:
            raise APIError(
                data.get("detail", "未知错误"),
                response.status_code,
                data
            )
            
        return data
    
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            params: URL参数
            data: 表单数据
            json_data: JSON数据
            **kwargs: 其他请求参数
            
        Returns:
            Dict[str, Any]: 响应数据
            
        Raises:
            APIError: 当API返回错误时
            TimeoutError: 当请求超时时
        """
        url = f"{self.config.api_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                timeout=self.config.timeout,
                **kwargs
            )
            return self._handle_response(response)
            
        except Timeout:
            raise TimeoutError(f"请求超时: {url}")
        except RequestException as e:
            raise APIError(f"请求失败: {str(e)}")
            
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送GET请求"""
        return self.request("GET", endpoint, **kwargs)
        
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送POST请求"""
        return self.request("POST", endpoint, **kwargs)
        
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送PUT请求"""
        return self.request("PUT", endpoint, **kwargs)
        
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送DELETE请求"""
        return self.request("DELETE", endpoint, **kwargs) 
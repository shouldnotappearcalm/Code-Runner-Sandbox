"""
Code Runner SDK主客户端模块
"""
from typing import Optional, List, Dict, Any

from .config import CodeRunnerConfig
from ..http.client import HTTPClient
from ..models.code_execution import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    ProgrammingLanguage,
    TestCase,
    TestResult,
    ExecutionStatus
)
from ..exceptions import ValidationError


class CodeRunnerClient:
    """Code Runner SDK主客户端类"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        protocol: str = "http",
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        """
        初始化Code Runner客户端
        
        Args:
            host: API主机地址
            port: API端口
            protocol: 协议（http/https）
            api_key: API密钥
            timeout: 请求超时时间（秒）
        """
        self.config = CodeRunnerConfig(
            host=host,
            port=port,
            protocol=protocol,
            api_key=api_key,
            timeout=timeout
        )
        self.http_client = HTTPClient(self.config)
    
    def execute_code(
        self,
        code: str,
        language: ProgrammingLanguage,
        test_cases: Optional[List[TestCase]] = None,
        problem_id: Optional[str] = None
    ) -> CodeExecutionResponse:
        """
        执行代码
        
        Args:
            code: 要执行的代码
            language: 编程语言
            test_cases: 测试用例列表
            problem_id: 问题ID
            
        Returns:
            CodeExecutionResponse: 代码执行结果
            
        Raises:
            ValidationError: 当参数验证失败时
            APIError: 当API调用失败时
        """
        if not code:
            raise ValidationError("代码不能为空")
            
        request = CodeExecutionRequest(
            code=code,
            language=language,
            test_cases=test_cases,
            problem_id=problem_id
        )
        
        response = self.http_client.post(
            "execute",
            json_data=request.__dict__
        )
        
        # 转换响应数据为CodeExecutionResponse对象
        test_results = []
        if response.get("test_results"):
            for result in response["test_results"]:
                test_results.append(TestResult(
                    test_case=result["test_case"],
                    passed=result["passed"],
                    input=result["input"],
                    expected_output=result["expected_output"],
                    actual_output=result["actual_output"],
                    execution_time=result["execution_time"],
                    memory_usage=result["memory_usage"],
                    error=result.get("error")
                ))
                
        return CodeExecutionResponse(
            status=ExecutionStatus(response["status"]),
            test_results=test_results,
            total_tests=response["total_tests"],
            passed_tests=response["passed_tests"],
            execution_time=response.get("execution_time"),
            memory_usage=response.get("memory_usage"),
            message=response.get("message")
        )
    
    def run_code(
        self,
        code: str,
        language: ProgrammingLanguage
    ) -> Dict[str, Any]:
        """
        直接运行代码（不需要测试用例）
        
        Args:
            code: 要执行的代码
            language: 编程语言
            
        Returns:
            Dict[str, Any]: 包含输出、执行时间和内存使用的字典
            
        Raises:
            ValidationError: 当参数验证失败时
            APIError: 当API调用失败时
        """
        if not code:
            raise ValidationError("代码不能为空")
            
        return self.http_client.post(
            "run",
            json_data={
                "code": code,
                "language": language
            }
        ) 
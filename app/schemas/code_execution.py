from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum


class ProgrammingLanguage(str, Enum):
    """支持的编程语言枚举"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"


class CodeExecutionRequest(BaseModel):
    """代码执行请求模型"""
    code: str = Field(..., description="用户提交的代码")
    language: ProgrammingLanguage = Field(..., description="编程语言")
    problem_id: str = Field(..., description="问题ID")
    test_cases: Optional[List[Dict[str, Any]]] = Field(None, description="自定义测试用例")


class TestCase(BaseModel):
    """测试用例模型"""
    input: Any = Field(..., description="测试输入")
    expected_output: Any = Field(..., description="期望输出")
    description: Optional[str] = Field(None, description="测试用例描述")


class TestResult(BaseModel):
    """单个测试结果模型"""
    passed: bool = Field(..., description="测试是否通过")
    input: Any = Field(..., description="测试输入")
    expected_output: Any = Field(..., description="期望输出")
    actual_output: Any = Field(..., description="实际输出")
    execution_time: float = Field(..., description="执行时间(毫秒)")
    memory_usage: float = Field(..., description="内存使用(KB)")
    description: Optional[str] = Field(None, description="测试描述")


class ExecutionStatus(str, Enum):
    """执行状态枚举"""
    SUCCESS = "success"
    COMPILE_ERROR = "compile_error"
    RUNTIME_ERROR = "runtime_error"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    INTERNAL_ERROR = "internal_error"


class CodeExecutionResponse(BaseModel):
    """代码执行响应模型"""
    status: ExecutionStatus = Field(..., description="执行状态")
    message: Optional[str] = Field(None, description="执行消息")
    test_results: Optional[List[TestResult]] = Field(None, description="测试结果")
    total_tests: int = Field(0, description="测试用例总数")
    passed_tests: int = Field(0, description="通过的测试用例数")
    execution_time: Optional[float] = Field(None, description="总执行时间(毫秒)")
    memory_usage: Optional[float] = Field(None, description="最大内存使用(KB)")


class Problem(BaseModel):
    """问题模型"""
    id: str = Field(..., description="问题ID")
    title: str = Field(..., description="问题标题")
    description: str = Field(..., description="问题描述")
    difficulty: str = Field(..., description="难度级别")
    test_cases: List[TestCase] = Field(..., description="测试用例")
    function_signature: Dict[str, Dict[str, str]] = Field(
        ..., description="各语言的函数签名"
    )
    constraints: Optional[str] = Field(None, description="约束条件")
    examples: Optional[List[Dict[str, Any]]] = Field(None, description="示例")
    tags: Optional[List[str]] = Field(None, description="标签") 
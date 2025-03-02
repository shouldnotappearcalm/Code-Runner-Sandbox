"""
代码执行相关的数据模型
"""
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


class ProgrammingLanguage(str, Enum):
    """支持的编程语言枚举"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    KOTLIN = "kotlin"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    BASH = "bash"
    OBJC = "objc"
    SWIFT = "swift"


class ExecutionStatus(str, Enum):
    """执行状态枚举"""
    SUCCESS = "success"
    COMPILE_ERROR = "compile_error"
    RUNTIME_ERROR = "runtime_error"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    INTERNAL_ERROR = "internal_error"


@dataclass
class TestCase:
    """测试用例模型"""
    input: Dict[str, Any]
    expected_output: Any
    description: Optional[str] = None


@dataclass
class TestResult:
    """测试结果模型"""
    test_case: int
    passed: bool
    input: Dict[str, Any]
    expected_output: Any
    actual_output: Any
    execution_time: float
    memory_usage: float
    error: Optional[str] = None


@dataclass
class CodeExecutionRequest:
    """代码执行请求模型"""
    code: str
    language: ProgrammingLanguage
    test_cases: Optional[List[TestCase]] = None
    problem_id: Optional[str] = None


@dataclass
class CodeExecutionResponse:
    """代码执行响应模型"""
    status: ExecutionStatus
    test_results: Optional[List[TestResult]] = None
    total_tests: int = 0
    passed_tests: int = 0
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None
    message: Optional[str] = None 
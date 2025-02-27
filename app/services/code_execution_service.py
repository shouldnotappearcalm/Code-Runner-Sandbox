import os
import time
import tempfile
import subprocess
import json
import shutil
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from pathlib import Path
import resource
from enum import Enum

from app.schemas.code_execution import (
    ProgrammingLanguage,
    ExecutionStatus,
    TestResult,
    CodeExecutionResponse,
    TestCase,
    CodeExecutionRequest
)

from app.utils.code_generator import CodeGenerator

from app.executors.python_executor import PythonExecutor
from app.executors.javascript_executor import JavaScriptExecutor
from app.executors.java_executor import JavaExecutor
from app.executors.cpp_executor import CppExecutor
from app.executors.go_executor import GoExecutor
from app.executors.rust_executor import RustExecutor

# 执行超时时间（秒）
EXECUTION_TIMEOUT = 10
# 内存限制（MB）
MEMORY_LIMIT = 512

class CodeExecutionService:
    """
    代码执行服务
    
    提供代码执行和测试功能的服务类，支持多种编程语言：
    - Python
    - JavaScript
    - Java
    - C++
    - Go
    - Rust
    
    每种语言都有对应的执行器实现，负责代码的编译和运行。
    所有执行都在安全的环境中进行，有执行时间和内存使用限制。
    """
    
    # 注册语言执行器
    _executors = {
        ProgrammingLanguage.PYTHON: PythonExecutor(),
        ProgrammingLanguage.JAVASCRIPT: JavaScriptExecutor(),
        ProgrammingLanguage.JAVA: JavaExecutor(),
        ProgrammingLanguage.CPP: CppExecutor(),
        ProgrammingLanguage.GO: GoExecutor(),
        ProgrammingLanguage.RUST: RustExecutor()
    }
    
    @classmethod
    async def execute_code(cls, request: CodeExecutionRequest) -> CodeExecutionResponse:
        """
        执行代码
        
        Args:
            request: 代码执行请求
            
        Returns:
            CodeExecutionResponse: 代码执行响应
        """
        code = request.code
        language = request.language
        problem_id = request.problem_id
        test_cases = request.test_cases
        
        # 获取对应语言的执行器
        executor = cls._executors.get(language)
        if not executor:
            return CodeExecutionResponse(
                status="error",
                message=f"不支持的编程语言: {language}",
                passed_tests=0,
                total_tests=len(test_cases),
                results=[]
            )
        
        # 对于Java语言，打印用户代码长度和内容以便调试
        if language == ProgrammingLanguage.JAVA:
            print(f"Java用户代码长度: {len(code)}")
            print(f"Java用户代码内容: {code[:100]}...")
            
            # 确保用户代码中有Solution类
            if "class Solution" not in code:
                code = f"""
                public class Solution {{
                    public Object solve(java.util.Map<String, Object> input) {{
                        // 默认实现
                        return null;
                    }}
                    
                    {code}
                }}
                """
        
        # 生成测试代码
        code_generator = CodeGenerator()
        test_code = code_generator.generate_test_code(code, language, test_cases)
        
        # 对于Java语言，打印生成的测试代码长度以便调试
        if language == ProgrammingLanguage.JAVA:
            print(f"生成的Java测试代码长度: {len(test_code)}")
            print(f"生成的Java测试代码前100字符: {test_code[:100]}...")
        
        # 执行测试代码
        try:
            results = []
            passed_tests = 0
            
            for i, test_case in enumerate(test_cases):
                test_input = {
                    "input": test_case.input,
                    "expected_output": test_case.expected_output
                }
                
                # 执行代码
                output, execution_time, memory_usage = await executor.execute(test_code, test_input)
                
                # 检查结果
                if isinstance(output, dict) and "error" in output:
                    results.append({
                        "test_case": i + 1,
                        "input": test_case.input,
                        "expected_output": test_case.expected_output,
                        "actual_output": None,
                        "passed": False,
                        "error": output["error"],
                        "execution_time": execution_time,
                        "memory_usage": memory_usage
                    })
                else:
                    passed = output == test_case.expected_output
                    if passed:
                        passed_tests += 1
                    
                    results.append({
                        "test_case": i + 1,
                        "input": test_case.input,
                        "expected_output": test_case.expected_output,
                        "actual_output": output,
                        "passed": passed,
                        "execution_time": execution_time,
                        "memory_usage": memory_usage
                    })
            
            return CodeExecutionResponse(
                status="success",
                message="代码执行完成",
                passed_tests=passed_tests,
                total_tests=len(test_cases),
                results=results
            )
            
        except Exception as exc:
            return CodeExecutionResponse(
                status="error",
                message=f"代码执行错误: {str(exc)}",
                passed_tests=0,
                total_tests=len(test_cases),
                results=[]
            )
    
    @classmethod
    async def run_tests(cls, code: str, language: ProgrammingLanguage, test_cases: List[TestCase]) -> CodeExecutionResponse:
        """
        运行测试用例
        
        接收用户代码、编程语言和测试用例列表，执行代码并返回测试结果。
        会对每个测试用例单独执行，并收集执行结果。
        
        Args:
            code: 用户代码
            language: 编程语言
            test_cases: 测试用例列表
            
        Returns:
            CodeExecutionResponse: 执行结果，包含测试通过情况、执行时间和内存使用等信息
            
        Raises:
            ValueError: 如果不支持指定的编程语言
            Exception: 执行过程中的其他异常
        """
        executor = cls._executors.get(language)
        if not executor:
            raise ValueError(f"不支持的编程语言: {language}")
        
        # 对于Java语言，打印用户代码长度和内容以便调试
        if language == ProgrammingLanguage.JAVA:
            print(f"Java用户代码长度: {len(code)}")
            print(f"Java用户代码内容: {code[:100]}...")
            
            # 确保用户代码中有Solution类
            if "class Solution" not in code:
                code = f"""
                public class Solution {{
                    public Object solve(java.util.Map<String, Object> input) {{
                        // 默认实现
                        return null;
                    }}
                    
                    {code}
                }}
                """
            # 检查用户代码是否已经包含Solution类
            elif "class Solution" not in code and "public class Solution" not in code:
                # 检查用户代码是否已经包含其他类定义
                if "class " not in code and "public class " not in code:
                    # 如果用户代码不包含任何类定义，将其包装在Solution类中
                    code = f"""
                    public class Solution {{
                        {code}
                        
                        public Object solve(java.util.Map<String, Object> input) {{
                            // 默认实现，应该被用户代码覆盖
                            return null;
                        }}
                    }}
                    """
                # 否则，用户代码已经包含其他类定义，不进行包装
        
        test_code = CodeGenerator().generate_test_code(code, language, test_cases)
        
        # 对于Java语言，打印生成的测试代码长度以便调试
        if language == ProgrammingLanguage.JAVA:
            print(f"生成的Java测试代码长度: {len(test_code)}")
            print(f"生成的Java测试代码前100字符: {test_code[:100]}...")
        
        # 执行测试
        try:
            results = []
            passed_tests = 0
            
            for i, test_case in enumerate(test_cases):
                test_input = {
                    "input": test_case.input,
                    "expected_output": test_case.expected_output
                }
                
                # 执行代码
                output, execution_time, memory_usage = await executor.execute(test_code, test_input)
                
                # 检查结果
                if isinstance(output, dict) and "error" in output:
                    results.append(TestResult(
                        passed=False,
                        input=test_case.input,
                        expected_output=test_case.expected_output,
                        actual_output=None,
                        error=output["error"],
                        execution_time=execution_time,
                        memory_usage=memory_usage,
                        description=test_case.description
                    ))
                else:
                    passed = output == test_case.expected_output
                    if passed:
                        passed_tests += 1
                    
                    results.append(TestResult(
                        passed=passed,
                        input=test_case.input,
                        expected_output=test_case.expected_output,
                        actual_output=output,
                        execution_time=execution_time,
                        memory_usage=memory_usage,
                        description=test_case.description
                    ))
            
            return CodeExecutionResponse(
                status=ExecutionStatus.SUCCESS,
                test_results=results,
                total_tests=len(test_cases),
                passed_tests=passed_tests,
                execution_time=sum(r.execution_time for r in results),
                memory_usage=max((r.memory_usage for r in results), default=0)
            )
            
        except Exception as exc:
            return CodeExecutionResponse(
                status=ExecutionStatus.INTERNAL_ERROR,
                message=str(exc),
                total_tests=len(test_cases),
                passed_tests=0
            ) 
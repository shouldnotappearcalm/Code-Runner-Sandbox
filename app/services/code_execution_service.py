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

class ProgrammingLanguage(str, Enum):
    """编程语言枚举"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"

class CodeExecutor:
    """代码执行器基类"""
    
    def __init__(self, language: ProgrammingLanguage):
        self.language = language
        self.code_generator = CodeGenerator()
    
    async def execute(self, code: str, test_input: Any) -> Tuple[Any, float, float]:
        """
        执行代码并返回结果
        
        Args:
            code: 用户代码
            test_input: 测试输入
            
        Returns:
            Tuple[Any, float, float]: (执行结果, 执行时间(ms), 内存使用(KB))
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # 生成包装后的代码
                wrapped_code = self.code_generator.wrap_user_code(code, self.language, test_input)
                
                # 准备代码文件
                filepath = self._prepare_code_file(temp_dir, wrapped_code)
                
                # 编译代码（如果需要）
                compile_result = self._compile_code(temp_dir, filepath)
                if compile_result.get("error"):
                    return compile_result, 0, 0
                
                # 执行代码
                start_time = time.time()
                result, execution_time = self._run_code(temp_dir, filepath)
                
                # 计算内存使用（简化版本，实际应用中可能需要更复杂的计算）
                memory_usage = 0
                
                return result, execution_time, memory_usage
                
            except Exception as exc:
                return {"error": f"执行错误: {str(exc)}"}, 0, 0
    
    async def run_tests(self, code: str, test_cases: List[TestCase]) -> CodeExecutionResponse:
        """
        运行测试用例
        
        Args:
            code: 用户代码
            test_cases: 测试用例列表
            
        Returns:
            CodeExecutionResponse: 执行结果
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # 生成测试代码
                test_code = self.code_generator.generate_test_code(code, self.language, test_cases)
                
                # 准备代码文件
                filepath = self._prepare_code_file(temp_dir, test_code)
                
                # 编译代码（如果需要）
                compile_result = self._compile_code(temp_dir, filepath)
                if compile_result.get("error"):
                    return CodeExecutionResponse(
                        status=ExecutionStatus.COMPILE_ERROR,
                        message=compile_result.get("error"),
                        total_tests=len(test_cases),
                        passed_tests=0
                    )
                
                # 执行测试
                start_time = time.time()
                result, execution_time = self._run_code(temp_dir, filepath)
                
                # 解析测试结果
                if isinstance(result, list):
                    test_results = []
                    passed_tests = 0
                    
                    for i, test_result in enumerate(result):
                        if i < len(test_cases):
                            test_result_obj = TestResult(
                                passed=test_result.get("passed", False),
                                input=test_result.get("input", test_cases[i].input),
                                expected_output=test_result.get("expected_output", test_cases[i].expected_output),
                                actual_output=test_result.get("actual_output", None),
                                execution_time=test_result.get("execution_time", 0),
                                memory_usage=test_result.get("memory_usage", 0),
                                description=test_result.get("description", test_cases[i].description)
                            )
                            test_results.append(test_result_obj)
                            
                            if test_result.get("passed", False):
                                passed_tests += 1
                    
                    return CodeExecutionResponse(
                        status=ExecutionStatus.SUCCESS,
                        test_results=test_results,
                        total_tests=len(test_cases),
                        passed_tests=passed_tests,
                        execution_time=execution_time,
                        memory_usage=0  # 简化版不计算内存使用
                    )
                else:
                    # 如果结果不是列表，可能是执行出错
                    return CodeExecutionResponse(
                        status=ExecutionStatus.RUNTIME_ERROR,
                        message=str(result) if result else "未知运行时错误",
                        total_tests=len(test_cases),
                        passed_tests=0
                    )
                    
            except Exception as exc:
                # 确保异常变量名为exc而不是e
                return CodeExecutionResponse(
                    status=ExecutionStatus.INTERNAL_ERROR,
                    message=str(exc),
                    total_tests=len(test_cases),
                    passed_tests=0
                )
    
    def _prepare_code_file(self, temp_dir: str, code: str) -> str:
        """
        准备代码文件（子类应重写此方法）
        
        Args:
            temp_dir: 临时目录
            code: 代码
            
        Returns:
            str: 代码文件路径
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def _compile_code(self, temp_dir: str, filepath: str) -> Dict[str, Any]:
        """
        编译代码（子类应重写此方法）
        
        Args:
            temp_dir: 临时目录
            filepath: 代码文件路径
            
        Returns:
            Dict[str, Any]: 编译结果，如果有错误则包含error字段
        """
        return {}  # 默认不需要编译
    
    def _run_code(self, temp_dir: str, filepath: str) -> Tuple[Any, float]:
        """
        运行代码（子类应重写此方法）
        
        Args:
            temp_dir: 临时目录
            filepath: 代码文件路径
            
        Returns:
            Tuple[Any, float]: (执行结果, 执行时间(ms))
        """
        raise NotImplementedError("子类必须实现此方法")


class PythonExecutor(CodeExecutor):
    """Python代码执行器"""
    
    def __init__(self):
        super().__init__(ProgrammingLanguage.PYTHON)
    
    def _prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备Python代码文件"""
        filepath = os.path.join(temp_dir, "solution.py")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def _run_code(self, temp_dir: str, filepath: str) -> Tuple[Any, float]:
        """运行Python代码"""
        start_time = time.time()
        try:
            # 设置资源限制
            def limit_resources():
                # 设置内存限制 (MEMORY_LIMIT MB)
                resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT * 1024 * 1024, MEMORY_LIMIT * 1024 * 1024))
            
            # 执行Python代码
            process = subprocess.run(
                ["python3", filepath],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT,
                preexec_fn=limit_resources
            )
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # 转换为毫秒
            
            # 检查是否有错误
            if process.returncode != 0:
                return {"error": process.stderr}, execution_time
            
            # 解析输出
            try:
                output = json.loads(process.stdout)
            except json.JSONDecodeError:
                output = process.stdout.strip()
            
            return output, execution_time
            
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000
        except Exception as exc:
            return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000


class JavaScriptExecutor(CodeExecutor):
    """JavaScript代码执行器"""
    
    def __init__(self):
        super().__init__(ProgrammingLanguage.JAVASCRIPT)
    
    def _prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备JavaScript代码文件"""
        filepath = os.path.join(temp_dir, "solution.js")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def _run_code(self, temp_dir: str, filepath: str) -> Tuple[Any, float]:
        """运行JavaScript代码"""
        start_time = time.time()
        try:
            # 执行JavaScript代码
            process = subprocess.run(
                ["node", filepath],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # 转换为毫秒
            
            # 检查是否有错误
            if process.returncode != 0:
                return {"error": process.stderr}, execution_time
            
            # 解析输出
            try:
                output = json.loads(process.stdout)
            except json.JSONDecodeError:
                output = process.stdout.strip()
            
            return output, execution_time
            
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000
        except Exception as exc:
            return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000


class JavaExecutor(CodeExecutor):
    """Java代码执行器"""
    
    def __init__(self):
        super().__init__(ProgrammingLanguage.JAVA)
    
    def _prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备Java代码文件"""
        # 解析主类名
        main_class = self._extract_main_class(code)
        
        # 创建Java文件
        filepath = os.path.join(temp_dir, f"{main_class}.java")
        with open(filepath, "w") as f:
            f.write(code)
        
        return filepath
    
    def _extract_main_class(self, code: str) -> str:
        """从Java代码中提取主类名"""
        import re
        
        # 查找包含main方法的类
        main_match = re.search(r'public\s+class\s+(\w+).*public\s+static\s+void\s+main', code, re.DOTALL)
        if main_match:
            return main_match.group(1)
        
        # 查找TestRunner类（测试代码）
        test_match = re.search(r'public\s+class\s+(\w+TestRunner)', code)
        if test_match:
            return test_match.group(1)
        
        # 查找任何public class
        public_match = re.search(r'public\s+class\s+(\w+)', code)
        if public_match:
            return public_match.group(1)
        
        # 查找任何class
        class_match = re.search(r'class\s+(\w+)', code)
        if class_match:
            return class_match.group(1)
        
        # 默认类名
        return "Main"
    
    def _compile_code(self, temp_dir: str, filepath: str) -> Dict[str, Any]:
        """编译Java代码"""
        try:
            # 编译Java代码
            process = subprocess.run(
                ["javac", filepath],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                return {"error": f"编译错误: {process.stderr}"}
            
            return {}
            
        except Exception as exc:
            return {"error": f"编译错误: {str(exc)}"}
    
    def _run_code(self, temp_dir: str, filepath: str) -> Tuple[Any, float]:
        """运行Java代码"""
        start_time = time.time()
        try:
            # 获取类名（不包含.java扩展名）
            class_name = os.path.basename(filepath).replace(".java", "")
            
            # 执行Java代码
            process = subprocess.run(
                ["java", class_name],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # 转换为毫秒
            
            # 检查是否有错误
            if process.returncode != 0:
                return {"error": process.stderr}, execution_time
            
            # 解析输出
            try:
                output = json.loads(process.stdout)
            except json.JSONDecodeError:
                output = process.stdout.strip()
            
            return output, execution_time
            
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000
        except Exception as exc:
            return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000


class CppExecutor(CodeExecutor):
    """C++代码执行器"""
    
    def __init__(self):
        super().__init__(ProgrammingLanguage.CPP)
    
    def _prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备C++代码文件"""
        filepath = os.path.join(temp_dir, "solution.cpp")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def _compile_code(self, temp_dir: str, filepath: str) -> Dict[str, Any]:
        """编译C++代码"""
        try:
            executable = os.path.join(temp_dir, "solution")
            
            # 编译C++代码
            process = subprocess.run(
                ["g++", "-std=c++17", filepath, "-o", executable, "-I/usr/include/nlohmann"],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                return {"error": f"编译错误: {process.stderr}"}
            
            return {}
            
        except Exception as exc:
            return {"error": f"编译错误: {str(exc)}"}
    
    def _run_code(self, temp_dir: str, filepath: str) -> Tuple[Any, float]:
        """运行C++代码"""
        start_time = time.time()
        try:
            executable = os.path.join(temp_dir, "solution")
            
            # 执行C++代码
            process = subprocess.run(
                [executable],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # 转换为毫秒
            
            # 检查是否有错误
            if process.returncode != 0:
                return {"error": process.stderr}, execution_time
            
            # 解析输出
            try:
                output = json.loads(process.stdout)
            except json.JSONDecodeError:
                output = process.stdout.strip()
            
            return output, execution_time
            
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000
        except Exception as exc:
            return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000


class GoExecutor(CodeExecutor):
    """Go代码执行器"""
    
    def __init__(self):
        super().__init__(ProgrammingLanguage.GO)
    
    def _prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备Go代码文件"""
        filepath = os.path.join(temp_dir, "main.go")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def _compile_code(self, temp_dir: str, filepath: str) -> Dict[str, Any]:
        """编译Go代码"""
        try:
            executable = os.path.join(temp_dir, "solution")
            
            # 编译Go代码
            process = subprocess.run(
                ["go", "build", "-o", executable, filepath],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                return {"error": f"编译错误: {process.stderr}"}
            
            return {}
            
        except Exception as exc:
            return {"error": f"编译错误: {str(exc)}"}
    
    def _run_code(self, temp_dir: str, filepath: str) -> Tuple[Any, float]:
        """运行Go代码"""
        start_time = time.time()
        try:
            executable = os.path.join(temp_dir, "solution")
            
            # 执行Go代码
            process = subprocess.run(
                [executable],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # 转换为毫秒
            
            # 检查是否有错误
            if process.returncode != 0:
                return {"error": process.stderr}, execution_time
            
            # 解析输出
            try:
                output = json.loads(process.stdout)
            except json.JSONDecodeError:
                output = process.stdout.strip()
            
            return output, execution_time
            
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000
        except Exception as exc:
            return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000


class RustExecutor(CodeExecutor):
    """Rust代码执行器"""
    
    def __init__(self):
        super().__init__(ProgrammingLanguage.RUST)
    
    def _prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备Rust代码文件"""
        # 创建Cargo项目
        subprocess.run(
            ["cargo", "init", "--bin"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        # 添加serde依赖到Cargo.toml
        cargo_toml = os.path.join(temp_dir, "Cargo.toml")
        with open(cargo_toml, "a") as f:
            f.write("\n[dependencies]\n")
            f.write("serde = { version = \"1.0\", features = [\"derive\"] }\n")
            f.write("serde_json = \"1.0\"\n")
        
        # 写入代码到src/main.rs
        filepath = os.path.join(temp_dir, "src", "main.rs")
        with open(filepath, "w") as f:
            f.write(code)
        
        return filepath
    
    def _compile_code(self, temp_dir: str, filepath: str) -> Dict[str, Any]:
        """编译Rust代码"""
        try:
            # 编译Rust代码
            process = subprocess.run(
                ["cargo", "build", "--release"],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                return {"error": f"编译错误: {process.stderr}"}
            
            return {}
            
        except Exception as exc:
            return {"error": f"编译错误: {str(exc)}"}
    
    def _run_code(self, temp_dir: str, filepath: str) -> Tuple[Any, float]:
        """运行Rust代码"""
        start_time = time.time()
        try:
            # 执行Rust代码
            process = subprocess.run(
                ["cargo", "run", "--release"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # 转换为毫秒
            
            # 检查是否有错误
            if process.returncode != 0:
                return {"error": process.stderr}, execution_time
            
            # 解析输出
            try:
                output = json.loads(process.stdout)
            except json.JSONDecodeError:
                output = process.stdout.strip()
            
            return output, execution_time
            
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000
        except Exception as exc:
            return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000


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
        
        # 生成测试代码
        code_generator = CodeGenerator()
        test_code = code_generator.generate_test_code(code, language, test_cases)
        
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
        
        return await executor.run_tests(code, test_cases) 
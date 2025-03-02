import os
import subprocess
import tempfile
import time
from typing import Any, Tuple
from app.executors.base_executor import BaseExecutor, EXECUTION_TIMEOUT


class SwiftExecutor(BaseExecutor):
    """Swift代码执行器"""

    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        filepath = os.path.join(temp_dir, "main.swift")
        with open(filepath, "w") as f:
            f.write(code)  # Swift不需要main函数包装
        return filepath

    def get_compile_command(self, filepath: str) -> str:
        """获取编译命令"""
        output_dir = os.path.dirname(filepath)
        return f"swiftc {filepath} -o {os.path.join(output_dir, 'solution')}"

    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        return os.path.join(os.path.dirname(filepath), "solution")

    async def execute(self, code: str, test_input: Any) -> Tuple[Any, float, float]:
        """
        执行Swift代码

        Args:
            code: 用户代码
            test_input: 测试输入（在直接执行模式下不使用）

        Returns:
            Tuple[Any, float, float]: (执行结果, 执行时间(ms), 内存使用(KB))
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # 准备代码文件
            filepath = self.prepare_code_file(temp_dir, code)

            # 编译代码
            compile_process = subprocess.run(
                self.get_compile_command(filepath),
                shell=True,
                cwd=temp_dir,
                capture_output=True,
                text=True
            )

            if compile_process.returncode != 0:
                return {"error": f"编译错误: {compile_process.stderr}"}, 0, 0

            # 执行代码
            start_time = time.time()
            try:
                process = subprocess.run(
                    self.get_execute_command(filepath),
                    shell=True,
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=EXECUTION_TIMEOUT
                )

                execution_time = (time.time() - start_time) * 1000  # 转换为毫秒

                if process.returncode != 0:
                    return {"error": f"执行错误: {process.stderr}"}, execution_time, 0

                # 合并 stdout 和 stderr 的输出
                output = process.stdout.strip()
                if process.stderr:
                    if output:
                        output += "\n"
                    output += process.stderr.strip()

                # 返回执行结果
                return output, execution_time, 0

            except subprocess.TimeoutExpired:
                return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000, 0
            except Exception as e:
                return {"error": f"执行错误: {str(e)}"}, (time.time() - start_time) * 1000, 0 
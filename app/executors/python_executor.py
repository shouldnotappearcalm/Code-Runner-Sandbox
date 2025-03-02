import os
import subprocess
import tempfile
import time
import platform
from typing import Any, Tuple
from app.executors.base_executor import BaseExecutor, EXECUTION_TIMEOUT

class PythonExecutor(BaseExecutor):
    """Python代码执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        filepath = os.path.join(temp_dir, "solution.py")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        return f"python3 {filepath}"
    
    async def execute(self, code: str, test_input: Any) -> Tuple[Any, float, float]:
        """
        执行代码
        
        Args:
            code: 用户代码
            test_input: 测试输入（在直接执行模式下不使用）
            
        Returns:
            Tuple[Any, float, float]: (执行结果, 执行时间(ms), 内存使用(KB))
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # 准备代码文件
            filepath = self.prepare_code_file(temp_dir, code)
            
            # 执行代码
            start_time = time.time()
            try:
                # 在非macOS系统上设置资源限制
                kwargs = {}

                process = subprocess.run(
                    self.get_execute_command(filepath),
                    shell=True,
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=EXECUTION_TIMEOUT,
                    **kwargs
                )
                
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000  # 转换为毫秒
                
                if process.stderr:
                    return {"error": process.stderr}, execution_time, 0
                
                # 返回输出
                return process.stdout.strip(), execution_time, 0  # 简化版不计算内存使用
                
            except subprocess.TimeoutExpired:
                return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000, 0
            except Exception as exc:
                return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000, 0 
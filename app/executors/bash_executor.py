import os
import subprocess
import tempfile
import time
from typing import Any, Tuple
from app.executors.base_executor import BaseExecutor, EXECUTION_TIMEOUT

class BashExecutor(BaseExecutor):
    """Bash脚本执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        filepath = os.path.join(temp_dir, "script.sh")
        with open(filepath, "w") as f:
            f.write("#!/bin/bash\n")  # 添加 shebang
            f.write(code)
        # 设置可执行权限
        os.chmod(filepath, 0o755)
        return filepath
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        return filepath  # 直接执行脚本文件，因为我们已经设置了可执行权限
    
    async def execute(self, code: str, test_input: Any) -> Tuple[Any, float, float]:
        """
        执行Bash脚本
        
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
                
                # 返回执行结果
                return process.stdout.strip(), execution_time, 0
                
            except subprocess.TimeoutExpired:
                return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000, 0
            except Exception as e:
                return {"error": f"执行错误: {str(e)}"}, (time.time() - start_time) * 1000, 0 
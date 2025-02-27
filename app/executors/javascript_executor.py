import os
from app.executors.base_executor import BaseExecutor

class JavaScriptExecutor(BaseExecutor):
    """JavaScript代码执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        filepath = os.path.join(temp_dir, "solution.js")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        return f"node {filepath}" 
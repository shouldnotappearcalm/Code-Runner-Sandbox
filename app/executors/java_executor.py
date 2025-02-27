import os
from app.executors.base_executor import BaseExecutor

class JavaExecutor(BaseExecutor):
    """Java代码执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        filepath = os.path.join(temp_dir, "Solution.java")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def get_compile_command(self, filepath: str) -> str:
        """获取编译命令"""
        return f"javac {filepath}"
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        directory = os.path.dirname(filepath)
        return f"cd {directory} && java Solution" 
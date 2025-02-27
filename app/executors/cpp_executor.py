import os
from app.executors.base_executor import BaseExecutor

class CppExecutor(BaseExecutor):
    """C++代码执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        filepath = os.path.join(temp_dir, "solution.cpp")
        with open(filepath, "w") as f:
            f.write(code)
        return filepath
    
    def get_compile_command(self, filepath: str) -> str:
        """获取编译命令"""
        output_path = os.path.join(os.path.dirname(filepath), "solution")
        return f"g++ -std=c++17 -I/usr/include/nlohmann -o {output_path} {filepath}"
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        output_path = os.path.join(os.path.dirname(filepath), "solution")
        return f"{output_path}" 
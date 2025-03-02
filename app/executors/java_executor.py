import os
import subprocess
import tempfile
import time
import platform
from typing import Any, Tuple
from app.executors.base_executor import BaseExecutor, EXECUTION_TIMEOUT

class JavaExecutor(BaseExecutor):
    """Java代码执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件，将代码写入Main.java"""
        filepath = os.path.join(temp_dir, "Main.java")
        with open(filepath, "w") as f:
            # 如果代码中没有定义Main类，则添加包装
            if "class Main" not in code:
                code = f"""
public class Main {{
    public static void main(String[] args) {{
        {code}
    }}
}}
"""
            else:
                # 确保类名为Main
                code = code.replace("public class Solution", "public class Main")
                code = code.replace("class Solution", "public class Main")
            f.write(code)
        return filepath
    
    def get_compile_command(self, filepath: str) -> str:
        """获取编译命令"""
        return f"javac {filepath}"
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        # 获取包含编译后的.class文件的目录
        directory = os.path.dirname(filepath)
        return f"java -Xmx{EXECUTION_TIMEOUT}M -cp {directory} Main"
    
    async def execute(self, code: str, test_input: Any) -> Tuple[Any, float, float]:
        """
        执行Java代码
        
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
                return process.stdout.strip(), execution_time, 0
                
            except subprocess.TimeoutExpired:
                return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000, 0
            except Exception as exc:
                return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000, 0 
import os
import time
import tempfile
import subprocess
import json
from typing import Any, Tuple

# 执行超时时间（秒）
EXECUTION_TIMEOUT = 1000
# 内存限制（MB）
MEMORY_LIMIT = 512

class BaseExecutor:
    """基础执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        raise NotImplementedError
    
    def get_compile_command(self, filepath: str) -> str:
        """获取编译命令"""
        return None
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        raise NotImplementedError
    
    async def execute(self, code: str, test_input: Any) -> Tuple[Any, float, float]:
        """
        执行代码
        
        Args:
            code: 用户代码
            test_input: 测试输入
            
        Returns:
            Tuple[Any, float, float]: (执行结果, 执行时间(ms), 内存使用(KB))
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # 准备代码文件
            filepath = self.prepare_code_file(temp_dir, code)
            
            # 写入输入文件
            input_file = os.path.join(temp_dir, "input.json")
            with open(input_file, "w") as f:
                json.dump(test_input, f)
            
            # 编译代码（如果需要）
            compile_cmd = self.get_compile_command(filepath)
            if compile_cmd:
                compile_process = subprocess.run(
                    compile_cmd, 
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
                # 设置资源限制
                def limit_resources():
                    # 设置内存限制 (MEMORY_LIMIT MB)
                    import resource
                    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT * 1024 * 1024, MEMORY_LIMIT * 1024 * 1024))
                
                execute_cmd = self.get_execute_command(filepath)
                process = subprocess.run(
                    execute_cmd,
                    shell=True,
                    cwd=temp_dir,
                    input=open(input_file, "r").read(),
                    capture_output=True,
                    text=True,
                    timeout=EXECUTION_TIMEOUT,
                    preexec_fn=limit_resources
                )
                
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000  # 转换为毫秒
                
                # 解析输出
                try:
                    output = json.loads(process.stdout)
                except:
                    output = process.stdout.strip()
                
                return output, execution_time, 0  # 简化版不计算内存使用
                
            except subprocess.TimeoutExpired:
                return {"error": "执行超时"}, EXECUTION_TIMEOUT * 1000, 0
            except Exception as exc:
                return {"error": f"执行错误: {str(exc)}"}, (time.time() - start_time) * 1000, 0 
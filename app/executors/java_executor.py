import os
import re
import tempfile
from app.executors.base_executor import BaseExecutor

class JavaExecutor(BaseExecutor):
    """Java代码执行器"""
    
    def prepare_code_file(self, temp_dir: str, code: str) -> str:
        """准备代码文件"""
        # 检查代码中是否包含Solution类
        has_solution = "class Solution" in code or "public class Solution" in code
        
        # 检查代码中是否包含TestRunner类
        has_test_runner = "class TestRunner" in code or "public class TestRunner" in code
        
        # 打印调试信息
        print(f"Java代码长度: {len(code)}")
        print(f"代码包含Solution类: {has_solution}")
        print(f"代码包含TestRunner类: {has_test_runner}")
        
        # 如果代码中包含TestRunner类，直接写入TestRunner.java
        if has_test_runner:
            filepath = os.path.join(temp_dir, "TestRunner.java")
            with open(filepath, "w") as f:
                f.write(code)
                
            # 打印文件内容用于调试
            with open(filepath, "r") as f:
                file_content = f.read()
                print(f"写入的TestRunner.java文件内容 (长度: {len(file_content)}):\n{file_content}")
                
            return filepath
        
        # 如果代码中包含Solution类，需要创建单独的Solution.java文件
        if has_solution and not has_test_runner:
            # 提取Solution类的代码
            solution_pattern = re.compile(r'(public\s+)?class\s+Solution\s*\{.*?\}', re.DOTALL)
            solution_match = solution_pattern.search(code)
            
            if solution_match:
                solution_code = solution_match.group(0)
                
                # 提取导入语句
                import_lines = []
                for line in code.split('\n'):
                    if line.strip().startswith("import "):
                        import_lines.append(line)
                
                # 创建Solution.java文件
                solution_filepath = os.path.join(temp_dir, "Solution.java")
                with open(solution_filepath, "w") as f:
                    # 写入导入语句
                    for import_line in import_lines:
                        f.write(import_line + "\n")
                    
                    # 写入Solution类代码
                    f.write(solution_code)
                
                # 打印文件内容用于调试
                with open(solution_filepath, "r") as f:
                    file_content = f.read()
                    print(f"写入的Solution.java文件内容 (长度: {len(file_content)}):\n{file_content}")
                
                return solution_filepath
        
        # 默认情况：提取主类名并创建对应的Java文件
        main_class = self._extract_main_class(code)
        filepath = os.path.join(temp_dir, f"{main_class}.java")
        
        # 写入代码到文件
        with open(filepath, "w") as f:
            f.write(code)
        
        # 打印文件内容用于调试
        with open(filepath, "r") as f:
            file_content = f.read()
            print(f"写入的{main_class}.java文件内容 (长度: {len(file_content)}):\n{file_content}")
        
        return filepath
    
    def _extract_main_class(self, code: str) -> str:
        """从Java代码中提取主类名"""
        # 查找TestRunner类（测试代码）
        if "public class TestRunner" in code or "class TestRunner" in code:
            return "TestRunner"
        
        # 查找Main类（包装器代码）
        if "public class Main" in code or "class Main" in code:
            return "Main"
        
        # 查找Solution类
        if "public class Solution" in code or "class Solution" in code:
            return "Solution"
        
        # 查找任何public class
        public_match = re.search(r'public\s+class\s+(\w+)', code)
        if public_match:
            return public_match.group(1)
        
        # 查找任何class
        class_match = re.search(r'class\s+(\w+)', code)
        if class_match:
            return class_match.group(1)
        
        # 默认类名
        return "Solution"
    
    def get_compile_command(self, filepath: str) -> str:
        """获取编译命令"""
        directory = os.path.dirname(filepath)
        # 编译目录中的所有Java文件，添加-verbose参数查看编译详情
        return f"cd {directory} && javac -Xlint:none -verbose *.java"
    
    def get_execute_command(self, filepath: str) -> str:
        """获取执行命令"""
        directory = os.path.dirname(filepath)
        
        # 检查是否存在TestRunner.java文件
        if os.path.exists(os.path.join(directory, "TestRunner.java")):
            return f"cd {directory} && java TestRunner"
        
        # 检查是否存在Main.java文件
        if os.path.exists(os.path.join(directory, "Main.java")):
            return f"cd {directory} && java Main"
        
        # 获取文件名（不含扩展名）
        filename = os.path.basename(filepath)
        main_class = os.path.splitext(filename)[0]
        
        # 默认使用文件名对应的类作为入口点
        return f"cd {directory} && java {main_class}" 
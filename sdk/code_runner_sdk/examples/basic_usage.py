"""
基础使用示例

展示Code Runner SDK的基本功能：
1. 初始化客户端
2. 运行简单代码
3. 执行带测试用例的代码
4. 错误处理
"""
import sys
import os

# 添加父目录到Python路径，以便能够导入SDK
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from code_runner_sdk.core.client import (
    CodeRunnerClient,
    ProgrammingLanguage,
    TestCase
)
from code_runner_sdk.exceptions import APIError, ValidationError


def run_simple_code():
    """运行简单的代码示例"""
    print("\n1. 运行简单的Python代码")
    print("-" * 50)
    
    client = CodeRunnerClient(
        host="localhost",
        port=8000
    )
    
    # 运行Hello World
    try:
        result = client.run_code(
            code='print("Hello, Code Runner!")',
            language=ProgrammingLanguage.PYTHON
        )
        print("代码输出:")
        print(f"输出内容: {result['output']}")
        print(f"执行时间: {result['execution_time']}ms")
        print(f"内存使用: {result['memory_usage']}KB")
    except APIError as e:
        print(f"API错误: {e}")


def run_multi_language_example():
    """多语言代码执行示例"""
    print("\n3. 多语言代码执行示例")
    print("-" * 50)
    
    client = CodeRunnerClient(
        host="localhost",
        port=8000
    )
    
    # 准备不同语言的代码
    code_samples = {
        ProgrammingLanguage.PYTHON: 'print("Hello from Python!")',
        ProgrammingLanguage.JAVASCRIPT: 'console.log("Hello from JavaScript!");',
        ProgrammingLanguage.GO: 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello from Go!")\n}',
    }
    
    for language, code in code_samples.items():
        print(f"\n执行 {language} 代码:")
        try:
            result = client.run_code(code=code, language=language)
            print(f"输出: {result['output']}")
            print(f"执行时间: {result['execution_time']}ms")
            print(f"内存使用: {result['memory_usage']}KB")
        except APIError as e:
            print(f"执行失败: {e}")


def main():
    """运行所有示例"""
    print("Code Runner SDK 使用示例")
    print("=" * 50)
    
    try:
        run_simple_code()
        run_multi_language_example()
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# 简单的测试用例
test_cases = [
    {
        "input": {"value": 42},
        "expected_output": 42,
        "description": "Test case"
    }
]

# 用户代码
user_code = """
public class Solution {
    public Object solve(java.util.Map<String, Object> input) {
        return input.get("value");
    }
}
"""

# 设置Jinja2环境
template_dir = Path(__file__).parent / "app" / "templates"
env = Environment(loader=FileSystemLoader(template_dir))

# 尝试加载模板
try:
    # 检查模板目录是否存在
    if not template_dir.exists():
        print(f"错误: 模板目录不存在: {template_dir}")
        sys.exit(1)
        
    # 列出模板目录中的文件
    print(f"模板目录内容: {list(template_dir.glob('*'))}")
    
    template = env.get_template("java_test_template.jinja2")
    
    # 渲染模板
    rendered_code = template.render(
        user_code=user_code,
        test_cases=test_cases
    )
    
    # 打印渲染结果
    print("渲染结果:")
    print("-" * 50)
    print(rendered_code)
    print("-" * 50)
    
    # 检查用户代码是否在渲染结果中
    if user_code.strip() in rendered_code:
        print("用户代码已成功渲染到模板中")
    else:
        print("警告: 用户代码可能没有正确渲染")
        
        # 查找用户代码的部分内容
        code_snippet = "public class Solution"
        if code_snippet in rendered_code:
            print(f"但找到了部分用户代码: '{code_snippet}'")
        
        # 检查模板中的条件语句
        if "{% if" in rendered_code:
            print("警告: 模板条件语句未被处理")
            
except Exception as e:
    print(f"错误: {str(e)}") 
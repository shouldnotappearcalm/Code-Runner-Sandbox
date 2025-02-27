import os
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

try:
    from app.schemas.code_execution import ProgrammingLanguage, TestCase
except ImportError:
    # 当在app目录下运行时，使用相对导入
    from schemas.code_execution import ProgrammingLanguage, TestCase


class CodeGenerator:
    """代码生成器，用于生成各种语言的测试代码"""
    
    def __init__(self):
        # 获取模板目录
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # 注册自定义过滤器
        self.env.filters['tojson'] = self._to_json
    
    def _to_json(self, value):
        """将值转换为JSON字符串，处理特殊字符"""
        import json
        return json.dumps(value)
    
    def generate_test_code(
        self, 
        user_code: str, 
        language: ProgrammingLanguage, 
        test_cases: List[TestCase]
    ) -> str:
        """
        生成测试代码
        
        Args:
            user_code: 用户代码
            language: 编程语言
            test_cases: 测试用例列表
            
        Returns:
            str: 生成的测试代码
        """
        # 获取对应语言的模板
        template_name = f"{language.value}_test_template.jinja2"
        
        try:
            template = self.env.get_template(template_name)
        except Exception as exc:
            raise ValueError(f"不支持的编程语言模板: {language.value}, 错误: {str(exc)}")
        
        # 打印用户代码用于调试
        if language == ProgrammingLanguage.JAVA:
            print(f"用户代码 (长度: {len(user_code)}):\n{user_code}")
            
        # 渲染模板
        test_code = template.render(
            user_code=user_code,
            test_cases=test_cases
        )
        
        # 打印生成的测试代码用于调试
        if language == ProgrammingLanguage.JAVA:
            print(f"生成的Java测试代码 (长度: {len(test_code)}):\n{test_code}")
            
            # 检查用户代码是否在生成的测试代码中
            if user_code.strip() in test_code:
                print("用户代码已成功包含在生成的测试代码中")
            else:
                print("警告: 用户代码可能没有正确包含在生成的测试代码中")
                
                # 检查用户代码的一部分是否在生成的测试代码中
                if "public class Solution" in user_code and "public class Solution" in test_code:
                    print("但找到了Solution类定义")
        
        return test_code
    
    def wrap_user_code(self, user_code: str, language: ProgrammingLanguage, test_input: Any) -> str:
        """
        包装用户代码，使其能够接收输入并输出结果
        
        Args:
            user_code: 用户代码
            language: 编程语言
            test_input: 测试输入
            
        Returns:
            str: 包装后的代码
        """
        # 获取对应语言的模板
        template_name = f"{language.value}_wrapper_template.jinja2"
        
        try:
            template = self.env.get_template(template_name)
        except Exception as exc:
            raise ValueError(f"不支持的编程语言模板: {language.value}, 错误: {str(exc)}")
        
        # 渲染模板
        return template.render(
            user_code=user_code,
            test_input=test_input
        )
    
    def get_supported_languages(self) -> List[ProgrammingLanguage]:
        """
        获取支持的编程语言列表
        
        Returns:
            List[ProgrammingLanguage]: 支持的编程语言列表
        """
        # 查找所有 *_wrapper_template.jinja2 文件
        template_dir = Path(__file__).parent.parent / "templates"
        wrapper_templates = list(template_dir.glob("*_wrapper_template.jinja2"))
        
        # 提取语言名称
        languages = []
        for template in wrapper_templates:
            language_name = template.name.split("_")[0]
            try:
                language = ProgrammingLanguage(language_name)
                languages.append(language)
            except ValueError:
                # 忽略无效的语言名称
                pass
        
        return languages 
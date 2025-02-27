#!/usr/bin/env python3

import sys
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# 用户代码示例
user_code = """import java.util.HashMap;
import java.util.Map;

/**
 * 两数之和问题解决方案
 */
public class Solution {
    /**
     * 解决两数之和问题
     * @param problem 包含输入数据的对象
     * @return 结果数组
     */
    public int[] solve(Map<String, Object> problem) {
        // 获取输入数据
        int[] nums = convertToIntArray(problem.get("nums"));
        int target = ((Number) problem.get("target")).intValue();
        
        // 使用哈希表解决两数之和问题
        Map<Integer, Integer> numMap = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (numMap.containsKey(complement)) {
                return new int[] { numMap.get(complement), i };
            }
            numMap.put(nums[i], i);
        }
        
        return new int[0];  // 没有找到解
    }
    
    /**
     * 辅助方法：将Object转换为int数组
     */
    private int[] convertToIntArray(Object obj) {
        if (obj instanceof java.util.List) {
            java.util.List<?> list = (java.util.List<?>) obj;
            int[] result = new int[list.size()];
            for (int i = 0; i < list.size(); i++) {
                result[i] = ((Number) list.get(i)).intValue();
            }
            return result;
        }
        return new int[0];
    }
}"""

# 简单的测试用例
test_cases = [
    {
        "input": {"nums": [2, 7, 11, 15], "target": 9},
        "expected_output": [0, 1],
        "description": "示例测试用例"
    }
]

# 设置Jinja2环境
template_dir = Path(__file__).parent / "app" / "templates"
env = Environment(loader=FileSystemLoader(template_dir))

# 尝试加载模板
try:
    # 检查模板目录是否存在
    if not template_dir.exists():
        print(f"错误: 模板目录不存在: {template_dir}")
        sys.exit(1)
    
    template = env.get_template("java_test_template.jinja2")
    
    # 分析用户代码
    import_lines = []
    code_lines = []
    
    print("分析用户代码:")
    for line in user_code.split('\n'):
        if line.strip().startswith("import "):
            import_lines.append(line)
            print(f"导入语句: {line}")
        else:
            code_lines.append(line)
            print(f"代码行: {line}")
    
    print(f"\n导入语句数量: {len(import_lines)}")
    print(f"代码行数量: {len(code_lines)}")
    
    # 渲染模板
    rendered_code = template.render(
        user_code=user_code,
        test_cases=test_cases
    )
    
    # 打印渲染结果
    print("\n渲染结果:")
    print("-" * 50)
    print(rendered_code)
    print("-" * 50)
    
    # 检查用户代码是否在渲染结果中
    if "public class Solution" in rendered_code:
        print("Solution类已成功渲染到模板中")
    else:
        print("警告: Solution类可能没有正确渲染")
    
    # 检查导入语句是否在渲染结果中
    for import_line in import_lines:
        if import_line in rendered_code:
            print(f"导入语句已渲染: {import_line}")
    
    # 检查代码行是否在渲染结果中
    code_sample = "public int[] solve(Map<String, Object> problem)"
    if code_sample in rendered_code:
        print(f"代码行已渲染: {code_sample}")
    else:
        print(f"警告: 代码行未渲染: {code_sample}")
    
except Exception as e:
    print(f"错误: {str(e)}") 
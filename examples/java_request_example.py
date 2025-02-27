import requests
import json

# API 端点
API_URL = "http://localhost:8000/code/execute"

# 用户代码 - Java版本的两数之和
user_code = """
import java.util.HashMap;
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
}
"""

# 测试用例
test_cases = [
    {
        "input": {
            "nums": [2, 7, 11, 15],
            "target": 9
        },
        "expected_output": [0, 1],
        "description": "示例 1: 目标和为 9"
    },
    {
        "input": {
            "nums": [3, 2, 4],
            "target": 6
        },
        "expected_output": [1, 2],
        "description": "示例 2: 目标和为 6"
    },
    {
        "input": {
            "nums": [3, 3],
            "target": 6
        },
        "expected_output": [0, 1],
        "description": "示例 3: 相同元素"
    }
]

# 构建请求
request_data = {
    "code": user_code,
    "language": "java",
    "problem_id": "two-sum-java",
    "test_cases": test_cases
}

# 发送请求
response = requests.post(API_URL, json=request_data)

# 打印结果
print("状态码:", response.status_code)
print("响应内容:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 检查是否所有测试都通过
if response.status_code == 200:
    result = response.json()
    if result["passed_tests"] == result["total_tests"]:
        print("\n✅ 所有测试通过!")
    else:
        print(f"\n❌ 通过了 {result['passed_tests']}/{result['total_tests']} 个测试")
        
        # 打印失败的测试
        for i, test_result in enumerate(result["test_results"]):
            if not test_result["passed"]:
                print(f"\n失败的测试 #{i+1}:")
                print(f"  输入: {test_result['input']}")
                print(f"  期望输出: {test_result['expected_output']}")
                print(f"  实际输出: {test_result['actual_output']}")
else:
    print("\n❌ 请求失败") 
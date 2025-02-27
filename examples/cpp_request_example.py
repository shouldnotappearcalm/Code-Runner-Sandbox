import requests
import json

# API 端点
API_URL = "http://localhost:8000/code/execute"

# 用户代码 - C++版本的两数之和
user_code = """
#include <vector>
#include <unordered_map>
#include <iostream>
#include <string>
#include <nlohmann/json.hpp>

// 定义宏，避免模板中重复定义Solution类
#define SOLUTION_CLASS_DEFINED

using json = nlohmann::json;

/**
 * 两数之和问题解决方案
 */
class Solution {
public:
    /**
     * 解决两数之和问题
     * @param problem 包含输入数据的JSON对象
     * @return 结果数组
     */
    json solve(const json& problem) {
        try {
            // 获取输入数据
            std::vector<int> nums = problem["nums"].get<std::vector<int>>();
            int target = problem["target"].get<int>();
            
            // 使用哈希表解决两数之和问题
            std::unordered_map<int, int> numMap;
            for (int i = 0; i < nums.size(); i++) {
                int complement = target - nums[i];
                if (numMap.find(complement) != numMap.end()) {
                    return json::array({numMap[complement], i});
                }
                numMap[nums[i]] = i;
            }
            
            return json::array();  // 没有找到解
        } catch (const std::exception& e) {
            // 捕获并处理异常
            json error = {{"error", std::string(e.what())}};
            return error;
        }
    }
};

// 主函数：读取输入，调用解决方案，输出结果
int main() {
    // 从标准输入读取JSON
    json input;
    std::cin >> input;
    
    // 创建解决方案实例并调用
    Solution solution;
    auto result = solution.solve(input);
    
    // 将结果转换为JSON并输出
    json output = result;
    std::cout << output << std::endl;
    
    return 0;
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
    "language": "cpp",
    "problem_id": "two-sum-cpp",
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
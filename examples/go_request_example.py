import requests
import json

# API 端点
API_URL = "http://localhost:8000/code/execute"

# 用户代码 - Go版本的两数之和
user_code = """
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

// 解决两数之和问题
func solve(problem map[string]interface{}) []int {
	// 获取输入数据
	nums := make([]int, 0)
	for _, v := range problem["nums"].([]interface{}) {
		nums = append(nums, int(v.(float64)))
	}
	target := int(problem["target"].(float64))

	// 使用哈希表解决两数之和问题
	numMap := make(map[int]int)
	for i, num := range nums {
		complement := target - num
		if idx, found := numMap[complement]; found {
			return []int{idx, i}
		}
		numMap[num] = i
	}

	return []int{} // 没有找到解
}

func main() {
	// 从标准输入读取JSON
	input, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		fmt.Fprintf(os.Stderr, "读取输入错误: %v\\n", err)
		os.Exit(1)
	}

	// 解析JSON
	var problem map[string]interface{}
	if err := json.Unmarshal(input, &problem); err != nil {
		fmt.Fprintf(os.Stderr, "解析JSON错误: %v\\n", err)
		os.Exit(1)
	}

	// 调用解决方案
	result := solve(problem)

	// 输出结果
	output, err := json.Marshal(result)
	if err != nil {
		fmt.Fprintf(os.Stderr, "序列化结果错误: %v\\n", err)
		os.Exit(1)
	}

	fmt.Println(string(output))
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
    "language": "go",
    "problem_id": "two-sum-go",
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
import requests
import json

# API 端点
API_URL = "http://localhost:8000/code/execute"

# 用户代码 - Rust版本的两数之和
user_code = """
use std::collections::HashMap;
use std::io::{self, Read};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};

#[derive(Deserialize, Debug)]
struct Problem {
    nums: Vec<i32>,
    target: i32,
}

#[derive(Serialize, Debug)]
struct Solution;

impl Solution {
    /// 解决两数之和问题
    fn solve(problem: &Value) -> Value {
        // 解析输入数据
        let problem: Problem = match serde_json::from_value(problem.clone()) {
            Ok(p) => p,
            Err(e) => return json!({"error": format!("解析输入错误: {}", e)}),
        };
        
        // 使用哈希表解决两数之和问题
        let mut num_map = HashMap::new();
        for (i, &num) in problem.nums.iter().enumerate() {
            let complement = problem.target - num;
            if let Some(&idx) = num_map.get(&complement) {
                return json!([idx, i]);
            }
            num_map.insert(num, i);
        }
        
        // 没有找到解
        json!([])
    }
}

fn main() {
    // 从标准输入读取JSON
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("读取输入失败");
    
    // 解析JSON
    let problem: Value = match serde_json::from_str(&input) {
        Ok(p) => p,
        Err(e) => {
            eprintln!("解析JSON错误: {}", e);
            return;
        }
    };
    
    // 调用解决方案
    let result = Solution::solve(&problem);
    
    // 输出结果
    println!("{}", result);
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
    "language": "rust",
    "problem_id": "two-sum-rust",
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
const axios = require('axios');

// API 端点
const API_URL = 'http://localhost:8000/code/execute';

// 用户代码 - 回文字符串检查
const userCode = `
class Solution {
  solve(str) {
    // 移除非字母数字字符并转为小写
    const cleanStr = str.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
    
    // 检查是否为回文
    const len = cleanStr.length;
    for (let i = 0; i < len / 2; i++) {
      if (cleanStr[i] !== cleanStr[len - 1 - i]) {
        return false;
      }
    }
    
    return true;
  }
}
`;

// 测试用例
const testCases = [
  {
    input: 'A man, a plan, a canal: Panama',
    expected_output: true,
    description: '示例 1: 标准回文句子'
  },
  {
    input: 'race a car',
    expected_output: false,
    description: '示例 2: 非回文句子'
  },
  {
    input: ' ',
    expected_output: true,
    description: '示例 3: 空白字符'
  },
  {
    input: 'Madam, I\'m Adam.',
    expected_output: true,
    description: '示例 4: 另一个回文句子'
  }
];

// 构建请求
const requestData = {
  code: userCode,
  language: 'javascript',
  problem_id: 'palindrome-string',
  test_cases: testCases
};

// 发送请求
async function runTests() {
  try {
    const response = await axios.post(API_URL, requestData);
    
    // 打印结果
    console.log('状态码:', response.status);
    console.log('响应内容:');
    console.log(JSON.stringify(response.data, null, 2));
    
    // 检查是否所有测试都通过
    if (response.status === 200) {
      const result = response.data;
      if (result.passed_tests === result.total_tests) {
        console.log('\n✅ 所有测试通过!');
      } else {
        console.log(`\n❌ 通过了 ${result.passed_tests}/${result.total_tests} 个测试`);
        
        // 打印失败的测试
        result.test_results.forEach((testResult, i) => {
          if (!testResult.passed) {
            console.log(`\n失败的测试 #${i+1}:`);
            console.log(`  输入: ${JSON.stringify(testResult.input)}`);
            console.log(`  期望输出: ${JSON.stringify(testResult.expected_output)}`);
            console.log(`  实际输出: ${JSON.stringify(testResult.actual_output)}`);
          }
        });
      }
    }
  } catch (error) {
    console.log('\n❌ 请求失败');
    if (error.response) {
      console.log('错误状态码:', error.response.status);
      console.log('错误信息:', error.response.data);
    } else {
      console.log('错误:', error.message);
    }
  }
}

runTests(); 
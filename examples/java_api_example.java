import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Java API调用示例 - 使用Java 11的HttpClient
 */
public class JavaApiExample {
    // API端点
    private static final String API_URL = "http://localhost:8000/code/execute";
    
    public static void main(String[] args) throws IOException, InterruptedException {
        // 用户代码 - 合并区间问题
        String userCode = "import java.util.*;\n" +
                "\n" +
                "public class Solution {\n" +
                "    public List<List<Integer>> solve(List<List<Integer>> intervals) {\n" +
                "        if (intervals == null || intervals.isEmpty()) {\n" +
                "            return new ArrayList<>();\n" +
                "        }\n" +
                "        \n" +
                "        // 按区间起点排序\n" +
                "        Collections.sort(intervals, (a, b) -> a.get(0) - b.get(0));\n" +
                "        \n" +
                "        List<List<Integer>> result = new ArrayList<>();\n" +
                "        List<Integer> currentInterval = intervals.get(0);\n" +
                "        result.add(currentInterval);\n" +
                "        \n" +
                "        for (int i = 1; i < intervals.size(); i++) {\n" +
                "            List<Integer> interval = intervals.get(i);\n" +
                "            \n" +
                "            // 如果当前区间的结束点大于等于下一个区间的起点，则合并\n" +
                "            if (currentInterval.get(1) >= interval.get(0)) {\n" +
                "                // 更新结束点为两个区间结束点的最大值\n" +
                "                currentInterval.set(1, Math.max(currentInterval.get(1), interval.get(1)));\n" +
                "            } else {\n" +
                "                // 否则，添加新区间\n" +
                "                currentInterval = interval;\n" +
                "                result.add(currentInterval);\n" +
                "            }\n" +
                "        }\n" +
                "        \n" +
                "        return result;\n" +
                "    }\n" +
                "}";
        
        // 构建测试用例
        String testCases = "[\n" +
                "  {\n" +
                "    \"input\": [[1,3],[2,6],[8,10],[15,18]],\n" +
                "    \"expected_output\": [[1,6],[8,10],[15,18]],\n" +
                "    \"description\": \"示例 1: 标准合并\"\n" +
                "  },\n" +
                "  {\n" +
                "    \"input\": [[1,4],[4,5]],\n" +
                "    \"expected_output\": [[1,5]],\n" +
                "    \"description\": \"示例 2: 相邻区间\"\n" +
                "  },\n" +
                "  {\n" +
                "    \"input\": [[1,4],[0,4]],\n" +
                "    \"expected_output\": [[0,4]],\n" +
                "    \"description\": \"示例 3: 包含关系\"\n" +
                "  }\n" +
                "]";
        
        // 构建请求体
        String requestBody = "{\n" +
                "  \"code\": " + escapeJson(userCode) + ",\n" +
                "  \"language\": \"java\",\n" +
                "  \"problem_id\": \"merge-intervals\",\n" +
                "  \"test_cases\": " + testCases + "\n" +
                "}";
        
        // 创建HTTP客户端
        HttpClient client = HttpClient.newHttpClient();
        
        // 构建请求
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();
        
        // 发送请求
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        
        // 打印结果
        System.out.println("状态码: " + response.statusCode());
        System.out.println("响应内容:");
        System.out.println(response.body());
    }
    
    /**
     * 转义JSON字符串
     */
    private static String escapeJson(String input) {
        return "\"" + input.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n") + "\"";
    }
} 
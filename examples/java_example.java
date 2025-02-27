import java.util.*;

/**
 * 示例Java解决方案 - 合并区间问题
 */
public class Solution {
    /**
     * 合并重叠的区间
     * 
     * @param intervals 区间列表，每个区间是一个包含两个元素的数组 [start, end]
     * @return 合并后的区间列表
     */
    public List<List<Integer>> solve(List<List<Integer>> intervals) {
        if (intervals == null || intervals.isEmpty()) {
            return new ArrayList<>();
        }
        
        // 按区间起点排序
        Collections.sort(intervals, (a, b) -> a.get(0) - b.get(0));
        
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentInterval = intervals.get(0);
        result.add(currentInterval);
        
        for (int i = 1; i < intervals.size(); i++) {
            List<Integer> interval = intervals.get(i);
            
            // 如果当前区间的结束点大于等于下一个区间的起点，则合并
            if (currentInterval.get(1) >= interval.get(0)) {
                // 更新结束点为两个区间结束点的最大值
                currentInterval.set(1, Math.max(currentInterval.get(1), interval.get(1)));
            } else {
                // 否则，添加新区间
                currentInterval = interval;
                result.add(currentInterval);
            }
        }
        
        return result;
    }
}

/**
 * 测试代码
 */
class MergeIntervalsTest {
    public static void main(String[] args) {
        // 创建测试用例
        List<List<List<Integer>>> testCases = new ArrayList<>();
        
        // 测试用例1: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
        List<List<Integer>> test1 = new ArrayList<>();
        test1.add(Arrays.asList(1, 3));
        test1.add(Arrays.asList(2, 6));
        test1.add(Arrays.asList(8, 10));
        test1.add(Arrays.asList(15, 18));
        testCases.add(test1);
        
        // 测试用例2: [[1,4],[4,5]] -> [[1,5]]
        List<List<Integer>> test2 = new ArrayList<>();
        test2.add(Arrays.asList(1, 4));
        test2.add(Arrays.asList(4, 5));
        testCases.add(test2);
        
        // 测试用例3: [[1,4],[0,4]] -> [[0,4]]
        List<List<Integer>> test3 = new ArrayList<>();
        test3.add(Arrays.asList(1, 4));
        test3.add(Arrays.asList(0, 4));
        testCases.add(test3);
        
        // 运行测试
        Solution solution = new Solution();
        for (int i = 0; i < testCases.size(); i++) {
            List<List<Integer>> input = testCases.get(i);
            List<List<Integer>> output = solution.solve(input);
            
            System.out.println("测试用例 " + (i+1) + ":");
            System.out.println("输入: " + input);
            System.out.println("输出: " + output);
            System.out.println();
        }
    }
} 
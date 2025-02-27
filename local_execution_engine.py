class LocalExecutionEngine:
    """本地代码执行引擎"""
    
    def __init__(self):
        # 注册语言执行器
        self.executors = {
            ProgrammingLanguage.PYTHON: PythonExecutor(),
            ProgrammingLanguage.JAVASCRIPT: JavaScriptExecutor(),
            ProgrammingLanguage.JAVA: JavaExecutor(),
            ProgrammingLanguage.CPP: CppExecutor(),
            ProgrammingLanguage.GO: GoExecutor(),
            ProgrammingLanguage.RUST: RustExecutor()
        }
    
    async def execute(self, code: str, language: ProgrammingLanguage, test_input: Any) -> Tuple[Any, float, float]:
        """
        执行代码
        
        Args:
            code: 用户代码
            language: 编程语言
            test_input: 测试输入
            
        Returns:
            Tuple[Any, float, float]: (执行结果, 执行时间(ms), 内存使用(KB))
        """
        # 获取对应语言的执行器
        executor = self.executors.get(language)
        if not executor:
            raise ValueError(f"不支持的编程语言: {language}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # 准备代码文件
            filepath = executor._prepare_code_file(temp_dir, code)
            
            # 写入输入文件
            input_file = os.path.join(temp_dir, "input.json")
            with open(input_file, "w") as f:
                json.dump(test_input, f)
            
            # 编译代码（如果需要）
            compile_result = executor._compile_code(temp_dir, filepath)
            if compile_result.get("error"):
                return compile_result, 0, 0
            
            # 执行代码
            start_time = time.time()
            try:
                result, execution_time = executor._run_code(temp_dir, filepath)
                
                return result, execution_time, 0  # 简化版不计算内存使用
                
            except Exception as e:
                return {"error": f"执行错误: {str(e)}"}, (time.time() - start_time) * 1000, 0 
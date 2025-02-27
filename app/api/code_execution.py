from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Optional

from app.schemas.code_execution import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    TestCase,
    ProgrammingLanguage,
    ExecutionStatus
)
from app.services.code_execution_service import CodeExecutionService

router = APIRouter(
    prefix="/code",
    tags=["code-execution"],
    responses={
        404: {"description": "未找到"},
        500: {"description": "服务器内部错误"}
    },
)


@router.post(
    "/execute", 
    response_model=CodeExecutionResponse,
    summary="执行代码并运行测试",
    description="接收用户代码和测试用例，执行代码并返回测试结果",
    response_description="代码执行结果，包含测试通过情况、执行时间和内存使用等信息"
)
async def execute_code(
    request: CodeExecutionRequest = Body(
        ...,
        example={
            "code": "def add(a, b):\n    return a + b",
            "language": "python",
            "problem_id": "problem-001",
            "test_cases": [
                {
                    "input": {"a": 1, "b": 2},
                    "expected_output": 3,
                    "description": "简单加法测试"
                }
            ]
        }
    )
):
    """
    执行代码并运行测试
    
    - **code**: 用户提交的代码
    - **language**: 编程语言（python, javascript, java, cpp, go, rust）
    - **problem_id**: 问题ID
    - **test_cases**: 测试用例列表
    
    返回:
    - 测试结果，包含通过情况、执行时间和内存使用等信息
    """
    try:
        # 如果提供了自定义测试用例，则使用自定义测试用例
        if request.test_cases:
            test_cases = [
                TestCase(
                    input=tc.get("input"),
                    expected_output=tc.get("expected_output"),
                    description=tc.get("description")
                )
                for tc in request.test_cases
            ]
            
            # 运行测试
            return await CodeExecutionService.run_tests(
                code=request.code,
                language=request.language,
                test_cases=test_cases
            )
        else:
            # 如果没有提供测试用例，则返回错误
            return CodeExecutionResponse(
                status=ExecutionStatus.INTERNAL_ERROR,
                message="未提供测试用例"
            )
            
    except Exception as exc:
        # 处理执行过程中的异常
        return CodeExecutionResponse(
            status=ExecutionStatus.INTERNAL_ERROR,
            message=f"执行代码时发生错误: {str(exc)}"
        )


@router.post(
    "/run-test", 
    response_model=Dict[str, Any],
    summary="运行单个测试",
    description="接收用户代码和单个测试输入，执行代码并返回结果",
    response_description="代码执行结果，包含输出、执行时间和内存使用"
)
async def run_single_test(
    code: str = Body(..., description="用户提交的代码", example="def add(a, b):\n    return a + b"),
    language: ProgrammingLanguage = Body(..., description="编程语言"),
    test_input: Dict[str, Any] = Body(..., description="测试输入", example={"a": 1, "b": 2})
):
    """
    运行单个测试
    
    - **code**: 用户提交的代码
    - **language**: 编程语言（python, javascript, java, cpp, go, rust）
    - **test_input**: 测试输入数据
    
    返回:
    - **output**: 执行结果
    - **execution_time**: 执行时间(毫秒)
    - **memory_usage**: 内存使用(KB)
    """
    try:
        # 执行代码
        output, execution_time, memory_usage = await CodeExecutionService.execute_code(
            code=code,
            language=language,
            test_input=test_input
        )
        
        # 返回结果
        return {
            "output": output,
            "execution_time": execution_time,
            "memory_usage": memory_usage
        }
        
    except Exception as exc:
        # 处理执行过程中的异常
        raise HTTPException(
            status_code=500,
            detail=f"执行代码时发生错误: {str(exc)}"
        ) 
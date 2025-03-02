"""
SDK异常模块
"""


class CodeRunnerError(Exception):
    """Code Runner SDK基础异常类"""
    pass


class APIError(CodeRunnerError):
    """API调用异常"""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ValidationError(CodeRunnerError):
    """数据验证异常"""
    pass


class ConfigurationError(CodeRunnerError):
    """配置错误异常"""
    pass


class TimeoutError(CodeRunnerError):
    """请求超时异常"""
    pass 
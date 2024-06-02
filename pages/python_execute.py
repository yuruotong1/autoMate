import io
import sys
import traceback


class PythonExecute:
    def run(self, code):
        # 创建一个 StringIO 对象来捕获输出
        output = io.StringIO()
        # 保存当前的 stdout
        old_stdout = sys.stdout
        sys.stdout = output
        try:
            # 执行代码
            exec(code)
        except Exception as e:
            # 如果执行出错，返回错误的堆栈跟踪
            sys.stdout = old_stdout
            return traceback.format_exc()
        finally:
            # 恢复原来的 stdout
            sys.stdout = old_stdout
        # 获取捕获的输出并返回
        return output.getvalue()
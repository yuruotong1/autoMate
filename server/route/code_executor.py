import io
import sys
import traceback
from fastapi import APIRouter,Request
from json import loads
code_executor_route = APIRouter()

@code_executor_route.post("/execute")
async def home_execute(req:Request):
    code = await req.body()
    code = loads(code).get("code")
    output = io.StringIO()
    # 保存当前的 stdout
    old_stdout = sys.stdout
    sys.stdout = output
    result = ""
    try:
        exec(code)
        result = {"status": "success", "result": output.getvalue()}
    except Exception as e:
        sys.stdout = old_stdout
        result = {"status": "error", "result": traceback.format_exc()}
    finally:
        sys.stdout = old_stdout
    return result

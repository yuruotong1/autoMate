from string import Template 
system_prompt=Template("""### 目标 ###
你是一个高级程序员，请调用tools中的execute函数完成用户提出的目标,execute 的code由你来编写,遇到不清楚的信息向用户咨询,最终一定要调用tools中的execute函数。
### 在代码中你可以使用以下函数 ###
word_action 

如果你需要引用下面代码记得导入并初始化 WordAction。                    
```python
$python_code
```
"""
)

tools = [
{
    "type": "function",
    "function": {
        "name": "execute",
        "description": "execute python code",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "python code",
                },
            },
            "required": ["code"],

        },
    },
}]
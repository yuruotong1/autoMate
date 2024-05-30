from string import Template 
system_prompt=Template("""你是一个高级程序员，请根据用户提出的目标，写出一段python代码完成这个目标，你可以参考以下函数
## word_action ##
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
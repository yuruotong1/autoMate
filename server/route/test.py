import re
def extract_code_blocks(text):
    pattern_match = [
        r'.*?```python([\s\S]*?)```.*',
        r'.*?```([\s\S]*?)```.*'
    ]
    for pattern in pattern_match:
        pattern = re.compile(pattern, re.MULTILINE).findall(text)
        if pattern:
            return pattern[0]
        else:
            continue
if __name__ == "__main__":
    text = "为了帮助你打开并读取位于桌面上的 `a.txt` 文件，以下是相应的Python代码。请确保根据你的系统环境（如Windows或Mac OS），调整文件路径。\\n\\n```python\\n# 打开并读取桌面上的 a.txt 文件\\ntry:\\n    with open('/Users/your_username/Desktop/a.txt', 'r') as file:  # 请根据你的系统路径修改文件路径\\n        content = file.read()  # 读取文件\\n    print(content)  # 显示文件内容\\nexcept FileNotFoundError:\\n    print(\\\"文件没有找到，请确保文件路径正确。\\\")\\nexcept Exception as e:\\n    print(\\\"读取文件时发生错误:\\\", e)\\n```\\n\\n请将 `/Users/your_username/Desktop/a.txt` 中的 `your_username` 替换为你的用户名称。如果你是Windows用户，路径可能类似于 `C:\\\\\\\\Users\\\\\\\\your_username\\\\\\\\Desktop\\\\\\\\a.txt`。"
    print(extract_code_blocks(text))

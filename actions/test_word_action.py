from docx import Document

def read_word_tables(file_path):
    # 加载Word文档
    doc = Document(file_path)
    tables = []
    # 遍历文档中的所有表格
    for table in doc.tables:
        table_data = []
        # 遍历表格中的所有行
        for row in table.rows:
            row_data = []
            # 遍历行中的所有单元格
            for cell in row.cells:
                # 将单元格的文本添加到行数据中
                row_data.append(cell.text)
            # 将完整的行数据添加到表格数据中
            table_data.append(row_data)
        # 将完整的表格数据添加到结果列表中
        tables.append(table_data)
    return tables

# 示例用法
file_path = 'path_to_your_word_file.docx'
tables = read_word_tables(file_path)
for table in tables:
    for row in table:
        print(row)

from actions.action_base import action, ActionBase
class WordAction(ActionBase):
    actions_description = "word基本操作"
    def __init__(self):
        pass
    
    @action(description="批量修改表格中的内容，将表格的行和列修改为新内容")
    def change_content_for_table(self, word_path: str, start_table_number: int, end_table_number: int, table_cell: int, table_row: int, new_content: str):
        return True
    
    @action(description="批量修改表格中的内容，将表格的行和列修改为新内容")
    def tmp(self, tmp: object):
        return True

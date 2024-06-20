import { Delete } from "@icon-park/react"
import { useContextMenu } from "mantine-contextmenu"
import { useSubmit } from "react-router-dom"

export default ()=>{
    const submit = useSubmit()
    const { showContextMenu } = useContextMenu()

    const contextMenu = (category: CategoryType) => {
        return showContextMenu([
            {
              key: 'remove',
              icon: <Delete theme="outline" size="18" strokeWidth={3} />,
              title: '删除动作',
              onClick: () => {
                submit({ id: category.id }, { method: 'DELETE' })
              },
            }
          ],
            { className: 'contextMenu' })
        }
    return {contextMenu}
}
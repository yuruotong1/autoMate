import { Delete } from "@icon-park/react"
import { useContextMenu } from "mantine-contextmenu"
import { useSubmit } from "react-router-dom"
import styles from "./styles.module.scss"
import useContent from "../useContent"
import { DragEvent } from "react"
export default (category: CategoryType)=>{
    const submit = useSubmit()
    const { showContextMenu } = useContextMenu()
    const {updateContentCategory} = useContent()

    const contextMenu = () => {
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

    const dragHandle = {
      onDragOver: (e: DragEvent)=>{
        e.preventDefault()
        e!.dataTransfer!.dropEffect= 'move'
        const el = e.currentTarget as HTMLDivElement
        el.classList.add(styles.draging)
      },
      onDragLeave: (e: DragEvent)=>{
        const el = e.currentTarget as HTMLDivElement
        el.classList.remove(styles.draging)
      },
      onDrop: (e: DragEvent)=>{
        const el = e.currentTarget as HTMLDivElement
        el.classList.remove(styles.draging)
        const id = e.dataTransfer!.getData("id")
        updateContentCategory(Number(id), category.id)
      }
    }
    return {contextMenu, dragHandle}
}
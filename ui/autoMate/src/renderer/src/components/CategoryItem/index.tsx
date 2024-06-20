import { Delete, FolderClose } from "@icon-park/react"
import { NavLink, useSubmit } from "react-router-dom"
import styles from "./styles.module.scss"
import { useContextMenu } from "mantine-contextmenu"
interface Props {
    category: CategoryType
}

export const CategoryItem = ({category}: Props) => {
  const submit = useSubmit()
  const { showContextMenu } = useContextMenu()
  return (
    <NavLink 
        to={`/config/category/contentList/${category.id}`} 
        key={category.id} 
        className={({isActive})=>{
          return isActive ? styles.active : styles.link
        }}
        onContextMenu={showContextMenu([
          {
              key: 'remove',
              icon: <Delete theme="outline" size="18" strokeWidth={3} />,
              title: '删除动作',
              onClick: () => {
              submit({id: category.id}, {method: 'DELETE'})
              },
          }
          ],
          {className: 'contextMenu'})}
    >
        <div className="flex items-center gap-1">
        <FolderClose theme="outline" size="12" strokeWidth={3}></FolderClose>
        <div className="truncate">{category.name}</div>
        </div>
        </NavLink>
  )
}

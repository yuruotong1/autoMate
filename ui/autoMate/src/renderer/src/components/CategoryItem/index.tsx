import { Delete, FolderClose } from "@icon-park/react"
import { NavLink, useSubmit } from "react-router-dom"
import styles from "./styles.module.scss"
import { useContextMenu } from "mantine-contextmenu"
import { useStore } from "@renderer/store/useStore"
interface Props {
  category: CategoryType
}

export const CategoryItem = ({ category }: Props) => {
  const submit = useSubmit()
  const { showContextMenu } = useContextMenu()
  const setEditCategoryId = useStore(state => state.setEditCategoryId)
  const editCategoryId = useStore(state => state.editCategoryId)
  return (
    <>
      {editCategoryId == category.id ? (
        <div className={styles.input}>
          <input 
          defaultValue={category.name} 
          name="name" 
          autoFocus 
          onKeyDown={
            (e) => {
              if (e.key === 'Enter') {
                submit({ id: category.id, name: e.currentTarget.value }, { method: 'PUT' })
                setEditCategoryId(0)
              }
            }
          }
          />
        </div>
      ) :
        (<NavLink
          onDoubleClick={
            (_e) => {
              setEditCategoryId(category.id)
            }
          }
          to={`/config/category/contentList/${category.id}`}
          key={category.id}
          className={({ isActive }) => {
            return isActive ? styles.active : styles.link
          }}
          onContextMenu={showContextMenu([
            {
              key: 'remove',
              icon: <Delete theme="outline" size="18" strokeWidth={3} />,
              title: '删除动作',
              onClick: () => {
                submit({ id: category.id }, { method: 'DELETE' })
              },
            }
          ],
            { className: 'contextMenu' })}
        >
          <div className="flex items-center gap-1">
            <FolderClose theme="outline" size="12" strokeWidth={3}></FolderClose>
            <div className="truncate">{category.name}</div>
          </div>
        </NavLink>)
      }
    </>
  )

}

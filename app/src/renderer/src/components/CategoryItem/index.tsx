import { FolderClose } from "@icon-park/react"
import { NavLink, useFetcher} from "react-router-dom"
import styles from "./styles.module.scss"
import { useStore } from "@renderer/store/useStore"
import useCategory from "@renderer/hooks/useCategory"
interface Props {
  category: CategoryType
}

export const CategoryItem = ({ category }: Props) => {
  // fetcher 不会刷新路由
  const fetcher = useFetcher()
  const setEditCategoryId = useStore(state => state.setEditCategoryId)
  const editCategoryId = useStore(state => state.editCategoryId)
  const { contextMenu, dragHandle } = useCategory(category)
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
                  fetcher.submit({ id: category.id, name: e.currentTarget.value }, { method: 'PUT' })
                  setEditCategoryId(0)
                }
              }
            }
          />
        </div>
      ) : (
      <NavLink
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
          onContextMenu={contextMenu()}
          {...dragHandle}
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

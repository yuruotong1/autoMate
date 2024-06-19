import { FolderClose } from "@icon-park/react"
import { NavLink } from "react-router-dom"
import styles from "./styles.module.scss"
interface Props {
    category: CategoryType
}

export const CategoryItem = ({category}: Props) => {
  return (
    <NavLink 
        to={`/config/category/contentList/${category.id}`} 
        key={category.id} 
        className={({isActive})=>{
          return isActive ? styles.active : styles.link
        }}
    >
        <div className="flex items-center gap-1">
        <FolderClose theme="outline" size="12" strokeWidth={3}></FolderClose>
        <div className="truncate">{category.name}</div>
        </div>
        </NavLink>
  )
}

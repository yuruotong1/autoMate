import { AllApplication, FolderFailed } from "@icon-park/react"
import { NavLink } from "react-router-dom"
import styles from "./styles.module.scss"
export const QuickNav = () => {
  return (
    <main className="mb-3 border-b">
    <div className="px-2 mt-2 opacity-90 mb-1 text-[10px]">快捷操作</div>
    <NavLink to={`/config/category/contentList`} end className={({isActive})=>
        isActive ? styles.active : styles.link
    }>
        <div className="flex items-center gap-1">
            <AllApplication theme="outline" size="12" strokeWidth={3}/>
            <div className="truncate">所有内容</div>
        </div>
    </NavLink>
    <NavLink to={`/config/category/contentList/0`} end className={({isActive})=>
        isActive ? styles.active : styles.link
    }>
        <div className="flex items-center gap-1">
            <FolderFailed theme="outline" size="12" strokeWidth={3}/>
            <div className="truncate">未分类</div>
        </div>
    </NavLink>
    </main>
  )

}

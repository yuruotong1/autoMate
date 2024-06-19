import { AllApplication } from "@icon-park/react"
import { NavLink } from "react-router-dom"

export const QuickNav = () => {
  return (
    <>
    <div className="px-2 mt-2 opacity-90 mb-1">快捷操作</div>
    <NavLink to={`/config/category/contentList`} end className="font-blod mb-1">
        <div className="flex items-center gap-1">
            <AllApplication theme="outline" size="12" strokeWidth={3}/>
            <div className="truncate">所有内容</div>
        </div>
    </NavLink>
    <NavLink to={`/config/category/contentList/0`} end className="font-blod mb-1">
        <div className="flex items-center gap-1">
            <AllApplication theme="outline" size="12" strokeWidth={3}/>
            <div className="truncate">未分类</div>
        </div>
    </NavLink>
    </>
  )

}

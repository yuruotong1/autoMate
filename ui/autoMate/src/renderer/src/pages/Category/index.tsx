import { NavLink, Outlet, useLoaderData } from "react-router-dom"
import "./category.scss"
import { Add, AllApplication, DatabaseConfig, FolderClose } from "@icon-park/react"

export const Category = () => {
    const categories = useLoaderData() as CategoryType[]
    return (
    <main className="category-page">
        <div className="categories">
            <div className="px-2 mt-2 opacity-90 mb-1">快捷操作</div>
            {/* 加 end 表示路径完全匹配时，才会被选中 */}
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
            {categories.map((category) => (
                <NavLink 
                to={`/config/category/contentList/${category.id}`} 
                key={category.id} >
                    <div className="flex items-center gap-1">
                    <FolderClose theme="outline" size="12" strokeWidth={3}></FolderClose>
                    <div className="truncate">{category.name}</div>
                    </div>
                    </NavLink>
            ))}
        </div>

        <div className="nav">
        <Add theme="outline" size="20" fill="#333"/>
        <DatabaseConfig theme="outline" size="20" fill="#333"/>
        </div>
        <div className="content">
            <Outlet></Outlet>
        </div>
    </main>
 )
}
import { NavLink, Outlet, useLoaderData } from "react-router-dom"
import "./category.scss"
import { Add, AllApplication, DatabaseConfig, FolderClose } from "@icon-park/react"

export const Category = () => {
    const categories = useLoaderData() as CategoryType[]
    return (
    <main className="category-page">
        <div className="categories">
            {/* 加 end 是避免子路由被选中时，父路由也被选中 */}
            <NavLink to={`/config/category/contentList`} end>
                <AllApplication theme="outline" size="22" strokeWidth={3}/>
                <div className="truncate">所有内容</div>
            </NavLink>
            {categories.map((category) => (
                <NavLink 
                to={`/config/category/contentList/${category.id}`} 
                key={category.id} >
                    <FolderClose theme="outline" size="12" strokeWidth={3}></FolderClose>
                    <div className="truncate">{category.name}</div>
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